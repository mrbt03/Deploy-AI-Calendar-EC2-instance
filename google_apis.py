import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

def create_service(service_account_file, api_name, api_version, *scopes, prefix=''):
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    # Load service account credentials
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(f"{API_SERVICE_NAME} {API_VERSION} service created successfully")
        return service
    except Exception as e:
        print(f"Failed to create service instance for {API_SERVICE_NAME}: {e}")
        return None
