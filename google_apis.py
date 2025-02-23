import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import streamlit as st

def create_service(client_secret_file, api_name, api_version, *scopes):
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    CLIENT_SECRET_FILE = client_secret_file

    # Check if user already logged in
    if 'credentials' not in st.session_state:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=SCOPES,
            redirect_uri='http://<ec2-public-ip>:8501'  # Replace with your EC2 IP
        )
        auth_url, state = flow.authorization_url(prompt='consent')
        st.session_state['oauth_state'] = state

        # Show login button
        st.write("Click below to log in with Google:")
        if st.button("Login with Google"):
            st.write(f"Go here: {auth_url}")
            st.write("Copy the code it gives you after logging in:")
            auth_code = st.text_input("Paste Code Here")
            if auth_code:
                flow.fetch_token(code=auth_code)
                st.session_state['credentials'] = flow.credentials

    creds = st.session_state.get('credentials')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            st.session_state['credentials'] = creds
        else:
            st.write("Please log in above.")
            return None

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(f"{API_SERVICE_NAME} {API_VERSION} service created")
        return service
    except Exception as e:
        print(f"Error: {e}")
        return None
