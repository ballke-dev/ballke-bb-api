from requests import put, get, post
import json

TIMEOUT = 15


class Pix:
    def __init__(self, sandbox=True, credentials=None):
        self.sandbox = sandbox
        self.credentials = credentials
        self.versao_pix = self.credentials['versao_pix']
        self.url_base = "https://api.hm.bb.com.br/" if self.sandbox else "https://api.bb.com.br/"
        self.url_token = 'https://oauth.sandbox.bb.com.br/oauth/token' if sandbox \
            else "https://oauth.bb.com.br/oauth/token"
        self.token_pix = self.get_token_pix().get("access_token")
        self.headers_pix = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token_pix)
        }
        self.developer_application_key_pix = self.credentials['pix_sandbox']['developer_application_key'] \
            if self.sandbox else self.credentials['pix_production']['developer_application_key']

    def get_token_pix(self):
        data_token_pix = {
            "grant_type": "client_credentials",
            "scope": "cob.write cob.read pix.read"
        }
        headers = {
            "Authorization": self.credentials['pix_sandbox']['basic'] if self.sandbox else
            self.credentials['pix_production']['basic'],
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = post(self.url_token, data=data_token_pix, headers=headers, verify=False).json()
        return response

    def create_cob(self, data):
        txid = data['txid']
        data.pop('txid')
        response = put("{}pix/{}/cobqrcode/{}?".format(self.url_base, self.versao_pix, txid),
                       params={
                           'gw-dev-app-key': self.developer_application_key_pix
                       }, headers=self.headers_pix, data=json.dumps(data), verify=False, timeout=TIMEOUT).json()
        return response

    def read_cob(self, data):
        response = get("{}pix/{}/cob/{}?".format(self.url_base, self.versao_pix, data['txid']), params={
            'gw-dev-app-key': self.developer_application_key_pix
        }, headers=self.headers_pix, verify=False, timeout=TIMEOUT)
        return json.loads(json.dumps(response.text))
