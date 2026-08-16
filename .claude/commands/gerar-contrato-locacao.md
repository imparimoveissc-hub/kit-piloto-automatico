# Gerar Contrato de Locação

Gera automaticamente o **Contrato de Locação** e o **Termo de Vistoria** preenchidos, salvando no Desktop com nomenclatura padrão. Nunca altera os modelos originais.

## Como usar

Rode o script interativo:

```bash
python3 "/Users/user/Downloads/Kit-Piloto-Automatico-V30-DISTRIB/00_OS/commands/gerar-contrato-locacao.py"
```

Ou, se o usuário passar os dados diretamente no chat, colete os campos abaixo e chame as funções do script via Python inline.

## Campos obrigatórios (modelo de perguntas base)

| Campo | Descrição |
|-------|-----------|
| **Locador / Proprietário** | Nome, nacionalidade, profissão, RG, CPF, endereço. 2º locador se houver. |
| **Locatário / Inquilino** | Nome, nacionalidade, profissão (opcional), RG (opcional), CPF, endereço. |
| **Residencial ou Comercial** | RESIDENCIAL ou COMERCIAL |
| **Imóvel** | Endereço completo, denominação, área privativa, área total, matrícula, inscrição imobiliária |
| **Prazo** | Quantidade de meses + extenso (ex: 12 / doze) |
| **Início do contrato** | Data no formato DD/MM/AAAA |
| **1º vencimento do aluguel** | Data no formato DD/MM/AAAA |
| **Dia de vencimento** | Número do dia (ex: 10) |
| **Valor do aluguel** | Ex: R$ 1.100,00 + por extenso |
| **Fiança locatícia** | Valor |
| **Seguro incêndio** | Valor |
| **IPTU** | Valor (opcional) |
| **Taxa de lixo** | Valor (opcional) |
| **Condomínio** | Valor (opcional, deixar vazio se não tiver) |
| **Valor total** | Aluguel + IPTU + lixo + fiança + seguro + condomínio |
| **Data do contrato** | Ex: 29 de Maio de 2025 |
| **Condição específica** | Qualquer cláusula única para este contrato (opcional) |
| **Ar condicionado** | Descrição detalhada ou "Não possui" |
| **Demais acessórios** | Descrição ou "Não possui" |
| **Chaves** | Descrição do que foi entregue |
| **Fotos** | Caminho da pasta (opcional — inserir manualmente no termo) |

## Saída

Uma **pasta nova** é criada no Desktop com o título:
`Locação - Rua, nº e Bairro - Proprietário x Locatário`

Dentro da pasta:
- `Contrato de locação - Rua, nº e bairro - Proprietário x Locatário.docx`
- `TERMO DE VISTORIA - Rua, nº e bairro - Proprietário x Locatário.docx`

Se a pasta já existir com o mesmo nome, um sufixo numérico é adicionado automaticamente (ex: `... (2)`).

## Regras

- **Nunca alterar** os modelos originais em `Claude Desktop/Modelos de contrato/LOCAÇÃO/`
- Fotos do termo de vistoria devem ser inseridas manualmente (tamanho: vertical 8cm×4,5cm ou horizontal 4cm×7,11cm)
- Condições específicas únicas devem ser inseridas manualmente no contrato após geração
