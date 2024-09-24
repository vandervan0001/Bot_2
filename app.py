import streamlit as st
import requests
from authlib.integrations.requests_client import OAuth2Session
import os

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
DISCORD_API_ENDPOINT = "https://discord.com/api/v10"
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")
DISCORD_REQUIRED_ROLE = os.getenv("DISCORD_REQUIRED_ROLE")

def get_token(auth_code):
    token_url = "https://discord.com/api/oauth2/token"
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': DISCORD_REDIRECT_URI,
    }
    response = requests.post(token_url, data=data)
    return response.json()

def get_user_roles(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{DISCORD_API_ENDPOINT}/users/@me/guilds/{DISCORD_GUILD_ID}/member"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["roles"]
    else:
        return []

def check_user_role(roles, required_role):
    return required_role in roles

auth_code = st.experimental_get_query_params().get('code')

if auth_code:
    token = get_token(auth_code[0])
    user_roles = get_user_roles(token['access_token'])

    if check_user_role(user_roles, DISCORD_REQUIRED_ROLE):
        st.success("Accès autorisé au chatbot")
        # Intégrer ici le code du chatbot LlamaIndex
    else:
        st.error("Accès refusé. Vous n'avez pas le rôle requis.")
else:
    auth_url = f"https://discord.com/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope=identify%20guilds"
    st.write(f"[Connecte-toi avec Discord]({auth_url})")
