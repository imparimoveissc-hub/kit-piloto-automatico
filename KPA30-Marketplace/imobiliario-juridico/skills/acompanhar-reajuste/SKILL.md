---
name: acompanhar-reajuste
description: >
  Mostra contratos com reajuste anual ou fim de vigência chegando, e avisa antes dos prazos
  fecharem, trabalhando a partir de um registro mantido. Use quando o usuário perguntar "quais
  contratos reajustam agora", "o que vence esse mês", "algum aluguel pra reajustar", "adiciona
  esse contrato ao acompanhamento", ou em base agendada. Recebe entradas de gerar-contrato-locacao.
argument-hint: "[--dias N para mudar a janela | --vencidos para prazos que passaram]"
---

# /acompanhar-reajuste

Mostra o que reajusta e quando a vigência termina.

## Instruções

0. **Carregue o playbook** (`~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md`) para
   pegar o índice padrão e o destino dos alertas. Se houver marcadores `[PREENCHER]`, **pare** e peça:
   "Rode `/imobiliario-juridico:cold-start-interview` primeiro — preciso do índice e do destino dos
   alertas antes de acompanhar reajustes."

1. **Leia `~/.claude/plugins/config/kpa30/imobiliario-juridico/registro-reajustes.yaml`**
   (diretório de config — sobrevive a atualizações). Se não existir, copie o template de
   `references/registro-reajustes.yaml`.

2. **Modo padrão:** próximos 90 dias, agrupado por urgência com intervalos meio-abertos para cada
   prazo cair em exatamente uma faixa: 🔴 0–13 dias, 🟠 14–44 dias, 🟡 45–89 dias. Os dias 14, 45 e 90
   são limites — cada um pertence a exatamente uma faixa.

3. **Dois tipos de evento por contrato:**
   - **Reajuste anual:** a cada 12 meses da data de início, aplicar o índice do contrato
     (IGP-M/IPCA/INCC). Mostre o valor atual, o índice acumulado no período e o valor sugerido.
   - **Fim de vigência:** data de término; para residencial ≥ 30 meses, sinalizar janela de
     denúncia vazia.

4. **`--dias N`:** muda a janela.

5. **`--vencidos`:** reajustes cuja data passou sem aplicação registrada, e vigências vencidas.

6. **Se o Asaas estiver conectado:** cruze com as cobranças para confirmar que o valor cobrado
   bate com o último reajuste aplicado; sinalize divergências.

7. **Saída inclui ações recomendadas:** quem avisar (proprietário/inquilino do registro), qual
   índice usar e o novo valor calculado. Toda sugestão de valor é **rascunho para conferência**.

## Adicionar/atualizar uma entrada

Quando chamada com dados de um contrato novo (da skill de geração ou manual), acrescente uma
entrada em `renovacoes:` no registro, com data de início, índice, valor e contatos.

## Exemplos

```
/imobiliario-juridico:acompanhar-reajuste
```

```
/imobiliario-juridico:acompanhar-reajuste --dias 180
```

```
/imobiliario-juridico:acompanhar-reajuste --vencidos
```
