# PixPayloadGen

O Payload-Pix é um gerador de payload para transações PIX que cria um código QR a partir das informações fornecidas, facilitando a realização de pagamentos.

## Funcionalidades

- Geração de payload PIX com base em informações fornecidas (valor, nome, chave PIX, cidade, ID-Estabelecimento).
- Cálculo do código CRC16 para validação do payload.
- Geração de código QR para o payload PIX.
- Salvamento do código QR como um arquivo PNG.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `crcmod`
  - `qrcode[pil]`
 
  - 
Você pode instalar a biblioteca usando:

```sh
pip install PixPayloadGen
```


Você pode instalar as bibliotecas necessárias usando:

```sh
pip install crcmod qrcode[pil]
```


Você pode importar a biblioteca usando:

```sh
from PixPayloadGen import PayloadPixGen
```


Chamar função responsavel para gerar a Payload e QRCODE:

```sh
PayloadPixGen('VALOR', 'NOME', 'CHAVE-PIX', 'CIDADE' , 'NOME DA LOJA')
```


Chamada com dados Ficticios:

```sh
PayloadPixGen('30,00', 'Victor Julio Rocha', '97212482404', 'RECIFE' , 'VIPSURF')
```

Payload Gerada:

```sh
00020126330014BR.GOV.BCB.PIX011197212482404520400005303986540530.005802BR5918Victor Julio Rocha6006RECIFE62110507VIPSURF630425A1
```




