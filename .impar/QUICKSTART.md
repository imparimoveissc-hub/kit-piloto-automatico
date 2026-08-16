# IMPAR v1.0.0 — Guia de Início Rápido

## Comando Único

```bash
impar
```

## Uso Rápido

### 1. Ver ajuda
```bash
impar help
```

### 2. Verificar estado
```bash
impar status
```

### 3. Executar diagnóstico
```bash
impar doctor
```

### 4. Ver logs
```bash
# Listar todos os módulos
impar logs

# Ver logs específicos
impar logs marketplace
impar logs messenger
impar logs whatsapp
impar logs leads
```

### 5. Verificar memória
```bash
impar memory
```

### 6. Criar backup
```bash
impar backup
```

## Localização dos Arquivos

| Localização | Propósito |
|-------------|-----------|
| `~/.local/bin/impar` | Executável global |
| `.impar/config.json` | Configuração |
| `.impar/modules/` | 5 submódulos |
| `.impar/lib/common.sh` | Biblioteca compartilhada |
| `.impar/docs/README.md` | Documentação completa |

## Estrutura de Diretórios

```
.impar/
├── config.json
├── impar (executável principal)
├── lib/
│   └── common.sh
├── modules/
│   ├── status.sh
│   ├── doctor.sh
│   ├── logs.sh
│   ├── memory.sh
│   └── backup.sh
└── docs/
    └── README.md
```

## Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `impar help` | Mostrar ajuda |
| `impar status` | Estado das automações (somente leitura) |
| `impar doctor` | Diagnóstico completo (somente leitura) |
| `impar logs` | Listar logs (somente leitura) |
| `impar memory` | Memória persistente (somente leitura) |
| `impar backup` | Criar backup seguro |

## Exemplos Práticos

### Diagnosticar problemas
```bash
impar doctor
```

### Ver últimos logs do Messenger
```bash
impar logs messenger
```

### Verificar memória
```bash
impar memory
```

### Backup de segurança
```bash
impar backup
```

## Informações Importantes

- ✅ Todos os comandos são **somente leitura** por padrão
- ✅ Nenhuma credencial é exposta
- ✅ Nenhuma automação é alterada
- ✅ WhatsApp permanece offline
- ✅ Completamente reversível

## Rollback (se necessário)

```bash
rm ~/.local/bin/impar
rm -rf .impar/
```

## Próximos Passos

1. Execute `impar help` para ver todos os comandos
2. Execute `impar status` para ver o estado atual
3. Execute `impar doctor` para diagnóstico completo

---

**Versão:** 1.0.0  
**Modo:** Beta (Pronto para Produção)
