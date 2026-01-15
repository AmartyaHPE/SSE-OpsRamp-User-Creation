import requests
from typing import Dict, Optional

class OpsRampAuth:

    def __init__(self, base_url: str, client_key: str, client_secret: str):
        self.base_url = base_url.rstrip('/')
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token: Optional[str] = None
        self.token_type: Optional[str] = None
    
    def get_token(self) -> Dict[str, str]:
        if self.access_token:
            return {
                'access_token': self.access_token,
                'token_type': self.token_type
            }
        
        url = f"{self.base_url}/tenancy/auth/oauth/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        data = {
            'grant_type': 'client_credentials',
            'client_key': self.client_key,
            'client_secret': self.client_secret
        }

        response = requests.post(url, headers=headers, data=data, verify=False)

        token_data = response.json()
        self.access_token = token_data['access_token']
        self.token_type = token_data['token_type']

        return {
            'access_token': self.access_token,
            'token_type': self.token_type
        }
    
    def get_auth_header(self) -> Dict[str, str]:

        token_info = self.get_token()
        return {
            'Authorization': f"Bearer {token_info['access_token']}"
        }


        