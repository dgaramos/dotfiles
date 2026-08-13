# CLAUDE.md — local-env

## Escopo

`local-env` gerencia variáveis de ambiente machine-local em `~/.config/local-env/env`.
O registro em `~/.config/local-env/names` permite que novos shells limpem variáveis
herdadas antes de carregar o estado atual — essa semântica é central ao funcionamento.

## Linguagem e dependências

Python 3, stdlib apenas. Sem dependências externas.

## Invariantes críticas

- `names` registra **todas** as variáveis que já foram gerenciadas, inclusive as removidas.
  Isso permite que `common.zsh` limpe variáveis herdadas mesmo após um `unset`.
  Nunca remover um nome do registro `names` ao fazer `unset`.

- Os arquivos `env` e `names` têm permissão `600` e o diretório `700`.
  `ensure_storage` reaplica isso a cada operação — manter esse comportamento.

- `write_vars` usa `shlex.quote` para escapar valores. Nunca escrever valores
  sem escape no arquivo.

## O que não mudar

- O formato `export NAME=VALUE` no arquivo `env` — `common.zsh` depende disso.
- O comportamento de `cmd_edit`: após edição manual, sincroniza `names` com as
  variáveis presentes no arquivo para não perder nomes introduzidos manualmente.

## Validação

```bash
local-env set TEST_LOCAL_ENV "hello world"
exec zsh && echo "$TEST_LOCAL_ENV"   # → hello world

local-env unset TEST_LOCAL_ENV
exec zsh && echo "${TEST_LOCAL_ENV:-<unset>}"  # → <unset>
```
