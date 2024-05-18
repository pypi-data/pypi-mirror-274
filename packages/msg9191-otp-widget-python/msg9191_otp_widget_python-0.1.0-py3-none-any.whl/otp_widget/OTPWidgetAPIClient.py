
import requests
import json

class OTPWidgetAPIClient:

    def _verify_access_token(self, authkey, jwt_token):
        url = 'https://control.msg91.com/api/v5/widget/verifyAccessToken'
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "authkey": authkey,
            "access-token": jwt_token
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return None
        except Exception as err:
            return None
