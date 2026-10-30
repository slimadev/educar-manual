# Pesquisar Turma

**Menu:** Matrícula e Turmas › Pesquisar Turma
**Quem vê:** Chefe da secretaria, Director da escola, Director pedagógico

Encontrar uma turma ou um aluno, e abrir a ficha do aluno.

## Pesquisar

1. Escolha o **Ano lectivo**, a **Classe** e o **Regime**. A **Turma** é opcional.
2. Use **Pesquisar**.

![Pesquisar turma](img/pesquisar-turma.png)

Os botões **Turma A**, **Turma B**… filtram a lista por turma, com o número de alunos. A caixa de pesquisa procura pelo nome, n.º de processo, código ou secção. **Com contas em atraso** mostra só os alunos com contas por pagar fora do prazo.

Cada linha mostra o número do aluno na turma, o processo, o código, a turma, o estado da matrícula e as contas por pagar. Clique no aluno para abrir a ficha.

## Ficha do aluno

O topo mostra os dados do aluno e o resumo das contas: por pagar, em atraso, valor por pagar e total pago. Os separadores:

| Separador | Para quê |
|---|---|
| **Dados gerais** | Dados pessoais e da matrícula; o lápis **Editar** altera-os |
| **Contas por pagar** | Seleccionar contas e registar o pagamento |
| **Pagamentos** | Pagamentos feitos, com o recibo |
| **Documentos** | Pedidos de documentos do aluno (veja [Pedidos de documentos](../documentos/pedidos-de-documentos.md#registar-um-pedido)) |
| **Situação pedagógica** | Médias dos trimestres e fecho do ano do aluno |

![A conta do documento na ficha do aluno](../documentos/img/ficha-pagar.png)

### Registar um pagamento

1. No separador **Contas por pagar**, marque as contas que o aluno vai pagar. A multa das contas em atraso soma-se sozinha.
2. Em **Registar pagamento**, escolha a conta de entrada, escreva a referência (talão, transferência…) e a data do pagamento.
3. Use **Registar pagamento**. O recibo fica disponível.

Os botões no topo da ficha:

- **Turma** volta à turma;
- **Editar matrícula** altera a classe, a turma e o número, a secção, a bolsa, a modalidade de pagamento e o encarregado;
- **Extracto** mostra o extracto das contas do aluno, para imprimir;
- **Renovar matrícula** aparece no período de renovação.

Estes botões dependem do perfil: as finanças vêem a ficha para receber pagamentos, mas não alteram a matrícula.

### Renovar a matrícula

Dentro do período de renovação ([Calendário Académico](../configuracoes/calendario-academico.md)), use **Renovar matrícula** na ficha do aluno.

1. Confirme o regime, a modalidade de pagamento e a bolsa ou desconto.
2. Use **Salvar**.
3. Registe o pagamento da renovação em **Contas por pagar**.

## Horário da turma

Com uma turma escolhida, o separador **Horário** mostra o horário da turma.

1. Escolha o **Período de aula** da turma (o turno, de [Períodos Leccionados](../configuracoes/periodos-leccionados.md)).
2. Clique num tempo para escolher ou trocar a disciplina e o professor. O professor não pode ter duas aulas ao mesmo tempo: o horário avisa se tiver aula noutra turma nesse tempo.
3. Escolha o **Director de turma** e o **Chefe de turma**.

!!! warning "Mudar o período"
    Ao mudar o período de aulas da turma, o horário tem de ser refeito.

O resumo dos horários de todas as turmas está em [Configurações › Professores por Turma](../configuracoes/professores-por-turma.md).
