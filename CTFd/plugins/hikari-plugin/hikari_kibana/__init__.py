import requests
import json
import secrets


class KibanaHelper:

    ELASTIC_URL = "http://elastic:9200"
    ELASTIC_USERNAME = "elastic"
    ELASTIC_PASSWORD = "adminPass123"
    KIBANA_URL = "http://kibana:5601"
    KIBANA_USERNAME = "elastic"
    KIBANA_PASSWORD = "adminPass123"

    @staticmethod
    def create_space(space_name):
        headers = {
            "Content-Type": "application/json",
            "kbn-xsrf": "true"
        }
        
        # Create a new space with the given name
        space_data = {
            "id": space_name,  # Use space name directly as ID
            "name": space_name,
            "description": "A custom Kibana space",
            "disabledFeatures": []
        }

        response = requests.post(
            f"{KibanaHelper.KIBANA_URL}/api/spaces/space",
            auth=(KibanaHelper.KIBANA_USERNAME, KibanaHelper.KIBANA_PASSWORD),
            headers=headers,
            data=json.dumps(space_data)
        )

        if response.status_code == 200 or response.status_code == 201:
            print(f"Kibana space '{space_name}' created successfully!")
        else:
            print("Error:", response.text)

    @staticmethod
    def create_role(role_name, space_name):
        headers = {
            "Content-Type": "application/json",
            "kbn-xsrf": "true"
        }

        # Define the role for specific space access without sharing queries
        role_data = {
            "indices": [
                {
                    "names": ["*"],  # Adjust index patterns if needed
                    "privileges": ["read"]
                }
            ],
            "applications": [
                {
                    "application": "kibana-.kibana",
                    "privileges": ["all"],
                    "resources": [f"space:{space_name}"]  # Grant access to the specific space only
                },
                {
                    "application": "kibana-.kibana",
                    "privileges": ["all"],
                    "resources": ["feature:dashboard", "feature:discover", "feature:visualize"]  # Access only to specific features
                }
            ]
        }

        response = requests.put(
            f"{KibanaHelper.ELASTIC_URL}/_security/role/{role_name}",
            auth=(KibanaHelper.ELASTIC_USERNAME, KibanaHelper.ELASTIC_PASSWORD),
            headers=headers,
            data=json.dumps(role_data)
        )

        if response.status_code in [200, 201]:
            print(f"Role '{role_name}' created successfully!")
        else:
            print("Error:", response.text)

    @staticmethod
    def assign_user(role_name, username):
        password = secrets.token_urlsafe(18)
        user_data = {
            "roles": [role_name],
            "password": password,
            "full_name": username,
            "email": f"{username}@example.com",
            "enabled": True
        }
        
        headers = {
            "Content-Type": "application/json",
            "kbn-xsrf": "true"
        }

        response = requests.post(
            f"{KibanaHelper.ELASTIC_URL}/_security/user/{username}",
            auth=(KibanaHelper.ELASTIC_USERNAME, KibanaHelper.ELASTIC_PASSWORD),
            headers=headers,
            data=json.dumps(user_data)
        )

        if response.status_code in [200, 201]:
            print(f"User '{username}' assigned to role '{role_name}' successfully!")
            return username, password
        else:
            print("Error:", response.text)

# Create space, role, and assign user
#create_space('space01')
#create_role('role01', 'space01')
#assign_user('role01', 'account01')