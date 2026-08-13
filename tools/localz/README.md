# localz — Local Shell Manager

Gerencia `~/.config/zsh/local.zsh`, o arquivo de configuração shell local de cada máquina.
Instalado em `~/.local/bin/localz`.

## Comandos

```
localz edit           abre local.zsh no $EDITOR
localz show           imprime o conteúdo de local.zsh
localz list           lista aliases e funções definidas em local.zsh
localz add NAME CMD   adiciona um alias ao final de local.zsh
```

## Quando usar

Use `localz` para configurações shell que são específicas de uma máquina e não devem
entrar no repositório — aliases para serviços locais, caminhos específicos, etc.

Para variáveis de ambiente, prefira `local-env`.

## Exemplo

```bash
localz add myapp 'docker compose -f ~/projects/myapp/docker-compose.yml'
localz list
# ALIASES
#   myapp  docker compose -f ~/projects/myapp/docker-compose.yml
```

## Instalação via chezmoi

O executável fica em `tools/localz/bin/localz` no repositório e é instalado por
`run_onchange_install-tools.sh.tmpl` em `~/.local/bin/localz`.

`~/.config/zsh/local.zsh` é local e nunca gerenciado pelo chezmoi.
