# AGENTS.md — sshm

## Responsabilidade

`sshm` lê e escreve `~/.ssh/config`. Mudanças incorretas podem quebrar todas as
conexões SSH da máquina. Testar com cuidado antes de commitar.

## Antes de editar

1. Ler o `CLAUDE.md` desta ferramenta.
2. Entender o parser de `~/.ssh/config` — ele preserva comentários e formatação.
3. Nunca introduzir menus numerados — usar `select_interactive`.

## Validação obrigatória

Após qualquer mudança:

```bash
chezmoi apply
sshm list           # hosts existentes devem continuar aparecendo
sshm --help         # help deve imprimir sem erro
```

Para mudanças no `sshm add`:

```bash
sshm add            # completar o fluxo com um host de teste
sshm list           # confirmar que o host foi adicionado
# inspecionar ~/.ssh/config manualmente para verificar formatação
```

## Dependências

- `tty`, `termios` (stdlib) — usados pelo `select_interactive`
- `ssh-keygen` (sistema) — usado por `sshm copy-id` com `.pem`
- `ssh-copy-id` (sistema) — usado por `sshm copy-id` com chave normal

## Commits

Usar `fix(sshm):` ou `feat(sshm):` como prefixo conforme o tipo de mudança.
