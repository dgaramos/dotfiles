# AGENTS.md — check-dotfiles

## Responsabilidade

`check-dotfiles` roda como pre-commit hook em todo commit neste repositório.
Falsos positivos bloqueiam commits legítimos. Falsos negativos deixam segredos
passarem. Testar os dois lados ao modificar padrões.

## Antes de editar

1. Ler o `CLAUDE.md` desta ferramenta.
2. Ao adicionar padrão de bloqueio: testar contra o próprio repo com `--all`.
3. Ao adicionar comando a `REPO_INSTALLED`: verificar que o nome do binário está correto.

## Validação obrigatória

Após qualquer mudança:

```bash
pytest tools/check-dotfiles/tests/ -v
chezmoi apply
check-dotfiles --all        # não deve ter falsos positivos no repo
```

Para novos padrões de bloqueio, adicionar um teste em `tests/test_block_patterns.py`
com `# check-dotfiles: ignore` na linha do padrão de teste. Não testar apenas
manualmente — o padrão precisa ter cobertura na suite.

## Suprimindo falsos positivos no repo

Adicionar `# check-dotfiles: ignore` à linha — nunca enfraquecer o padrão
para contornar um caso específico.

## Commits

Usar `fix(check-dotfiles):` ou `feat(check-dotfiles):` como prefixo.
