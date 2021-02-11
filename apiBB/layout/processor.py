from apiBB.layout.pdf import BoletoPDF
from apiBB.layout.bancodobrasil import BoletoBB
import datetime


def get_data_bb(data, boleto):
    d = BoletoBB(7, 2)
    d.nosso_numero = data['numeroTituloCliente'][-7:]
    d.numero_documento = data['numeroTituloBeneficiario']
    d.convenio = data['numeroConvenio']
    d.especie_documento = 'DM'

    d.carteira = str(data['numeroCarteira'])
    d.cedente = data['beneficiarioFinal']['nome']
    d.cedente_documento = str(data['beneficiarioFinal']['numeroInscricao'])
    d.cedente_endereco = "{}, {} - {} - {} - CEP: {}".format(boleto['beneficiario']['logradouro'],
                                                             boleto['beneficiario']['bairro'],
                                                             boleto['beneficiario']['cidade'],
                                                             boleto['beneficiario']['uf'],
                                                             boleto['beneficiario']['cep'])
    d.agencia_cedente = str(boleto['beneficiario']['agencia'])
    d.conta_cedente = str(boleto['beneficiario']['contaCorrente'])

    d.data_vencimento = datetime.datetime.strptime(data['dataVencimento'], "%d.%m.%Y").date()
    d.data_documento = datetime.datetime.strptime(data['dataEmissao'], "%d.%m.%Y").date()
    d.data_processamento = datetime.datetime.now().date()

    d.instrucoes = [
        "COBRAR JUROS DE R$ {} POR DIA DE ATRASO".format(data['jurosMora']['valor']) if 'jurosMora' in data else "",
        "COBRAR MULTA DE R$ {} A PARTIR DE {}".format(data['multa']['valor'], data['multa']['data']) if 'multa' in data else "",
        "PAGAVEL EM QUALQUER BANCO"
    ]
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


def get_pdf(data, boleto):
    boleto_PDF = BoletoPDF('boleto-bb-{}.pdf'.format(boleto['numero']))
    boleto_PDF.drawBoleto(get_data_bb(data, boleto))
    boleto_PDF.nextPage()
    boleto_PDF.save()
    return boleto_PDF
