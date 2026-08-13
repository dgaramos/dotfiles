# CLAUDE.md — localz

## Escopo

`localz` gerencia `~/.config/zsh/local.zsh` — arquivo machine-local de configuração
shell. Nunca gerenciado pelo chezmoi.

## Linguagem e dependências

Python 3, stdlib apenas. Sem dependências externas.

## Padrões de código

- `ensure_file` cria o arquivo com header explicativo se não existir. Manter o header.
- `cmd_add` verifica duplicatas antes de escrever. Manter essa verificação.
- O arquivo é aberto em modo append (`"a"`) — nunca reescrever o arquivo inteiro
  ao adicionar um alias.

## Limites intencionais

`localz add` só adiciona aliases simples. Funções e configurações mais complexas
devem ser adicionadas via `localz edit`. Não expandir `cmd_add` para suportar
funções — a complexidade não justifica.

## O que não mudar

- Permissão `600` no arquivo criado por `ensure_file`.
- O formato `alias NAME='CMD'` ao escrever (aspas simples).
