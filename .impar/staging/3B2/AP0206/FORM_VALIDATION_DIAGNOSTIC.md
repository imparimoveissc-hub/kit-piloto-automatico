# DIAGNÓSTICO DE VALIDAÇÃO DO FORMULÁRIO — AP0206

**Data:** 2026-07-23  
**Objetivo:** Descobrir por que o botão "Avançar" permanece desabilitado  
**Status:** Investigação em andamento

---

## CHECKLIST DE VALIDAÇÃO DO FORMULÁRIO

### SEÇÃO 1: CAMPOS OBRIGATÓRIOS E VISIBILIDADE

Campos que DEVEM estar preenchidos para ativar "Avançar":

#### 1.1 — Categoria do Imóvel
- [ ] Campo obrigatório: `required`
- [ ] Preenchido: "Locação de Imóveis" ou equivalente
- [ ] Visível: SIM
- [ ] Desabilitado: NÃO
- [ ] Mensagem de erro: NENHUMA
- **Evidência esperada:** Seletor `select[name="category"]` ou `input[aria-label*="categoria"]`

#### 1.2 — Tipo de Imóvel
- [ ] Campo obrigatório: `required`
- [ ] Preenchido: "Apartamento"
- [ ] Visível: SIM
- [ ] Desabilitado: NÃO
- [ ] Mensagem de erro: NENHUMA
- **Evidência esperada:** `select[name="property_type"]` ou similar

#### 1.3 — Título do Anúncio
- [ ] Campo obrigatório: `required`
- [ ] Preenchido: "Apartamento 5 Dormitórios - Ubatuba, São Francisco do Sul - R$ 2.800"
- [ ] Comprimento: 7-120 caracteres (Facebook limita)
- [ ] Visível: SIM
- [ ] Desabilitado: NÃO
- [ ] Mensagem de erro: NENHUMA
- **Evidência esperada:** `input[name="title"]` ou `textarea[aria-label*="título"]`

#### 1.4 — Descrição
- [ ] Campo obrigatório: `required`
- [ ] Preenchido: SIM (com markdown ou HTML limpo)
- [ ] Mínimo de caracteres: 25 (típico Facebook)
- [ ] Máximo de caracteres: 4000 (típico Facebook)
- [ ] Visível: SIM
- [ ] Desabilitado: NÃO
- [ ] Mensagem de erro: NENHUMA
- **Evidência esperada:** `textarea[name="description"]`

#### 1.5 — Preço
- [ ] Campo obrigatório: `required`
- [ ] Preenchido: "2800" ou "2,800" ou "2.800" (verificar formato aceito)
- [ ] Formato: Número positivo
- [ ] Moeda: "BRL" (se seletor separado)
- [ ] Visível: SIM
- [ ] Desabilitado: NÃO
- [ ] Mensagem de erro: NENHUMA
- **Evidência esperada:** `input[name="price"]` ou `input[type="number"][name="price"]`

#### 1.6 — Localização
- [ ] Campo obrigatório: `required`
- [ ] Preenchido: "São Francisco do Sul, SC, Brasil" ou formato aceito
- [ ] Método de entrada: SELEÇÃO DE LISTA (não digitação livre)
- [ ] Validado: SIM (deve corresponder a localização real do Marketplace)
- [ ] Visível: SIM
- [ ] Desabilitado: NÃO
- [ ] Mensagem de erro: NENHUMA
- **Evidência esperada:** `input[aria-label*="localização"]` + autocomplete + seleção

#### 1.7 — Imagens
- [ ] Campo obrigatório: `required` (mínimo 1 imagem)
- [ ] Preenchido: SIM (68 imagens de AP0206)
- [ ] Mínimo de imagens: 1
- [ ] Máximo de imagens: 50 (típico Facebook Marketplace)
- [ ] Upload completo: SIM (processamento finalizou)
- [ ] Erros de upload: NENHUM
- [ ] Visível: SIM (thumbnail preview)
- [ ] Desabilitado: NÃO
- [ ] Mensagem de erro: NENHUMA
- **Evidência esperada:** `input[type="file"][name="images"]` + preview grid

---

### SEÇÃO 2: CAMPOS OCULTOS OBRIGATÓRIOS

Campos que podem estar em `display:none` mas ainda participar da validação:

#### 2.1 — Verificar atributos aria-hidden
```
document.querySelectorAll('[aria-hidden="true"]')
  .filter(el => el.value || el.required)
```
- [ ] Token CSRF: preenchido
- [ ] ID de sessão: preenchido
- [ ] Timestamp: preenchido
- [ ] Hash de validação: preenchido (se aplicável)

