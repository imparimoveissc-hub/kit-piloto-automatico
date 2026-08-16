---
name: project-automacao-contratos
description: "Automação de geração de contratos imobiliários (locação, vistoria e administração) para a Impar Imóveis"
metadata: 
  node_type: memory
  type: project
  originSessionId: a28a2d16-067e-4a92-aefa-a5995a931201
---

# Automação de Contratos — Impar Imóveis

## Script principal
`/Users/user/Downloads/Kit-Piloto-Automatico-V30-DISTRIB/00_OS/commands/gerar-contrato-locacao.py`

## Modelos originais (nunca alterar)
Pasta: `/Users/user/Desktop/Claude Desktop/Modelos de contrato /LOCAÇÃO/`
- `CONTRATO DE LOCAÇÃO - (LOFT) Seguro fiança atualizado - Exemplo - cópia.docx`
- `TERMO DE VISTORIA PARA LOCAÇÃO - Exemplo - Padrão .docx`
- `CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE ADMINISTRAÇÃO IMOBILIÁRIA - IMPAR.docx`

## O que é gerado a cada contrato de locação

Cria uma **pasta nova no Desktop** com o título:
`Locação - Rua, nº e Bairro - Proprietário x Locatário`

Dentro da pasta, 3 arquivos gerados automaticamente:
1. `Contrato de locação - ...docx` — campos amarelos preenchidos
2. `TERMO DE VISTORIA - ...docx` — campos amarelos preenchidos
3. `Contrato de Administração - ...docx` — CONTRATANTE + IMÓVEL preenchidos

Se a pasta já existir com o mesmo nome, adiciona sufixo `(2)`, `(3)` etc.

## Campos editados por documento

### Contrato de Locação (campos amarelos)
- LOCADOR(A)(ES) — dados completos do proprietário
- LOCATÁRIO(A) — dados completos do inquilino
- Imóvel — endereço, denominação, área, matrícula, inscrição imobiliária
- Prazo — meses, datas de início/encerramento, vencimento
- Aluguel — valor, extenso, forma de pagamento
- Data de assinatura

### Termo de Vistoria (campos amarelos)
- LOCADOR, LOCATÁRIA, imóvel (reaproveitados)
- Item 9 — Ar condicionado
- Item 10 — Demais acessórios
- Item 13 — Chaves entregues
- Data
- Fotos: inseridas manualmente (vertical 8×4,5cm / horizontal 4×7,11cm)

### Contrato de Administração (placeholders de colchetes)
- CONTRATANTE — nome, nacionalidade, estado civil, profissão, RG, CPF, endereço
- IMÓVEL — mesmos dados do contrato de locação
- Linha de assinatura — nome e CPF do proprietário

## Regras
- Jamais alterar os modelos originais
- Usar `[A PREENCHER]` como placeholder quando dado estiver faltando
- **Destaque amarelo obrigatório:** todo `[A PREENCHER]` deve ter `<w:highlight w:val="yellow"/>` no `<w:rPr>` do run correspondente — se o placeholder estiver no meio de um texto maior, quebrar o `<w:r>` em múltiplos runs e aplicar o highlight só na parte do placeholder
- Quando o dado for fornecido e o campo for preenchido, remover o highlight amarelo junto com o texto `[A PREENCHER]`
- Fotos do termo de vistoria: inserir manualmente
- IPTU, taxa de lixo e condomínio podem ser inclusos no aluguel — quando for o caso, ajustar a cláusula de encargos do contrato de locação

## Modelo de perguntas base
1. Locador: nome, nacionalidade, profissão, RG, CPF, endereço, estado civil, cônjuge (se houver)
2. Locatário: nome, nacionalidade, profissão, RG, CPF, endereço
3. Uso: Residencial ou Comercial
4. Imóvel: endereço, denominação, área privativa, área total, matrícula, inscrição imobiliária
5. Prazos: meses, extenso, início, fim, 1º vencimento, dia mensal
6. Valores: aluguel, extenso, IPTU, taxa lixo, condomínio, fiança, seguro incêndio, total
7. Data do contrato
8. Condição específica (opcional)
9. Vistoria: ar condicionado, demais acessórios, chaves

## **Why:** Agilizar a geração de contratos imobiliários da Impar Imóveis sem risco de alterar modelos padrão.
## **How to apply:** Sempre que o Jonata pedir para gerar um contrato de locação, usar este script/fluxo. Os documentos de RG/CPF podem ser enviados como foto para extração automática dos dados.
