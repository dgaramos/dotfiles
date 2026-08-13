# AGENTS.md — local-env

## Responsabilidade

`local-env` é carregado por todo shell novo via `common.zsh`. Bugs aqui afetam
a inicialização de todos os shells na máquina.

## Antes de editar

1. Ler o `CLAUDE.md` desta ferramenta — especialmente as invariantes críticas.
2. Nunca remover um nome do registro `names` ao fazer `unset`.
3. Nunca escrever valores sem `shlex.quote` no arquivo `env`.

## Validação obrigatória

```bash
pytest tools/local-env/tests/ -v
chezmoi apply

local-env set TEST_LOCAL_ENV "hello world"
exec zsh
echo "$TEST_LOCAL_ENV"                      # deve imprimir: hello world

local-env unset TEST_LOCAL_ENV
exec zsh
echo "${TEST_LOCAL_ENV:-<unset>}"           # deve imprimir: <unset>
```

O segundo `exec zsh` valida que o nome foi registrado em `names` e a variável
é limpa mesmo estando no ambiente herdado.

## Commits

Usar `fix(local-env):` ou `feat(local-env):` como prefixo.
