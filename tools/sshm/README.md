# sshm — SSH Manager

CLI para gerenciar hosts SSH. Instalado em `~/.local/bin/sshm` via chezmoi.

## Comandos

```
sshm list                  lista hosts configurados em ~/.ssh/config
sshm add                   wizard interativo para adicionar um novo host
sshm edit                  abre ~/.ssh/config no $EDITOR
sshm copy-id <host>        copia a chave pública para o servidor
sshm keygen                wizard para gerar um novo par de chaves
```

## sshm add

Fluxo interativo com seleção por arrow keys:

```
Nome do host (alias): meu-servidor
Endereço (IP ou hostname): 10.0.0.1
Usuário [ec2-user]:
Porta [22]:

Chave SSH:
  > id_ed25519
    minha-chave.pem
    [ informar caminho... ]
```

A última opção permite digitar o caminho de um `.pem` em qualquer lugar do sistema. Se ele ainda não estiver em `~/.ssh/`, é copiado e recebe `chmod 400`.

## Chaves .pem

- `.pem` fora de `~/.ssh/` → copiado para `~/.ssh/` com permissão 400
- `.pem` já em `~/.ssh/` → apenas confirma permissão 400, sem duplicar
- `sshm copy-id` com `.pem` → deriva a chave pública via `ssh-keygen -y -f`

## Instalação via chezmoi

O executável fica em `tools/sshm/bin/sshm` no repositório e é instalado por
`run_onchange_install-tools.sh.tmpl` em `~/.local/bin/sshm`.
