from apiBB.cobranca import Cobranca
from apiBB.pix import Pix
import qrcode


def generate_billet_production():
    data = {
        'numeroConvenio': 1627888,
        'numeroCarteira': 17,
        'numeroVariacaoCarteira': 43,
        'codigoModalidade': 1,
        'dataEmissao': '01.02.2021',
        'dataVencimento': '03.03.2021',
        'valorOriginal': 1.00,
        'valorAbatimento': 0,
        'quantidadeDiasProtesto': 0,
        'indicadorNumeroDiasLimiteRecebimento': 'N',
        'numeroDiasLimiteRecebimento': 1,
        'codigoAceite': 'A',
        'codigoTipoTitulo': 4,
        'descricaoTipoTitulo': 'Duplicata Mercantil',
        'indicadorPermissaoRecebimentoParcial': 'N',
        'numeroTituloBeneficiario': '000460-1',
        'campoUtilizacaoBeneficiario': '',
        'codigoTipoContaCaucao': 0,
        'numeroTituloCliente': '00016278880000040035',
        "jurosMora": {
            "tipo": 1,
            "valor": 0.02
        },
        'multa': {
            'tipo': 1,
            'valor': 0.0148,
            'data': '04.03.2021'
        },
        'mensagemBloquetoOcorrencia': 'PAGAVEL EM QUALQUER BANCO',
        'pagador': {
            'tipoInscricao': 1,
            'numeroInscricao': 45933389803,
            'nome': 'DIOGO BALTAZAR DO NASCIMENTO',
            'endereco': 'AVENIDA PORTO ALEGRE, 877',
            'cep': 89802131,
            'cidade': 'CHAPECÓ',
            'bairro': 'CENTRO',
            'uf': 'SC',
            'telefone': '13997527728'
        },
        'beneficiarioFinal': {
            'tipoInscricao': 2,
            'numeroInscricao': '06103122000785',
            'nome': 'MAGAZINE MEDICA'
        },
        'indicadorPix': 'S'
    }
    cob = Cobranca(sandbox=False)
    response = cob.register_billet(data)
    if not 'erros' in response:
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=0)
        qr.add_data(response['qrCode'].get('emv'))
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('qrcode001.png')
    else:
        print(response)


def generate_billet_pix():
    cob = Cobranca()
    data = {
        "numeroConvenio": 3128557,
        "dataVencimento": "10.03.2021",
        "valorOriginal": 600.00,
        "numeroCarteira": 17,
        "numeroVariacaoCarteira": 35,
        "codigoModalidade": 1,
        "dataEmissao": "29.12.2020",
        "valorAbatimento": 0,
        "quantidadeDiasProtesto": 10,
        "quantidadeDiasNegativacao": 10,
        "orgaoNegativador": 10,
        "numeroDiasLimiteRecebimento": 10,
        "codigoAceite": "A",
        "codigoTipoTitulo": 4,
        "descricaoTipoTitulo": "Duplicata Mercantil",
        "indicadorPermissaoRecebimentoParcial": "S",
        "numeroTituloBeneficiario": "33300001",
        "campoUtilizacaoBeneficiario": "TESTE",
        "numeroTituloCliente": "00031285570033300854",
        "mensagemBloquetoOcorrencia": "TESTE",
        "desconto": {
            "tipo": 0,
            "porcentagem": 0,
            "valor": 0
        },
        "segundoDesconto": {
            "porcentagem": 0,
            "valor": 0
        },
        "terceiroDesconto": {
            "porcentagem": 0,
            "valor": 0
        },
        "jurosMora": {
            "tipo": 1,
            "porcentagem": 0,
            "valor": 3.00
        },
        "pagador": {
            "tipoInscricao": 1,
            "numeroInscricao": 12679202899,
            "nome": "Nome do Pagador",
            "endereco": "Rua dos Pagadores",
            "cep": 11020000,
            "cidade": "Santos",
            "bairro": "Boqueirao",
            "uf": "SP",
            "telefone": "1334000000"
        },
        "beneficiarioFinal": {
            "tipoInscricao": 1,
            "numeroInscricao": 51796036846,
            "nome": "Quem recebe os valores"
        },
        "indicadorPix": "S"
    }
    response = cob.register_billet(data)
    if not 'erros' in response:
        print(response)
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=0)
        qr.add_data(response['qrCode'].get('emv'))
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('qrcode001.png')
    else:
        print(response)


def read_billet():
    cob = Cobranca(sandbox=False, credentials=BANCO_DO_BRASIL)
    data = {
        'nn': '00016278880000039853',
        'numeroConvenio': 1627888
    }
    print(cob.read_billet(data))


def generate_pix():
    pix = Pix(sandbox=True, credentials=BANCO_DO_BRASIL)
    data = {
        "txid": "magazine89012123345678901245",
        "calendario": {
            "expiracao": 3600
        },
        "devedor": {
            "cnpj": "12345678000195",
            "nome": "Empresa de Serviços SA"
        },
        "valor": {
            "original": "37.00"
        },
        "chave": "d14d32de-b3b9-4c31-9f89-8df2cec92c50",
        "solicitacaoPagador": "Serviço realizado.",
        "infoAdicionais": [
            {
                "nome": "Campo 1",
                "valor": "Informação Adicional1 do PSP-Recebedor"
            },
            {
                "nome": "Campo 2",
                "valor": "Informação Adicional2 do PSP-Recebedor"
            }
        ]
    }
    response = pix.create_cob(data)
    if not 'errors' in response:
        print(response)
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=0)
        qr.add_data(response['textoImagemQRcode'])
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('qrcode001.png')
    else:
        print(response)


if __name__ == "__main__":
    # generate_billet_pix()
    read_billet()
    # generate_pix()
    # generate_billet_production()