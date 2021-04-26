from requests import get, post
import json

TIMEOUT = 15


class Cobranca:
    def __init__(self, sandbox=True, credentials=None):
        self.credentials = credentials
        self.sandbox = sandbox
        self.url_token = 'https://oauth.sandbox.bb.com.br/oauth/token' if sandbox \
            else "https://oauth.bb.com.br/oauth/token"
        self.token_cobranca = self.get_token_cobranca().get("access_token")
        self.headers_cobranca = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token_cobranca)
        }
        self.developer_application_key_cobranca = self.credentials['cobranca_sandbox'][
            'developer_application_key'] if self.sandbox \
            else self.credentials['cobranca_production']['developer_application_key']
        self.versao_cob = self.credentials['versao_cob']
        self.url_base = "https://api.sandbox.bb.com.br/" if self.sandbox else "https://api.bb.com.br/"

    def get_token_cobranca(self):
        data_token_cobranca = {
            "grant_type": "client_credentials",
            "scope": "cobrancas.boletos-info cobrancas.boletos-requisicao"
        }
        headers = {
            "Authorization": self.credentials['cobranca_sandbox']['basic'] if self.sandbox else
            self.credentials['cobranca_production']['basic'],
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = post(self.url_token, data=data_token_cobranca, headers=headers, verify=False).json()
        return response

    def register_billet(self, data):
        response = post("{}cobrancas/{}/boletos?".format(self.url_base, self.versao_cob),
                        params={
                            'gw-dev-app-key': self.developer_application_key_cobranca
                        }, data=json.dumps(data), headers=self.headers_cobranca, timeout=TIMEOUT, verify=False).json()
        return response

    def read_billet(self, data):
        response = get("{}cobrancas/{}/boletos/{}?".format(self.url_base, self.versao_cob, data['nn']),
                       params={
                           'gw-dev-app-key': self.developer_application_key_cobranca,
                           'numeroConvenio': data['numeroConvenio'],
                       }, headers=self.headers_cobranca, timeout=TIMEOUT, verify=False).json()
        return response

    def read_billet_list(self, data):
        response = get("{}cobrancas/{}/boletos/?".format(self.url_base, self.versao_cob), params={
            'gw-dev-app-key': self.developer_application_key_cobranca,
            'agenciaBeneficiario': data['agencia'],
            'contaBeneficiario': data['conta'],
            'indicadorSituacao': data['situacao'],
            'codigoEstadoTituloCobranca': data['estado_titulo'],
            'dataInicioVencimento': data['inicio_vencimento'],
            'dataFimVencimento': data['fim_vencimento']
        }, headers=self.headers_cobranca, timeout=TIMEOUT, verify=False).json()
        return response

    def cancel_billet(self, data):
        billet_id = data['nn']
        data.pop('nn')
        response = post("{}cobrancas/{}/boletos/{}/baixar".format(self.url_base, self.versao_cob, billet_id),
                        params={
                            'gw-dev-app-key': self.developer_application_key_cobranca
                        }, data=json.dumps(data), headers=self.headers_cobranca, timeout=TIMEOUT, verify=False).json()
        return response
