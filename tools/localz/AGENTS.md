# AGENTS.md — localz

## Responsabilidade

`localz` gerencia `~/.config/zsh/local.zsh`. Arquivo machine-local, nunca
gerenciado pelo chezmoi.

## Antes de editar

1. Ler o `CLAUDE.md` desta ferramenta.
2. Não expandir `cmd_add` para além de aliases simples.

## Validação obrigatória

```bash
pytest tools/localz/tests/ -v
chezmoi apply
localz --help               # deve imprimir sem erro
localz add TEST_ALIAS 'echo test'
localz list                 # deve mostrar o alias
localz show                 # deve mostrar o conteúdo atualizado
```

Verificar que o arquivo mantém permissão 600:

```bash
stat -f "%Lp" ~/.config/zsh/local.zsh   # deve imprimir: 600
```

## Commits

Usar `fix(localz):` ou `feat(localz):` como prefixo.
