# Dotfiles

Configuração centralizada de shell e ambiente usando [chezmoi](https://www.chezmoi.io/) e Git.

O repositório é a fonte da verdade para configurações compartilhadas entre máquinas pessoais, homelab, Steam Deck e máquinas de trabalho.

## Arquitetura

```text
Gitea / dotfiles
        │
        ├── Personal Mac
        │     profile = personal
        │     role    = mac
        │
        ├── Homelab
        │     profile = personal
        │     role    = homelab
        │
        ├── Steam Deck
        │     profile = personal
        │     role    = steamdeck
        │
        └── Work Mac
              profile = work
              role    = work-mac
```

Cada máquina recebe a configuração comum e apenas as configurações específicas do seu perfil e role.

## Estrutura

```text
.
├── .chezmoi.toml.tmpl
├── .chezmoiscripts/
│   └── run_once_install-zsh-plugins.sh.tmpl
├── dot_zshrc.tmpl
└── private_dot_config/
    └── zsh/
        ├── common.zsh
        ├── personal.zsh
        ├── work.zsh
        └── hosts/
            ├── mac.zsh
            ├── work-mac.zsh
            ├── homelab.zsh
            └── steamdeck.zsh
```

## Perfis e roles

| Máquina | Profile | Role |
|---|---|---|
| Personal Mac | `personal` | `mac` |
| Homelab | `personal` | `homelab` |
| Steam Deck | `personal` | `steamdeck` |
| Work Mac | `work` | `work-mac` |

## Configuração compartilhada

### `common.zsh`

Configuração carregada por todas as máquinas.

Atualmente contém:

- histórico do Zsh;
- aliases de navegação;
- aliases Git;
- aliases do chezmoi;
- prompt com `user@hostname`;
- integração opcional com `eza`;
- integração opcional com `bat`;
- carregamento opcional do FZF.

As integrações opcionais só são ativadas quando a ferramenta existe na máquina.

### `personal.zsh`

Configurações compartilhadas apenas entre máquinas pessoais.

Não deve conter secrets.

### `work.zsh`

Configurações compartilhadas entre máquinas de trabalho.

Não deve conter credenciais corporativas ou informações específicas de uma empresa.

## Configurações por host

### `hosts/mac.zsh`

Configuração do Mac pessoal.

Inclui configurações relacionadas a:

- Homebrew;
- IntelliJ IDEA CE;
- SDKMAN;
- Java.

### `hosts/work-mac.zsh`

Configuração de Macs de trabalho.

Inclui:

- Homebrew;
- IntelliJ IDEA;
- libpq;
- NVM;
- Java 17 como default;
- Java 21;
- função `usejdk17`;
- função `usejdk21`;
- helpers para exportar e remover temporariamente o token do GitHub.

### `hosts/homelab.zsh`

Configuração específica do homelab.

Inclui aliases para:

- Docker;
- Docker Compose;
- storage;
- diretório de stacks.

### `hosts/steamdeck.zsh`

Configuração específica do Steam Deck.

Inclui atalhos condicionais para:

- Emulation;
- ROMs;
- BIOS;
- Decky.

## Como o `.zshrc` é montado

O arquivo `dot_zshrc.tmpl` é um template do chezmoi.

Uma máquina com:

```text
profile = personal
role = homelab
```

gera um `.zshrc` que carrega:

```sh
source "$HOME/.config/zsh/common.zsh"
source "$HOME/.config/zsh/personal.zsh"
source "$HOME/.config/zsh/hosts/homelab.zsh"
```

Uma máquina de trabalho usa:

```sh
source "$HOME/.config/zsh/common.zsh"
source "$HOME/.config/zsh/work.zsh"
source "$HOME/.config/zsh/hosts/work-mac.zsh"
```

Todos os arquivos de host podem existir em `~/.config/zsh/hosts`, mas apenas o arquivo correspondente ao role da máquina é carregado.

## Pré-requisitos do shell

A configuração atual assume que **Zsh e Oh My Zsh já estão instalados**.

O bootstrap do chezmoi instala automaticamente os plugins adicionais usados pela configuração, mas não instala o Oh My Zsh.

Antes de aplicar os dotfiles em uma máquina nova, confirme:

```sh
zsh --version
test -d ~/.oh-my-zsh && echo "Oh My Zsh instalado"
```

O diretório esperado é:

```text
~/.oh-my-zsh
```

## Comandos principais

### Ver diferenças

```sh
chezmoi diff
```

Alias:

```sh
czd
```

Nenhuma saída significa que o estado atual da máquina corresponde ao estado desejado pelo chezmoi.

### Aplicar alterações

```sh
chezmoi apply
```

Alias:

```sh
cza
```

### Atualizar uma máquina

```sh
chezmoi update
```

Alias:

```sh
czu
```

Nas máquinas consumidoras, esse é o comando normal para receber alterações publicadas no repositório.

Ele:

1. atualiza a source local;
2. processa os templates;
3. aplica as alterações na máquina.

### Ver estado

```sh
chezmoi status
```

Nenhuma saída normalmente significa que não existe drift entre o estado gerenciado e a máquina.

### Editar um arquivo gerenciado

Exemplo:

```sh
chezmoi edit ~/.zshrc
```

Alias:

```sh
cze ~/.zshrc
```

### Ver a source

```sh
chezmoi source-path
```

Normalmente:

```text
~/.local/share/chezmoi
```

Para entrar nela:

```sh
cd "$(chezmoi source-path)"
```

## Fluxo de desenvolvimento

O Mac pessoal é normalmente usado como máquina autora.

O fluxo é:

```text
editar source
      ↓
chezmoi diff
      ↓
chezmoi apply
      ↓
git commit
      ↓
git push
      ↓
czu nas outras máquinas
```

Exemplo:

```sh
cd "$(chezmoi source-path)"
```

Edite o arquivo desejado.

Depois:

```sh
chezmoi diff
chezmoi apply
```

Publique:

```sh
git add -A
git commit -m "describe the change"
git push
```

Nas outras máquinas:

```sh
czu
```

## Bootstrap de uma nova máquina

### 1. Instalar Zsh e Oh My Zsh

Confirme primeiro que ambos estão disponíveis.

```sh
zsh --version
test -d ~/.oh-my-zsh && echo "Oh My Zsh instalado"
```

### 2. Instalar chezmoi

#### macOS

```sh
brew install chezmoi
```

#### Linux ou Steam Deck

```sh
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin
```

Confirme:

```sh
chezmoi --version
```

## Acesso SSH ao Gitea

Cada máquina deve possuir sua própria chave SSH.

Nunca copie a chave privada de uma máquina para outra apenas para acessar o repositório.

Se a máquina ainda não tiver uma chave:

```sh
ssh-keygen -t ed25519
```

A chave pública:

```text
~/.ssh/id_ed25519.pub
```

deve ser cadastrada no Gitea.

Exemplo de configuração em `~/.ssh/config`:

```sshconfig
Host gitea
    HostName 192.168.15.50
    Port 222
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

Teste:

```sh
ssh -T gitea
```

Uma autenticação válida deve retornar uma mensagem do Gitea indicando que a chave foi reconhecida.

O host `gitea` aponta para a instância privada no homelab. A máquina precisa ter conectividade com essa rede para clonar ou atualizar o repositório.

## Inicializar chezmoi

Com SSH funcionando:

```sh
chezmoi init gitea:dgaramos/dotfiles.git
```

O bootstrap solicita:

```text
Profile (personal/work)?
Role (mac/work-mac/homelab/steamdeck)?
```

### Personal Mac

```text
profile = personal
role = mac
```

### Homelab

```text
profile = personal
role = homelab
```

### Steam Deck

```text
profile = personal
role = steamdeck
```

### Work Mac

```text
profile = work
role = work-mac
```

Antes da primeira aplicação:

```sh
chezmoi diff
```

Revise as mudanças.

Depois:

```sh
chezmoi apply
exec zsh
```

Confirme:

```sh
chezmoi status
```

## Mudanças no template de configuração

O arquivo `.chezmoi.toml.tmpl` é usado para gerar a configuração local de cada máquina.

Se ele mudar, um `chezmoi update` pode emitir:

```text
warning: config file template has changed, run chezmoi init to regenerate config file
```

Nesse caso:

```sh
chezmoi init
```

Depois:

```sh
chezmoi status
```

O `chezmoi init` reaproveita os valores locais já configurados quando possível.

## Zsh plugins

O bootstrap instala automaticamente:

```text
zsh-autosuggestions
zsh-syntax-highlighting
```

em:

```text
~/.oh-my-zsh/custom/plugins/
```

O `zsh-autosuggestions` é carregado pelo Oh My Zsh.

O `zsh-syntax-highlighting` é carregado explicitamente no final do `.zshrc`.

## Ferramentas opcionais

O `common.zsh` detecta algumas ferramentas automaticamente.

### eza

Se `eza` estiver instalado:

```sh
ls
ll
la
tree
```

passam a usar `eza`.

### bat

Se `bat` estiver instalado:

```sh
cat
```

passa a usar `bat`.

### FZF

Se existir:

```text
~/.fzf.zsh
```

ele é carregado automaticamente.

Máquinas sem essas ferramentas continuam funcionando normalmente.

## Java no Work Mac

Java 17 é o default.

```sh
java -version
echo "$JAVA_HOME"
```

Para usar Java 21 no shell atual:

```sh
usejdk21
```

Para voltar ao Java 17:

```sh
usejdk17
```

As funções alteram `JAVA_HOME` e o `PATH` apenas no shell atual.

Abrir um novo shell volta ao default configurado.

## GitHub token no Work Mac

O token do GitHub não é exportado automaticamente.

Quando necessário:

```sh
github-token
```

Isso executa:

```sh
gh auth token
```

e exporta o resultado como `AUTH_TOKEN` no shell atual.

Para remover:

```sh
github-token-clear
```

Nenhum token deve ser armazenado neste repositório.

## Segurança

Nunca versionar:

- chaves SSH privadas;
- API tokens;
- GitHub tokens;
- Gitea tokens;
- senhas;
- cookies;
- credenciais corporativas;
- arquivos `.env` contendo secrets;
- certificados ou arquivos de autenticação privados.

O repositório deve conter **configuração**, não credenciais.

Chaves públicas e configurações sem segredo podem ser versionadas quando fizer sentido.

## Gitea e acesso remoto

O Gitea é a source remota principal dos dotfiles.

O acesso Git usa:

```text
gitea:dgaramos/dotfiles.git
```

com o alias SSH:

```text
gitea
```

O endpoint SSH do Gitea está disponível na porta:

```text
222
```

O endpoint web/API utiliza:

```text
3005
```

A dependência de rede deve ser considerada ao usar `czu` fora da rede onde o homelab está acessível.

## Estado esperado

Depois de sincronizar uma máquina:

```sh
chezmoi status
```

não deve produzir saída.

Da mesma forma:

```sh
chezmoi diff
```

não deve produzir saída quando os arquivos locais já correspondem ao estado desejado.

## Regra prática

### Alterando configuração

```text
Mac autor
   │
   ├── editar source
   ├── chezmoi diff
   ├── chezmoi apply
   ├── git commit
   └── git push
             │
             ▼
           Gitea
             │
             ▼
       outras máquinas
             │
             └── czu
```

### Atualizando uma máquina

Na maioria dos casos:

```sh
czu
```

Depois, se necessário:

```sh
exec zsh
```

Se o template de configuração tiver mudado:

```sh
chezmoi init
```

## Resumo

O objetivo deste repositório é permitir que uma máquina nova possa reconstruir o ambiente de shell com o mínimo possível de configuração manual, mantendo:

- configuração comum centralizada;
- diferenças entre ambientes pessoais e de trabalho;
- configuração específica de cada tipo de máquina;
- nenhum secret no Git;
- atualização simples através do chezmoi.