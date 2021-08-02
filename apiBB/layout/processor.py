from apiBB.layout.pdf import BoletoPDF
from apiBB.layout.bancodobrasil import BoletoBB
import datetime
import pathlib


def get_data_bb(data, path_logo):
    d = BoletoBB(7, 2, path_logo)
    d.nosso_numero = data['numeroTituloCliente']
    d.numero_documento = data['numeroTituloBeneficiario']
    d.convenio = data['numeroConvenio']
    d.especie_documento = 'DM'

    d.carteira = str(data['numeroCarteira'])
    d.cedente = data['beneficiario']['nome']
    d.cedente_documento = str(data['beneficiario']['numeroInscricao'])
    d.cedente_endereco = "{}, {} - {} - {} - CEP: {}".format(data['beneficiario']['logradouro'],
                                                             data['beneficiario']['bairro'],
                                                             data['beneficiario']['cidade'],
                                                             data['beneficiario']['uf'],
                                                             data['beneficiario']['cep'])
    d.agencia_cedente = str(data['beneficiario']['agencia'])
    d.conta_cedente = str(data['beneficiario']['contaCorrente'])

    d.data_vencimento = datetime.datetime.strptime(data['dataVencimento'], "%d.%m.%Y").date()
    d.data_documento = datetime.datetime.strptime(data['dataEmissao'], "%d.%m.%Y").date()
    d.data_processamento = datetime.datetime.now().date()

    d.instrucoes = [
        "COBRAR JUROS DE R$ {} POR DIA DE ATRASO".format(data['jurosMora']['valor']) if 'jurosMora' in data else "",
        "COBRAR MULTA DE R$ {} A PARTIR DE {}".format(data['multa']['valor'], data['multa']['data']) if 'multa' in data else "",
    ]

    if 'instrucoes' in data:
        d.instrucoes = data['instrucoes']

    d.demonstrativo = [
        # "- Serviço Teste R$ 5,00",
        # "- Total R$ 5,00",
    ]
    d.valor_documento = data['valorOriginal']

    d.sacado = [
        "{}".format(data['pagador']['nome']),
        "{}, {} - {} - {} - CEP: {}".format(data['pagador']['endereco'], data['pagador']['bairro'],
                                            data['pagador']['cidade'], data['pagador']['uf'], data['pagador']['cep'])
    ]
    return d


def get_pdf(data):
    boleto_PDF = BoletoPDF('boleto-bb-{}.pdf'.format(data['numeroTituloCliente']))
    boleto_PDF.drawBoleto(get_data_bb(data, pathlib.Path('layout/media/logo_bb.png').resolve()))
    boleto_PDF.nextPage()
    return boleto_PDF
