# local-env — Machine-local Environment Variables

Gerencia variáveis de ambiente específicas de cada máquina, fora do controle do chezmoi.
Instalado em `~/.local/bin/local-env`.

## Comandos

```
local-env set NAME VALUE   define uma variável
local-env unset NAME       remove uma variável
local-env get NAME         imprime o valor atual
local-env list             lista todas as variáveis configuradas
local-env path             imprime o caminho do arquivo de estado
local-env edit             abre o arquivo de estado no $EDITOR
```

## Como funciona

As variáveis são persistidas em `~/.config/local-env/env` (formato `export NAME=VALUE`).
Um registro interno em `~/.config/local-env/names` permite que novos shells limpem
variáveis herdadas antes de carregar o estado atual.

`common.zsh` carrega esses arquivos automaticamente em cada shell.

## Exemplo

```bash
local-env set MY_TOKEN "abc123"
exec zsh
echo $MY_TOKEN  # → abc123

local-env unset MY_TOKEN
exec zsh
echo ${MY_TOKEN:-<unset>}  # → <unset>
```

## Instalação via chezmoi

O executável fica em `tools/local-env/bin/local-env` no repositório e é instalado por
`run_onchange_install-tools.sh.tmpl` em `~/.local/bin/local-env`.

Os arquivos de estado (`env`, `names`) são locais e nunca gerenciados pelo chezmoi.
