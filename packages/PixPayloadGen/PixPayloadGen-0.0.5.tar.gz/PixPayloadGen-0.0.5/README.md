# [PixPayloadGen](https://pypi.org/project/PixPayloadGen/)

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

# Formatação das chaves do DICT no BR Code

A regra para formatação das chaves Pix no BR Code com trilho Pix segue estritamente as regras definidas no Manual Operacional do DICT.

## E-mail

O e-mail será codificado no seguinte formato:

```sh
e-mail: fulano_da_silva.recebedor@example.com
```
## CPF ou CNPJ

O CPF e o CNPJ serão codificados no seguinte formato:

```sh
CPF: 12345678900
CNPJ: 00038166000105
```

## Número de telefone celular

O telefone será codificado seguindo o formato internacional:

```sh
+5561912345678
```

Em que:

- `+55`: código do país.
- `61`: código do território ou estado.
- `912345678`: número do telefone celular.


## Chave aleatória

A chave aleatória será codificada juntamente com a pontuação, como segue:

```sh
123e4567-e12b-12d1-a456-426655440000
```





