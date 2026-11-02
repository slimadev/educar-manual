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
- Ecrã inteiro de 1440×900 px, com o menu lateral (mostra o menu do perfil que está a usar).

Para ver as capturas que faltam:
```bash
grep -rn "<!-- captura:" docs
```

### Tirar as capturas automaticamente

As capturas tiram-se com `scripts/capturas.py` (Playwright), que entra com cada utilizador de demonstração,
abre o ecrã e grava a imagem; a lista está em `scripts/capturas.json`. Precisa de:

1. A base de demonstração: no repositório da aplicação, `scripts/demo/criar_base_demo.sh` copia a base,
   troca todos os dados pessoais por fictícios e cria um utilizador por perfil (`director`, `pedagogico`,
   `secretaria`, `financeiro`, `funcionario`, `caixa`, `professor`, `aluno`; senha `demo1234`).
2. A aplicação a correr sobre essa base (ex. em `http://127.0.0.1:8099`).
3. `pip install playwright && playwright install chromium`, e `pdftoppm` (poppler) para os documentos PDF.

Os dados de exames fazem-se por etapas com o semeador `scripts/demo/exames` da aplicação; depois de cada
etapa tiram-se as capturas dessa etapa:

```bash
# na aplicação
go run ./scripts/demo/exames -etapa inscricoes -saida /tmp/exames_demo.json
# no manual
python scripts/capturas.py --etapa inscricoes --ids /tmp/exames_demo.json
# ... o mesmo com -etapa em_curso e -etapa fechada
```

Os pedidos de documentos fazem-se de uma vez com `go run ./scripts/demo/documentos -saida /tmp/documentos_demo.json`
(preços, etapas, avisos e pedidos em todos os estados); depois
`python scripts/capturas.py --etapa documentos --ids /tmp/documentos_demo.json`.

O fim do ano (pauta anual) faz-se com `go run ./scripts/demo/ano`, que põe a 1ª Classe A de 2026 com as notas dos três
trimestres; as capturas são as da etapa `ano` (`--ids` com `{"candidato": <id de um candidato por matricular>}`).

A tesouraria faz-se com `go run ./scripts/demo/tesouraria -saida /tmp/tesouraria_demo.json` (uma conta nova, vendas
ao balcão do dia, duas cobranças a turmas com parte paga, duas despesas e uma transferência); as capturas são as da
etapa `tesouraria`, com `--ids /tmp/tesouraria_demo.json`.

Os semeadores não se repetem sobre a mesma base: para refazer tudo, recrie a base e corra-os pela ordem exames
(três etapas), documentos, ano, tesouraria.

`--so <nome>` repete só uma captura (a imagem é substituída; a página já tem a referência).
