# check-dotfiles — Secret Scanner

Escaneia o repositório de dotfiles em busca de segredos, IPs privados, hostnames de
infraestrutura e aliases referenciando serviços externos não instalados pelo repo.
Instalado em `~/.local/bin/check-dotfiles` e configurado como pre-commit hook.

## Comandos

```
check-dotfiles --staged   escaneia arquivos staged (usado pelo hook pre-commit)
check-dotfiles --all      escaneia todos os arquivos rastreados pelo git
check-dotfiles FILE       escaneia arquivo(s) específico(s)
```

## O que bloqueia (commit abortado)

- Chaves privadas (`-----BEGIN ... PRIVATE KEY`)
- AWS access keys (`AKIA...`)
- GitHub tokens (`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`)
- Assignments genéricos de senha/token/secret
- Hostnames EC2 públicos (`ec2-*.compute.amazonaws.com`)
- Aliases referenciando serviços externos (open-webui, nginx, etc.)

## O que avisa (commit permitido)

- Endereços IPv4 (exceto loopback e documentação)
- Aliases com comandos não instalados por este repositório

## Suprimindo falsos positivos

Adicione `# check-dotfiles: ignore` ao final da linha.

## Adicionando novos comandos instalados pelo repo

Atualize `REPO_INSTALLED` no início do script para que aliases referenciando
o novo comando não gerem aviso.

## Instalação via chezmoi

O executável fica em `tools/check-dotfiles/bin/check-dotfiles` no repositório e é
instalado por `run_onchange_install-tools.sh.tmpl` em `~/.local/bin/check-dotfiles`.

O hook pre-commit é instalado por `run_onchange_install-git-hooks.sh.tmpl`.