#### 2.2 — Verificar display:none
```
document.querySelectorAll('[style*="display:none"]')
  .filter(el => el.value || el.required)
```
- [ ] Nenhum campo obrigatório está oculto sem motivo

---

### SEÇÃO 3: CONDIÇÕES DEPENDENTES DA CATEGORIA

Quando categoria = "Locação de Imóveis", campos adicionais PODEM ser obrigatórios:

- [ ] **Duração do aluguel:** Meses? Anos? Campo presente e preenchido?
- [ ] **Disponibilidade:** "Disponível agora", "Data específica"?
- [ ] **Tipo de ocupação:** Residencial? Comercial? Misto?
- [ ] **Modalidade:** Aluguel simples? Com financiamento? Permuta?
- [ ] **Documentação:** Requer comprovante de propriedade?

**Cada campo condicional deve estar validado quando obrigatório.**

---

### SEÇÃO 4: ESTADO DO UPLOAD DE IMAGENS

**Questão crítica:** As 68 imagens foram totalmente processadas pelo servidor?

#### 4.1 — Verificar status de upload
```
document.querySelectorAll('[data-upload-status]')
  .forEach(img => console.log(img.dataset.uploadStatus))
```

Estados possíveis:
- [ ] `pending` — Ainda processando (BLOQUEADOR)
- [ ] `uploading` — Ainda enviando (BLOQUEADOR)
- [ ] `uploaded` — Processamento em servidor (BLOQUEADOR)
- [ ] `complete` — Pronto (OK)
- [ ] `error` — Falha (BLOQUEADOR)

#### 4.2 — Verificar mensagens de erro no upload
```
document.querySelectorAll('[class*="error"], [aria-invalid="true"]')
  .forEach(el => console.log(el.textContent))
```

Procurar por:
- [ ] "Falha no upload"
- [ ] "Imagem inválida"
- [ ] "Formato não suportado"
- [ ] "Tamanho muito grande"
- [ ] "Processamento ainda em andamento"

---

### SEÇÃO 5: LOCALIZAÇÃO — SELEÇÃO vs DIGITAÇÃO

**Questão crítica:** A localização foi SELECIONADA ou apenas DIGITADA?

#### 5.1 — Verificar atributo data-id ou data-fbid
```
document.querySelector('input[aria-label*="localização"]')
  .getAttribute('data-id')
```

Esperado: Um ID numérico ou UUID (indicando seleção de lista validada)
Problema: null ou undefined (indica digitação livre — PODE SER BLOQUEADOR)

#### 5.2 — Verificar estrutura de autocomplete
```
document.querySelector('ul[role="listbox"]') // autocomplete aberto?
document.querySelector('[role="option"][aria-selected="true"]') // seleção confirmada?
```

---

### SEÇÃO 6: BOTÃO "AVANÇAR" — ANÁLISE PROFUNDA

#### 6.1 — Localizar o botão
```javascript
const advanceButton = document.querySelector('button[aria-label*="Avançar"]')
  || document.querySelector('button:contains("Avançar")')
  || document.querySelector('button[type="submit"]')
```

#### 6.2 — Estado do botão
```javascript
{
  disabled: advanceButton.disabled,
  aria_disabled: advanceButton.getAttribute('aria-disabled'),
  class: advanceButton.className,
  style_opacity: advanceButton.style.opacity,
  style_pointer_events: advanceButton.style.pointerEvents,
  style_display: advanceButton.style.display,
  onclick: advanceButton.onclick,
  data_attributes: advanceButton.dataset
}
```

**Qualquer um desses estados pode estar bloqueando:**
- ✓ `disabled=true`
- ✓ `aria-disabled="true"`
- ✓ Class `.is-disabled` ou `.disabled`
- ✓ `opacity: 0.5` ou menor
- ✓ `pointer-events: none`
- ✓ `display: none`
- ✓ onclick retorna false

#### 6.3 — Validação de formulário
```javascript
const form = document.querySelector('form')
const isFormValid = !form.classList.contains('invalid')
  && form.checkValidity()
  && Array.from(form.querySelectorAll('[required]'))
     .every(field => field.value && field.validity.valid)
```

#### 6.4 — Listener do botão
```javascript
advanceButton.addEventListener('click', (e) => {
  console.log({
    defaultPrevented: e.defaultPrevented,
    formValid: advanceButton.form?.checkValidity(),
    error: e.target.getAttribute('aria-invalid')
  })
})
```

---

### SEÇÃO 7: MONITORAR REQUISIÇÕES DE REDE

Durante o preenchimento, interceptar:

