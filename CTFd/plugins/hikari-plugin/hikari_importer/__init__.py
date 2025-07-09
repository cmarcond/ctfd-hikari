import zipfile
import json
import os
from CTFd.plugins.dynamic_challenges import DynamicChallenge
from CTFd.models import db, Challenges, Flags, Users, Teams, Awards, \
                            Brackets, Comments, Configs, \
                            FieldEntries, Fields, Files, \
                            Hints, Notifications, Pages, \
                            Solves, Submissions, Tags, \
                            Tokens, Topics, Tracking, Unlocks, ChallengeTopics

from CTFd.utils import get_app_config, set_config, string_types


from CTFd.plugins.hikari_challenge import HikariChallengeModel
from CTFd.utils.uploads import get_uploader
from ..hikari_models import ZerotierConfig, JsonLogFiles

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

import dataset


class HikariImporter:
    def __init__(self, zip_filename):
        self.zipfile = zip_filename
        self.tmppath = '/tmp'
        self.working_path = '/tmp/db/'

        # Unziping file
        self.backup = zipfile.ZipFile(self.zipfile)
        self.backup.extractall(path=self.tmppath)

        # Creating and setting up conn with db
        self.side_db = dataset.connect(get_app_config("SQLALCHEMY_DATABASE_URI"))

    def get_path(self, json_file):
        return os.path.join(self.working_path, json_file)

    def import_awards(self):
        self.import_data('awards.json', Awards)

    def import_brackets(self):
        self.import_data('brackets.json', Brackets)
    
    def import_challenges(self):
        self.import_data('challenges.json', Challenges)
    
    def import_challenge_topics(self):
        self.import_data('challenge_topics.json', ChallengeTopics)

    def import_comments(self):
        self.import_data('comments.json', Comments)

    def import_config(self):
        self.import_data('config.json', Configs)
    
    def import_dynamic_challenge(self):
        self.import_data('dynamic_challenge.json', DynamicChallenge)
    
    def import_field_entries(self):
        self.import_data('field_entries.json', FieldEntries)
    
    def import_fields(self):
        self.import_data('fields.json', Fields)
    
    def import_files(self):
        self.import_data('files.json', Files)
    
    def import_flags(self):
        self.import_data('flags.json', Flags)
    
    def import_hikari_challenge_model(self):
        self.import_data('hikari_challenge_model.json', HikariChallengeModel)

    def import_hints(self):
        self.import_data('hints.json', Hints)

    def import_json_log_files(self):
        self.import_data('json_log_files.json', JsonLogFiles)

    def import_notifications(self):
        self.import_data('notifications.json', Notifications)

    def import_pages(self):
        self.import_data('pages.json', Pages)
    
    def import_solves(self):
        self.import_data('solves.json', Solves)
    
    def import_submissions(self):
        self.import_data('submissions.json', Submissions)

    def import_tags(self):
        self.import_data('tags.json', Tags)
    
    def import_teams(self):
        self.import_data('teams.json', Teams)

    def import_tokens(self):
        self.import_data('tokens.json', Tokens)
    
    def import_topics(self):
        self.import_data('topics.json', Topics)
    
    def import_tracking(self):
        self.import_data('tracking.json', Tracking)

    def import_unlocks(self):
        self.import_data('unlocks.json', Unlocks)
    
    def import_users(self):
        self.import_data('users.json', Users)
    
    def import_zerotier_config(self):
        self.import_data('zerotier_config.json', ZerotierConfig)

    def import_uploads(self):
        files = [f for f in self.backup.namelist() if f.startswith("uploads/")]
        uploader = get_uploader()
        for f in files:
            filename = f.split(os.sep, 1)
            if (
                len(filename) < 2 or os.path.basename(filename[1]) == ""
            ):  # just an empty uploads directory (e.g. uploads/) or any directory
                continue

            filename = filename[1]  # Get the second entry in the list (the actual filename)
            source = self.backup.open(f)
            uploader.store(fileobj=source, filename=filename)


    #####################
    def import_data(self, json_filename, model):
        try:
            with open(self.get_path(json_filename), 'r') as f:
                jdata = json.loads(f.read())
        except Exception as e:
            print(f"Error loading json file: {e}")
            return False
    
        data = jdata['results']
        table = self.side_db[json_filename[:-5]]
        for _zdata in data:
            try:
                req = _zdata.get('requirements')
                if req and isinstance(req, dict):
                    _zdata['requirements'] = json.dumps(req)

                table.insert(_zdata)
            except IntegrityError:
                print(f"ERROR FOR TABLE: {json_filename}")
            except Exception as e:
                print(f"ERROR: {e}")
        return True

    def import_all(self):
        self.side_db.query("SET FOREIGN_KEY_CHECKS=0;")
        self.import_teams()
        self.import_users()
        self.import_challenges()
        self.import_dynamic_challenge()
        self.import_hikari_challenge_model()
        self.import_zerotier_config()
        self.import_flags()
        self.import_hints()
        self.import_unlocks()
        self.import_awards()
        self.import_tags()
        self.import_topics()
        self.import_submissions()
        self.import_solves()
        self.import_files()
        self.import_notifications()
        self.import_pages()
        self.import_tracking()
        self.import_config()
        self.import_fields()
        self.import_brackets()
        self.import_challenge_topics()
        self.import_comments()
        self.import_field_entries()
        self.import_json_log_files()
        self.import_tokens()
        self.import_uploads()
        self.side_db.query("SET FOREIGN_KEY_CHECKS=1;")
    