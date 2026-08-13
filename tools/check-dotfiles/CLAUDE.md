# CLAUDE.md — check-dotfiles

## Escopo

`check-dotfiles` escaneia o repositório de dotfiles antes de cada commit.
É um scanner conservador: bloqueia com alta confiança, avisa com baixa confiança.
Falsos positivos são suprimidos com `# check-dotfiles: ignore` na linha.

## Linguagem e dependências

Python 3, stdlib apenas. Sem dependências externas.

## Padrões de código

### Adicionando um novo padrão de bloqueio

Adicionar a `BLOCK_PATTERNS` com tupla `(slug, regex_compilado, descrição_humana)`.
Testar contra falsos positivos comuns antes de adicionar.

### Adicionando um novo padrão de aviso

Adicionar a `WARN_PATTERNS` com o mesmo formato.

### Adicionando um novo comando instalado pelo repo

Adicionar o nome do binário a `REPO_INSTALLED`. Isso evita falso positivo de
"uninstalled-alias" para aliases que referenciam a nova ferramenta.

### Adicionando um novo serviço externo bloqueado

Adicionar ao padrão regex em `EXTERNAL_SERVICE_RE`. Usar grupo não-capturante
quando necessário para evitar conflitos com o grupo `\1` usado na mensagem de erro.

## O que não mudar

- O código de saída: `sys.exit(1)` apenas quando há bloqueios, nunca por avisos.
- O marcador `# check-dotfiles: ignore` — está documentado no README e no AGENTS.md.
- A lógica de `inside_guard`: aliases dentro de `if command -v ... fi` não geram
  aviso de "uninstalled-alias" pois já estão devidamente guardados.

## Validação

```bash
check-dotfiles --staged    # no pre-commit hook
check-dotfiles --all       # varredura completa
```

Sempre rodar `--all` após adicionar novos padrões para verificar falsos positivos
no próprio repositório.