#### 7.1 — Validação em tempo real (XHR/Fetch)
```javascript
window.addEventListener('fetch', (e) => {
  console.log({
    url: e.request.url,
    method: e.request.method,
    timestamp: new Date().toISOString()
  })
})
```

Procurar por:
- [ ] `/api/validate/title` — Validando título
- [ ] `/api/validate/description` — Validando descrição
- [ ] `/api/validate/price` — Validando preço
- [ ] `/api/validate/location` — Validando localização
- [ ] `/api/upload/images` — Processando imagens
- [ ] `/api/validate/form` — Validação geral

Se alguma requisição retorna erro (status 400, 422, etc.), esse é o BLOQUEADOR.

#### 7.2 — Respostas de erro
```javascript
fetch(url).then(r => {
  if (!r.ok) console.log({
    status: r.status,
    statusText: r.statusText,
    body: r.json()
  })
})
```

---

### SEÇÃO 8: COMPARAR DOM ANTES E DEPOIS

Capturar snapshots do DOM em diferentes momentos:

#### 8.1 — Antes de preencher
```javascript
const beforeDOM = document.body.innerHTML.substring(0, 5000)
```

#### 8.2 — Depois de preencher primeiro campo
```javascript
const afterFirstField = document.body.innerHTML.substring(0, 5000)
```

#### 8.3 — Depois de preencher todos os campos
```javascript
const afterAll = document.body.innerHTML.substring(0, 5000)
```

**Diferenciais indicam:**
- Validação ocorrendo em tempo real
- Campos adicionais aparecendo/desaparecendo
- Mensagens de erro aparecendo
- Botão mudando de estado

---

### SEÇÃO 9: CONSOLE JAVASCRIPT

Verificar console para:

#### 9.1 — Erros de JavaScript
```
Error: [message]
TypeError: [message]
ReferenceError: [message]
```

Esses podem estar bloqueando a validação do formulário.

#### 9.2 — Avisos de validação
```
Warning: Form validation failed
Warning: Required field missing
Warning: Upload in progress
```

---

## MATRIZ DE DIAGNÓSTICO

| # | Área | Verificação | Bloqueador? | Evidência |
|---|------|-------------|------------|-----------|
| 1 | Categoria | Selecionada e preenchida? | SIM | valor presente |
| 2 | Tipo | Selecionado? | SIM | valor presente |
| 3 | Título | Comprimento 7-120? | SIM | length check |
| 4 | Descrição | Comprimento >25? | SIM | length check |
| 5 | Preço | Número positivo? | SIM | regex + parsing |
| 6 | Localização | Seleção validada (id presente)? | **PROVÁVEL** | data-id check |
| 7 | Imagens | Upload completo? | **PROVÁVEL** | status == "complete" |
| 8 | Imagens | Mínimo 1 imagem? | SIM | count >= 1 |
| 9 | Condicional | Campos adicionais se aluguel? | **PROVÁVEL** | categoria check |
| 10 | Botão | disabled attribute? | **PROVÁVEL** | direct check |

---

## HIPÓTESES MAIS PROVÁVEIS

### Hipótese 1: Localização não validada
A localização foi digitada mas não selecionada da lista de autocomplete. Facebook requer seleção validada.

**Teste:** `document.querySelector('input[aria-label*="localização"]').dataset.id` retorna undefined?

### Hipótese 2: Imagens ainda processando
68 imagens é muito. Alguma pode estar ainda sendo processada pelo servidor.

**Teste:** Algum elemento tem `data-upload-status="uploading"` ou `"uploaded"`?

### Hipótese 3: Campos condicionais obrigatórios
Categoria "Locação de Imóveis" pode exigir campos adicionais (duração, disponibilidade, tipo de ocupação) que não foram preenchidos.

**Teste:** Estão visíveis campos adicionais com `required` e `value=""` ?

### Hipótese 4: Erro JavaScript silencioso
Validador do formulário entrou em erro, impedindo ativação do botão.

**Teste:** Há erros no console? Há `try-catch` capturando exception?

---

## PRÓXIMOS PASSOS

1. ✅ Abrir console JavaScript do navegador (F12)
2. ✅ Executar cada verificação da SEÇÃO 1-9
3. ✅ Compilar FORMULÁRIO_VALIDATION_REPORT.json
4. ✅ Identificar exatamente qual CAMPO e qual CONDIÇÃO estão bloqueando
5. ✅ Gerar FORM_BLOCKED com causa-raiz identificada

**Nenhum clique em Avançar até identificar a causa.**

---

**Auditoria de formulário:** Pendente  
**Objetivo:** Identifcar root cause do bloqueio  
**Status:** Investigação em andamento
