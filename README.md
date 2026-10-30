# Manual do EDUCAR

Manual de uso do EDUCAR para as escolas, ecrã a ecrã, com capturas de ecrã. Feito com [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) e publicado no GitHub Pages.

## Ver localmente

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000
```

`mkdocs build --strict` falha se houver ligações partidas. O GitHub corre-o antes de publicar.

## Organização

```
docs/
  index.md                 início
  primeiros-passos/        entrar, avisos, a app
  perfis/                  um índice por perfil (só ligações, sem conteúdo repetido)
  processos/               tarefas que passam por vários menus (ex. exames)
  menus/<menu>/<ecrã>.md   uma página por item de menu do EDUCAR
  menus/<menu>/img/        as capturas desse menu
```

Cada ecrã é explicado **uma só vez**, na página do seu menu. Os perfis e os processos apontam para lá. O menu lateral (`nav` em `mkdocs.yml`) segue a ordem dos menus do sistema.

## Escrever uma página

- Comece com o menu e quem vê o ecrã:
  ```
  **Menu:** Exames › Inscrições
  **Quem vê:** Chefe da secretaria, …
  ```
- Explique para que serve e depois o passo a passo, com os nomes dos botões em **negrito**, tal como aparecem no ecrã.
- Escreva em português de Moçambique, no singular dirigido ao utilizador ("Escolha…", "Use…").
- Use `!!! note`, `!!! tip` ou `!!! warning` para avisos.
- Uma página ainda por escrever tem o aviso "Em preparação".

## Capturas de ecrã

- **Nunca usar dados reais.** As capturas tiram-se numa escola de demonstração, com nomes, contactos e valores fictícios.
- O lugar de cada captura está marcado na página com um comentário:
  ```
  <!-- captura: menus/exames/img/inscricoes-sessao.png | rota /exams/registrations/{id} | perfil Secretaria -->
  ```
  Ao tirar a captura, grave o PNG no caminho indicado e substitua o comentário por:
  ```
  ![Inscrições de uma sessão](img/inscricoes-sessao.png)
  ```
- Largura de 1440 px, só a área de conteúdo (sem o menu lateral, salvo quando o menu é o assunto).

Para ver as capturas que faltam:
```bash
grep -rn "<!-- captura:" docs
```
