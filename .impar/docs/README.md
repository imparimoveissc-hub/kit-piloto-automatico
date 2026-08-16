# IMPAR — Ponto de Entrada Central

**Versão:** 1.0.0  
**Projeto:** Kit Piloto Automático V30 — Impar Imóveis  
**Modo:** Somente leitura + Backup seguro

---

## Visão Geral

`impar` é um wrapper único que concentra o acesso aos principais comandos de gerenciamento da Automação Completa Impar Imóveis.

Todos os comandos operam em **modo somente leitura** por padrão. Nenhuma automação é alterada, nenhuma mensagem é enviada, nenhuma credencial é exposta.

---

## Instalação

O comando já está instalado em:

```bash
~/.local/bin/impar
```

Para usar em qualquer lugar do terminal:

```bash
impar help
```

---

## Comandos Disponíveis

### 1. `impar help`
Mostrar esta ajuda com exemplos.

```bash
impar help
```

### 2. `impar status`
Consultar estado atual das automações (somente leitura).

```bash
impar status
```

**Mostra:**
- LaunchAgents ativos
- Automações conhecidas
- Memória persistente
- Task ledger
- Checkpoints encontrados
- Serviços intencionalmente desligados
- Alertas atuais

### 3. `impar doctor`
Executar diagnóstico completo (somente leitura).

```bash
impar doctor
```

**Verifica:**
- Estrutura do projeto
- Arquivos críticos
- Validade de JSON
- LaunchAgents
- Integridade de memória
- Logs
- Permissões
- Espaço em disco
- Checkpoints

### 4. `impar logs [módulo]`
Listar e filtrar logs por módulo.

```bash
# Listar todos os módulos
impar logs

# Ver logs de um módulo específico
impar logs marketplace
impar logs messenger
impar logs whatsapp
impar logs leads
impar logs grupos
```

**Módulos suportados:**
- `marketplace` — Marketplace + Grupos
- `grupos` — Publicação em Grupos
- `messenger` — Messenger Inbox
- `whatsapp` — WhatsApp
- `leads` — Leads Chaves na Mão
- `nfse` — Emissão de NFS-e
- `memory` — Memória Persistente
- `launchagents` — LaunchAgents

### 5. `impar memory`
Mostrar estado da memória persistente (somente leitura).

```bash
impar memory
```

**Mostra:**
- Validação do índice MEMORY.md
- Estatísticas (arquivos, tamanho, linhas)
- Categorias de memória
- Lista de arquivos
- Últimas atualizações

### 6. `impar backup`
Criar backup seguro de memória e configurações.

```bash
impar backup
```

**Inclui:**
- Todos os arquivos .md de memória
- Configuração do wrapper
- Documentação criada pelo projeto

**Exclui:**
- Credenciais (.env, secrets)
- Cookies e sessões
- Chaves SSH/GPG
- Logs muito grandes
- .git/ e controle de versão
- Checkpoints JSON

---

## Arquitetura

```
.impar/
├── config.json           # Configuração central
├── impar                 # Executável principal
├── lib/
│   └── common.sh         # Biblioteca de funções
├── modules/
│   ├── status.sh         # Módulo status
│   ├── doctor.sh         # Módulo doctor
│   ├── logs.sh           # Módulo logs
│   ├── memory.sh         # Módulo memory
│   └── backup.sh         # Módulo backup
└── docs/
    └── README.md         # Esta documentação
```

---

## Exemplos de Uso

### Verificar estado geral
```bash
impar status
```

### Executar diagnóstico
```bash
impar doctor
```

### Ver logs do Messenger
```bash
impar logs messenger
```

### Verificar memória
```bash
impar memory
```

### Criar backup
```bash
impar backup
```

---

## Segurança

✓ **Todos os comandos são somente leitura** por padrão

✓ **Nenhuma credencial, token ou dado sensível é exposto**

✓ **Backup copia apenas memória e configurações autorizadas**

✓ **Nenhuma ação destrutiva é permitida**

✓ **Nenhum envio real de mensagens ou publicações**

✓ **Nenhuma modificação de automações, LaunchAgents ou .env**

✓ **WhatsApp permanece offline e não é reautenticado**

---

## Estrutura de Dados

### Configuração (config.json)

```json
{
  "version": "1.0.0",
  "name": "impar-wrapper",
  "project_root": "...",
  "memory_path": "~/.claude/projects/.../memory",
  "logs_path": "07_LOGS",
  "read_only_commands": ["help", "status", "doctor", "logs", "memory"],
  "safe_commands": ["backup"]
}
```

### Memória (MEMORY.md)

A memória está estruturada em 4 categorias:

1. **CONHECIMENTO ESTRUTURAL** — Arquitetura permanente
2. **CONFIRMADO AGORA** — Verificado na data mais recente
3. **MEMÓRIA/HISTÓRICO** — Dados potencialmente antigos
4. **NECESSITA VERIFICAÇÃO** — Pendente de confirmação

---

## Limitações Atuais

- ✗ Não implementa: start, stop, restart
- ✗ Não implementa: marketplace, whatsapp, messenger, grupos, leads, nfse diretos
- ✗ Não integra com CI/CD ou pre-commit hooks
- ✗ Não faz reescrita automática de memória
- ✗ Não auto-compacta arquivos

Estes recursos estão reservados para futuras versões.

---

## Próximas Versões

**ETAPA 2 (Futuro):**
- Implementar `impar start`, `impar stop`, `impar restart`
- Adicionar `impar marketplace --status`
- Adicionar `impar logs --filter` para busca avançada
- Implementar auto-sincronização de memória

**ETAPA 3+ (Futuro):**
- Integração com CI/CD
- Dashboard web
- Webhooks
- Notificações em tempo real

---

## Suporte

Se encontrar problemas:

1. Execute `impar doctor` para diagnóstico
2. Consulte `impar logs` para histórico
3. Verifique `impar memory` para contexto

---

## Desenvolvido por

**Kit Piloto Automático V30 — Impar Imóveis**

Data: 2026-07-22  
Versão: 1.0.0  
Modo: Beta
