# CLAUDE.md — sshm

## Escopo

`sshm` gerencia `~/.ssh/config` — lê, escreve e preserva blocos de host existentes.
Não gerencia chaves em si além de copiar `.pem` para `~/.ssh/` e ajustar permissões.

## Linguagem e dependências

Python 3, stdlib apenas. Sem dependências externas.

## Padrões de código

### Menus interativos

Qualquer seleção de lista usa `select_interactive`. Nunca usar menus numerados.

```python
chosen = select_interactive(
    options,
    prompt="Label:",
    allow_custom=True,
    custom_label="informar caminho...",
)
if chosen is CUSTOM_SENTINEL:
    value = input("Caminho: ").strip()
else:
    value = chosen
```

### Parser de ~/.ssh/config

O parser preserva comentários e formatação existentes. Nunca reescrever o arquivo
inteiro a partir do zero — sempre usar `write_config(blocks)` com os blocos parseados.

### Chaves .pem

`install_pem` é idempotente: se o arquivo já está em `~/.ssh/`, apenas ajusta
as permissões sem duplicar. Manter esse comportamento em qualquer mudança.

## O que não mudar

- O formato de escrita do `~/.ssh/config` — indentação com 4 espaços por opção.
- O comportamento de `IdentitiesOnly yes` — sempre adicionado junto com `IdentityFile`.
- A detecção de host duplicado antes de escrever.

## Validação

Após mudanças:
1. `chezmoi apply` na máquina local
2. `sshm list` — verificar que hosts existentes continuam listados
3. `sshm add` com um host novo — confirmar que o arquivo é escrito corretamente
