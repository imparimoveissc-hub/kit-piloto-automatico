# Rotina: Marketplace + Grupos para Amanhã (2026-07-18)

Fluxo de execução após postagens de hoje.

## Cronograma

| Horário | Etapa | Responsável |
|---------|-------|-------------|
| ~22:00 (hoje) | Postagens Marketplace finalizadas | Browser/Automação |
| 08:00-09:00 (amanhã) | Rodar gerador de fila de grupos | CLI/Python |
| 09:00+ (amanhã) | Publicar em grupos (cadência 3min/grupo) | Browser/Automação |

## Pré-requisitos

- [x] `fila-postagens.csv` gerada (hoje, rodar `generate_queue.py`)
- [x] `grupos-aprovados.csv` preenchido com 19 grupos (se não, usa placeholders)
- [x] Python 3.8+ instalado

## 1. Gerar fila de grupos para amanhã

Após confirmação de que as postagens de **hoje** no Marketplace foram concluídas:

```bash
cd 18_AUTOMATION_STACK/impar-facebook-marketplace-posting
python3 generate_group_queue.py 2026-07-18
```

**Saída esperada:**
- `fila-grupos-postagens.csv` com 19 grupos × N imóveis de amanhã
- Status: "rascunho_revisao_humana" (se grupos preenchidos) ou "aguardando_lista_de_grupos" (se placeholders)

**Ou rodar tudo junto (fila + grupos):**
```bash
./run_full_pipeline.sh 2026-07-18
```

## 2. Validar fila

Abrir `fila-grupos-postagens.csv` e verificar:

- [ ] Todas as linhas têm `grupo_nome` preenchido (sem `[A PREENCHER]`)
- [ ] Horários respeitam cadência de 3 minutos
- [ ] `data_sugerida` é 2026-07-18
- [ ] `status_publicacao` = "rascunho_revisao_humana" (pronto) ou "aguardando_lista_de_grupos" (falta preencher)

**Se houver placeholders:** Preencher `grupos-aprovados.csv` antes de continuar.

## 3. Publicar em grupos

### Opção A: Browser manual (seguro, com confirmação)

1. Abrir Facebook em navegador logado da Impar
2. Navegar para cada grupo na `fila-grupos-postagens.csv`
3. Colar descrição + foto (usar o template de `fila-postagens.csv`)
4. Aguardar 3 minutos antes de postar no próximo grupo

### Opção B: Automação (requer script de browser)

```bash
python3 publish_marketplace_playwright.py --mode=groups --target-day=2026-07-18
```

**Requer:**
- Playwright + navegador Chrome/Firefox instalado
- Sessão do Facebook mantida (login prévio)
- Arquivos de configuração `.env` com credenciais

## Checklist antes de publicar

- [ ] Imóveis de amanhã estão na fila (`fila-postagens.csv`)
- [ ] Grupos-aprovados estão todos preenchidos em `grupos-aprovados.csv`
- [ ] Fila de grupos foi gerada sem erros (`fila-grupos-postagens.csv`)
- [ ] Fotos dos imóveis estão disponíveis (verificar URLs)
- [ ] Descrições estão sem erros de caracteres/encoding
- [ ] Cadência de 3 minutos entre grupos está confirmada no CSV

## Troubleshooting

### Erro: "Nenhum imóvel encontrado em 2026-07-18"

**Causa:** A fila do Marketplace não foi gerada para essa data.

**Solução:**
```bash
python3 generate_queue.py
# Verificar datas disponíveis em fila-postagens.csv
python3 generate_group_queue.py 2026-07-18
```

### Erro: "Grupos ainda com placeholders"

**Causa:** `grupos-aprovados.csv` não foi preenchido.

**Solução:**
1. Abrir `grupos-aprovados.csv`
2. Listar 19 grupos do Facebook aprovados
3. Preencher nome + URL
4. Salvar e rodar de novo

### Timeout/Erro de conexão

**Causa:** Rede/Facebook indisponível.

**Solução:**
- Aguardar 2-3 minutos
- Verificar conexão de internet
- Rodar script de novo

## Monitoramento pós-publicação

Após publicações começarem:

```bash
# Verificar status de publicação
grep "2026-07-18" fila-grupos-postagens.csv | grep -c "publicado"

# Listar erros
grep "ERRO" fila-grupos-postagens.csv
```

## Documentação

- `README.md` — Visão geral da automação
- `generate_group_queue.py` — Script de geração de fila
- `publish_marketplace_playwright.py` — Script de publicação automática (beta)
- `grupos-aprovados.csv` — Lista de grupos aprovados
