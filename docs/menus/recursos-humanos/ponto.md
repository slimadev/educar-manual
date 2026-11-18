# Ponto

**Menu:** Recursos Humanos › Ponto
**Quem vê:** Gestor de recursos humanos, Director da escola

A assiduidade do pessoal com horário de trabalho: as entradas e as saídas de cada dia, os atrasos e as faltas, e o resumo do mês que vai para a folha de salários. As marcações vêm do relógio biométrico, do [registo digital](../ponto/o-meu-ponto.md) do próprio colaborador ou de uma correcção do RH.

## Antes de começar

1. Crie os **Horários** de trabalho (botão **Horários**): o nome, os dias, a hora de entrada e a de saída, e os minutos de tolerância. Por exemplo, `Secretaria e finanças`, de segunda a sexta, das 07:30 às 15:30, com 10 minutos de tolerância.
2. Na ficha de cada colaborador, em **Dados › Ponto**, escolha o **Horário de trabalho** e, se a escola tem relógio biométrico, o **Número no relógio** (o número do colaborador no relógio). Um colaborador sem horário não controla o ponto.
3. Em [Definições de RH](definicoes-de-rh.md), indique quantas horas de atraso valem uma falta e junte os feriados.

## O dia

Para cada colaborador com horário, no dia escolhido: a **Entrada** (a primeira marcação), a **Saída** (a última), o **Atraso** e a **Situação**:

- **Presente**, ou **Atraso** quando chegou depois da hora de entrada mais a tolerância. O atraso conta desde a hora de entrada.
- **Falta**: um dia de trabalho sem marcações (depois da hora de saída do horário).
- **Falta justificada**, **Folga** (dia sem trabalho no horário), **Feriado**, **Por registar** (o dia ainda não acabou).

Para corrigir:

- **Juntar uma marcação** (o relógio): quando o colaborador se esqueceu de marcar. Indique a hora e o motivo. Só estas marcações se podem apagar.
- **Justificar**: a falta ou o atraso, com o motivo (por exemplo, doença com atestado). A falta ou o atraso justificado não conta para os descontos.

## O mês

![O resumo do mês: faltas, atrasos e faltas por atraso](img/ponto-mes.png)

Em **Mês**: os dias de trabalho, as presenças, as faltas (sem justificação), as justificadas, os atrasos (o tempo e os dias), as **Faltas por atraso** e o **Total de faltas**. Os minutos de atraso somam-se no mês e cada X horas valem uma falta (X nas Definições de RH). O total de faltas é o que desconta no salário.

Clique num colaborador para ver o mês dele, dia a dia, com as marcações e as correcções.

![O mês de um colaborador, com uma falta e uma falta justificada](img/ponto-colaborador.png)

## Importar o relógio biométrico

Com relógio ZKTeco (ou outro que exporte as marcações):

1. Tire as marcações do relógio: o ficheiro `attlog.dat` na pen USB, ou a exportação do software do relógio em CSV ou Excel.
2. Use **Importar o relógio**, escolha o ficheiro e use **Importar**.

Cada marcação é do colaborador com o mesmo **Número no relógio**. Os números sem colaborador aparecem na mensagem: indique-os na ficha e importe outra vez. Pode importar o mesmo ficheiro (ou um que se sobrepõe) as vezes que quiser: as marcações já importadas não se repetem.
