# BB API

Pacote utilizado para estar facilitando o desenvolvimento a mudanças da nova api do Banco do Brasil.

### Antes de começar
Rode `pip install whell`<br>
Para utilizar qrcode na geração do pix instale `pip install qrcode[pil]
`
<br>
E nossas classes como `pip install git+https://github.com/ballke-dev/bb-api.git#egg=apiBB`
# Utilização

Métodos e chamadas prontos a unica utilização necessária é o envio de data como irei explicar nos próximos exemplos

## Create Cobranca

Para a utilização do create cobranca é necessario ter os seguintes dados em um dicionário  **data** .
```
{
   "numeroConvenio":3128557,
   "numeroCarteira":17,
   "numeroVariacaoCarteira":35,
   "codigoModalidade":1,
   "dataEmissao":"30.10.2019",
   "dataVencimento":"01.11.2019",
   "valorOriginal":100.00,
   "valorAbatimento":0,
   "quantidadeDiasProtesto":0,
   "indicadorNumeroDiasLimiteRecebimento":"N",
   "numeroDiasLimiteRecebimento":0,
   "codigoAceite":"A",
   "codigoTipoTitulo":4,
   "descricaoTipoTitulo":"DS",
   "indicadorPermissaoRecebimentoParcial":"N",
   "numeroTituloBeneficiario":"TESTE2",
   "textoCampoUtilizacaoBeneficiario":"TESTE3",
   "codigoTipoContaCaucao":0,
   "numeroTituloCliente":"00031285570000000001",
   "textoMensagemBloquetoOcorrencia":"TESTE5",
   "jurosMora":{
      "tipo":1,
      "valor":""
   },
   "multa":{
      "tipo":1,
      "valor":"",
      "data":""
   },
   "pagador":{
      "tipoRegistro":1,
      "numeroRegistro":71128590182,
      "nome":"NOME",
      "endereco":"ENDERECO",
      "cep":70675727,
      "cidade":"SAO PAULO",
      "bairro":"CENTRO",
      "uf":"SP",
      "telefone":"999939669"
   },
   "email":"cliente@email.com"
}
```
exemplo de boleto com pix em py
```
from apiBB.cobranca import Cobranca
import qrcode


def generate_billet_pix():
    cob = Cobranca(sandbox=True, credentials=BANCO_DO_BRASIL)
    cob.sandbox = False #or True if mode is delevopment
    data = {
        "numeroConvenio": 3128557,
        "dataVencimento": "10.01.2021",
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
        "numeroTituloCliente": "00031285570033300853",
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
    if not 'errors' in response:
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
```
## Gerar pdf

Consiste basicamente em chamar a função de geração informando data e o response da criação de boleto que retorna o objeto pdf
<br>
Exemplo:
```
from apiBB.layout.processor import get_pdf

img = get_pdf(data, response)

```
## Read cobranca

Método para consulta de boletos já registrados, aqui é feito a consulta em um único boleto por vez onde o **data**  precisa estar formatado da seguinte forma.
```
{  
    'numeroConvenio': 3128557,
    'nn': ""  
}
```

## Read cobranca list

 **Ainda não testado**
 Aqui temos a possibilidade de consultar e ter como resultado uma lista de boletos, sendo possível pegar apenas os boletos já pagos, mas como a api sandbox não possibilita a visualização de boletos liquidados o método ainda não esta finalizado
 **data** :
 ```
 {
	 "agencia": "",
	 "conta": "",
	 "situacao" "",
	 "estado_titulo": "",
	 "inicio_vencimento": "",
	 "fim_vencimento": ""
 }
```

# PIX

Novo método de pagamento onde o intuito são transações instantâneas entre usuários.

## Create cobranca

Como parâmetro obrigatório o envio de `txid` na url para a criação da transação como método `PATH`, envio de data ficaria assim:
```
{
   "txid": "",
   "calendario":{
      "expiracao":"<integer>"
   },
   "devedor":{
      "cpf":{
         "value":"<Error: Could not resolve allOf schema"
      },
      "nome":"<string>"
   },
   "valor":{
      "original":{
         "value":"<Error: Could not resolve allOf schema"
      }
   },
   "chave":"<string>",
   "solicitacaoPagador":"<string>",
   "infoAdicionais":[
      {
         "nome":"<string>",
         "valor":"<string>"
      },
      {
         "nome":"<string>",
         "valor":"<string>"
      }
   ]
}
```
exemplo de um código feito em py utilizando as classes e gerando qrcode
```
from apiBB.pix import Pix
import qrcode


def generate_pix():
    pix = Pix(sandbox=True, credentials=BANCO_DO_BRASIL)
    pix.sandbox = False #or True if mode is delevolpment
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
```

## Read Cobranca
Para a consulta do estado atual do pix é necessario o envio apenas do `txid` como um parâmetro de consulta, sendo data assim:
```
 "txid": ""
```

