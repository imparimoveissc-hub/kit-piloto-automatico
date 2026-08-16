---
name: customize
description: >
  Ajusta o perfil da prática já configurado — muda índice de reajuste padrão, modalidade de
  garantia, destino dos alertas, tom do memorando ou a matriz de escalonamento — sem re-rodar a
  entrevista inteira. Use quando o usuário disser "muda o índice pra IPCA", "manda os alertas pro
  grupo tal", "ajusta a regra de escalonamento", "atualiza o playbook".
argument-hint: '[o que ajustar em linguagem natural]'
---

# /customize

Edita pontualmente o perfil em `~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md`.

## Instruções

1. **Carregue o perfil da config.** Se houver `[PREENCHER]`, isto ainda não foi configurado —
   direcione para `/imobiliario-juridico:cold-start-interview`.

2. **Entenda o pedido** e localize a seção exata a mudar (playbook, estilo da casa, escalonamento,
   integrações).

3. **Mostre o antes → depois** do trecho afetado e confirme antes de gravar.

4. **Grave só o trecho alterado.** Não reescreva o arquivo inteiro nem apague seções não citadas.

5. **Confirme** o que mudou e onde.

## Exemplos

```
/imobiliario-juridico:customize muda o índice padrão para IPCA
```

```
/imobiliario-juridico:customize alertas de reajuste vão para o grupo "Impar — Locação"
```
