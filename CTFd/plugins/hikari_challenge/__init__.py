import os
import json
from flask import Blueprint
from CTFd.models import Challenges, db
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.migrations import upgrade
from CTFd.models import (
    ChallengeFiles,
    Challenges,
    Fails,
    Flags,
    Hints,
    Solves,
    Tags,
    db,
)

from CTFd.utils.challenges import (
    get_all_challenges,
    get_solve_counts_for_challenges,
    get_solve_ids_for_user_id,
    get_solves_for_challenge_id,
)

from CTFd.utils.uploads import delete_file
from CTFd.utils.uploads import upload_file


from confluent_kafka import Producer, Consumer, KafkaException, KafkaError

# KAFKA CONFIGURATION
PROD = os.environ.get("PROD", "False").lower() in ["true", "1", "yes"]
if PROD:
    bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka.elk.svc.cluster.local:9092")
    sasl_mechanism = os.environ.get("KAFKA_SASL_MECHANISM", "SCRAM-SHA-512")
    sasl_username = os.environ.get("KAFKA_SASL_USERNAME")
    sasl_password = os.environ.get("KAFKA_SASL_PASSWORD")
    producer_config = {
         'bootstrap.servers': bootstrap_servers,
         'security.protocol': 'SASL_SSL',
         'sasl.mechanisms': sasl_mechanism,
         'sasl.username': sasl_username,
         'sasl.password': sasl_password,
    }
else:
    bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    producer_config = {'bootstrap.servers': bootstrap_servers}

####### HikariController for controlling actiavation of logs
class HikariController:
    def __init__(self):
        # No code here needed for now
        pass

    # Send logs to kafka topic
    @staticmethod
    def activate_logs(chall_id):
        challenge = HikariChallengeModel.query.filter_by(id=chall_id).first()
        data = json.loads(challenge.chall_logs)
        if not isinstance(data, list):
            return
 
        for record in data:
            try:
                producer.produce('competition1', value=json.dumps(record).encode('utf-8'))
            except KafkaError as e:
               print(f"Error: {e}")
        
        # Garante que todos os dados sejam enviados
        producer.flush()


###### Hikari Challenge database representation
class HikariChallengeModel(Challenges):
    __mapper_args__ = {"polymorphic_identity": "hikari"}
    id = db.Column(db.Integer, db.ForeignKey("challenges.id", ondelete='CASCADE'), primary_key=True)
    logs_activated = db.Column(db.Boolean, default=False)
    is_first_challenge = db.Column(db.Boolean, default=False)
    logs_filename = db.Column(db.String(255))
    chall_logs = db.Column(db.JSON, nullable=False)

    def __init__(self, *args, **kwargs):
        super(HikariChallengeModel, self).__init__(**kwargs)
    

###### Custom Hikari Challenge created.
class HikariChallenge(BaseChallenge):
    id = "hikari"
    name = "hikari"
    templates = {
        "create": "/plugins/hikari_challenge/assets/create.html",
        "update": "/plugins/hikari_challenge/assets/update.html",
        "view": "/plugins/hikari_challenge/assets/view.html",
    }
    scripts = {
        "create": "/plugins/hikari_challenge/assets/create.js",
        "update": "/plugins/hikari_challenge/assets/update.js",
        "view": "/plugins/hikari_challenge/assets/view.js",
    }
    route = "/plugins/hikari_challenge/assets/"
    blueprint = Blueprint(
        "hikari-challenge",
        __name__,
        template_folder="templates",
        static_folder="assets",
    )

    challenge_model = HikariChallengeModel  

    @classmethod
    def read(cls, challenge):
        challenge = HikariChallengeModel.query.filter_by(id=challenge.id).first()
        data = {
            "id": challenge.id,
            "name": challenge.name,
            "value": challenge.value,
            "description": challenge.description,
            "connection_info": challenge.connection_info,
            "next_id": challenge.next_id,
            "category": challenge.category,
            "state": challenge.state,
            "max_attempts": challenge.max_attempts,
            "type": challenge.type,
            "chall_logs":challenge.chall_logs,
            "logs_filename": challenge.logs_filename,
            "is_first_challenge":challenge.is_first_challenge,
            "type_data": {
                "id": cls.id,
                "name": cls.name,
                "templates": cls.templates,
                "scripts": cls.scripts,
            },
        }

        return data

    @classmethod
    def update(cls, challenge, request):
        data = request.form or request.get_json()
       
        for attr, value in data.items():
            setattr(challenge, attr, value)
            print(attr, ":", value)
        db.session.commit()

        return challenge
    
    @classmethod
    def solve(cls, user, team, challenge, request):
        super().solve(user, team, challenge, request)
        
        # Grab all challenges available
        all_challenges = HikariChallengeModel.query.all()

        # Get all solves made by this user
        solve_ids = Solves.query.filter_by(user_id=user.id).all()
        solve_ids = [s.challenge_id for s in solve_ids]

        # Get challenges that were not solved by the user
        challs = [c for c in all_challenges if c.id not in solve_ids]

        # For each challenge not solved by the user,
        # check if all the prerequisites were solved by the user and,
        # if that is the case, activate the logs for this current challenge
        for chall in challs:
            prereqs = set()
            if chall.requirements:
                prereqs = set(chall.requirements.get('prerequisites'))
            if len(prereqs) == 0:
                continue
            if chall.logs_activated:
                continue
            if len(prereqs.intersection(solve_ids)) == len(prereqs):
                print("\n\n\n[ * * * ACTIVATING NEXT CHALLENGE LOGS: {} * * * ]".format(chall.name))
                HikariController.activate_logs(chall.id)
                print("\n\n\n")

                # Updating challenge logs status
                setattr(chall, 'logs_activated', True)
                db.session.commit()


def load(app):
    app.db.create_all()
    upgrade(plugin_name="hikari_challenge")
    CHALLENGE_CLASSES["hikari"] = HikariChallenge
    register_plugin_assets_directory(
        app, base_path="/plugins/hikari_challenge/assets/"
    )
