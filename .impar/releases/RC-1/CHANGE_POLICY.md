# Política de Mudança — Kernel IMPAR RC-1

**Data:** 2026-07-23  
**Versão:** 3.0.0  
**Status:** Frozen Release Candidate  

---

## 1. Componentes Protegidos

Os seguintes componentes estão **congelados** nesta RC-1:

### 🔒 Críticos (Require Full Recertification)

- `.impar/lib/executor.sh` — Controlador de execução
- `.impar/lib/audit-chain.sh` — Hash-chaining de eventos
- `.impar/lib/certifier.sh` — Validador de integridade
- `.impar/modules/verify-audit.sh` — Verificador de cadeia
- `.impar/modules/certify.sh` — Certificador de kernel
- `.impar/executor_whitelist.json` — Whitelist de serviços
- `.impar/registry.json` — Configuração do kernel
- `.impar/graph.json` — Grafo de conhecimento
- `.impar/VERSION` — Versão do kernel
- `07_LOGS/EXECUTION_AUDIT.jsonl` — Baseline legado (IMUTÁVEL)

### ⚠️ Sensíveis (Require Recertification)

- `.impar/knowledge/` — Arquivos de conhecimento
- `.impar/lib/` — Todas as bibliotecas
- `.impar/modules/` — Todos os módulos
- `.impar/CHANGELOG.md` — Histórico de mudanças
- `.impar/RELEASE_NOTES.md` — Notas de release

---

## 2. Regras de Modificação

### Regra 1: Componentes Críticos
**Se modificar:** executor, audit-chain, certifier, verify-audit, certify, whitelist, registry, graph, version

**Ação obrigatória:**
1. Criar nova branch isolada
2. Aplicar mudança
3. Executar suite completo: 20 testes negativos
4. Executar `impar verify-audit`
5. Executar `impar certify`
6. Gerar novo certificado
7. **NÃO liberar operacionalmente sem novo certificado PASS**

### Regra 2: Arquivo Legado Imutável
**Se EXECUTION_AUDIT.jsonl for alterado:**
- Falha automática (fail-closed)
- Execução cancelada
- Investigação obrigatória
- Resultado: FAIL (não aceitar sob nenhuma circunstância)

### Regra 3: Conhecimento e Automações
**Se modificar:** graph.json, automations.json, launchagents.json

**Ação obrigatória:**
1. Validar com `impar certify`
2. Atualizar INTEGRITY_MATRIX.json
3. Documentar em CHANGELOG.md
4. Nova certificação se componentes críticos foram afetados

### Regra 4: Serviços na Whitelist
**Se adicionar novo serviço à whitelist:**
1. Preparar especificação
2. Testar em ambiente isolado
3. Executar autorização explícita
4. Criar aprovação de uso único
5. Executar dentro de revalidação do DR
6. Solicitar recertificação

### Regra 5: Permissões
**Se modificar:** permissões de arquivos, proprietários, grupos

**Ação obrigatória:**
1. Restaurar a partir de INTEGRITY_MATRIX.json
2. Documentar mudança em 07_LOGS/decisions.md
3. Recertificar se críticos

---

## 3. Processo de Descongelamento

Para sair de RC-1 e iniciar ETAPA 3B:

1. **Autorização explícita do usuário** — Sem exceção
2. **Validação de pré-requisitos:**
   - verify-audit PASS
   - certify PASS
   - Whitelist conforme planejado
   - WhatsApp status confirmado
3. **Plano escrito** — Detalhando mudanças da 3B
4. **Aprovação** — Uso único, 60 segundos
5. **Execução isolada** — Sem afetar componentes críticos
6. **Recertificação** — Se modificado critical_components
7. **Novo RC** — RC-2 gerado ao final

---

## 4. Escalação de Divergências

**Se algum hash não corresponder ao INTEGRITY_MATRIX.json:**

1. **Investigar imediatamente:**
   - Quem modificou?
   - Quando?
   - Qual versão do arquivo estava antes?

2. **Diagnóstico:**
   - Git blame para mudanças
   - Compare com backup
   - Valide integridade

3. **Ação:**
   - Se não autorizado: ROLLBACK
   - Se autorizado: Recertifique
   - Se crítico: FAIL status até resolução

4. **Relatório:**
   - Documentar em 07_LOGS/divergences.md
   - Registrar em auditoria
   - Escalação se necessário

---

## 5. Versioning

**RC-1** → RC-2 (quando sair de ETAPA 3B)  
**RC-2** → Production (quando ETAPA 3C completa)

Cada RC nova gera novo INTEGRITY_MATRIX.json com hashes atualizados.

---

## 6. Contatos e Escalação

Se mudança em componente crítico é necessária mas não autorizada:
- Documentar em CLAUDE.md
- Aguardar decisão do operador
- Não prosseguir sem confirmação explícita

---

**Status RC-1:** Frozen. Nenhuma modificação sem recertificação.  
**Próximo passo:** Aguardar autorização para ETAPA 3B.

