# Dotfiles

Configuração centralizada de ambiente usando chezmoi.

O objetivo deste repositório é manter um ambiente consistente entre
máquinas, separando configurações pessoais, profissionais e específicas
de hardware.

## Filosofia

- Uma única fonte da verdade para configurações de shell
- Instalação automatizada de ferramentas
- Configurações portáveis entre macOS e Linux
- Separação por perfil e máquina

## Máquinas suportadas

### macOS pessoal

Profile:

    profile: personal
    role: mac

### macOS trabalho

Profile:

    profile: work
    role: mac

Inclui ferramentas de desenvolvimento como SDKMAN, Java e NVM.

### Raspberry Pi

Ambiente Debian/Linux.

Compatibilidades: - fd → fdfind - bat → batcat

### Steam Deck

Ambiente SteamOS/Arch Linux.

Antes de instalar pacotes:

      ``` bash
      sudo steamos-readonly disable
      ```

## Ferramentas instaladas

### Shell

- zsh-autosuggestions
- zsh-syntax-highlighting
- zsh-history-substring-search

### Navegação

- zoxide
- fzf

### Busca

- ripgrep
- fd

Aliases:

    ff     -> fd/fdfind
    rgrep  -> ripgrep

### Visualização

- bat
- eza

Aliases:

    cat   -> bat/batcat
    ll    -> eza -lah
    tree  -> eza --tree

### Git

- delta

Configurações: - pager delta - diff side-by-side - navegação

### Desenvolvimento

- direnv
- SDKMAN
- NVM

## Estrutura

    .
    ├── dot_zshrc.tmpl
    ├── private_dot_config/
    │   └── zsh/
    │       ├── common.zsh
    │       ├── personal.zsh
    │       ├── work.zsh
    │       └── hosts/
    └── .chezmoiscripts/

## Uso

Aplicar configurações:

      ``` bash
      chezmoi apply
      ```

Recarregar shell:

      ``` bash
      exec zsh
      ```

Ver alterações:

      ``` bash
      chezmoi diff
      ```

Ver estado:

      ``` bash
      chezmoi status
      ```

## Bootstrap

Scripts automáticos:

- instalação de plugins ZSH
- instalação de ferramentas CLI
- adaptação por sistema operacional

Suportados:

- Homebrew
- apt
- pacman

## Próximos passos

- Melhorar documentação de bootstrap
- Revisar publicação no GitHub
- Adicionar mais automações de desenvolvimento
