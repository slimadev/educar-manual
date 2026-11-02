#!/usr/bin/env bash
# Reconstrói a base de demonstração, corre os semeadores e tira todas as capturas do manual.
#
#   TRABALHO=/tmp/manual PYTHON=.venv/bin/python scripts/refazer.sh
#
# ZIWA é o repositório da aplicação (por omissão ../ziwa); a aplicação fica a correr na porta 8099 no fim.
set -euo pipefail
M=$(cd "$(dirname "$0")/.." && pwd)
Z=$(cd "${ZIWA:-$M/../ziwa}" && pwd)
T=${TRABALHO:-/tmp/educar-manual}
PY=$(realpath -s "${PYTHON:-$M/.venv/bin/python}") # -s: sem seguir o atalho, senão perde o ambiente virtual
mkdir -p "$T/run"
: > "$T/semeadores.log"
ln -sfn "$Z/handler/web/templates/static" "$T/run/static"
ln -sfn "$Z/resources" "$T/run/resources"

pkill -x educar-web || true
sleep 1
cd "$Z"
scripts/demo/criar_base_demo.sh | grep pronta
go build -o "$T/educar-web" ./cmd/web
set -a; . "$Z/.env"; set +a
(cd "$T/run" && DB_HOST=127.0.0.1 DB_PORT=5432 DB_NAME=educar_demo REDIS_ADDR=127.0.0.1:6379 HTTP_PORT=8099 \
  HTTP_URL=127.0.0.1 HTTP_ALLOWED_ORIGINS=127.0.0.1 SMTP_HOST=smtp.exemplo.co.mz SMTP_FROM=avisos@escola-demo.co.mz \
  nohup "$T/educar-web" > "$T/web.log" 2>&1 < /dev/null &)
for _ in $(seq 30); do curl -s -o /dev/null http://127.0.0.1:8099/ && break; sleep 1; done
export DEMO_DB_URL="postgres://$DB_USER:$DB_PASSWORD@127.0.0.1:5432/educar_demo"

semear() { (cd "$Z" && go run "./scripts/demo/$1" "${@:2}" >> "$T/semeadores.log" 2>&1) && echo "semeador $*: ok"; }
capturar() { echo "capturas: $(cd "$M" && "$PY" scripts/capturas.py "$@" | wc -l)"; }

rm -f "$T/exames_demo.json"
for etapa in inscricoes em_curso fechada; do
  semear exames -etapa "$etapa" -saida "$T/exames_demo.json"
  capturar --etapa "$etapa" --ids "$T/exames_demo.json"
done
semear documentos -saida "$T/documentos_demo.json"
capturar --etapa documentos --ids "$T/documentos_demo.json"
semear ano
C=$(PGPASSWORD=$DB_PASSWORD psql -h 127.0.0.1 -U "$DB_USER" educar_demo -At -c "select id from students_candidates where not is_enrolled order by id desc limit 1")
echo "{\"candidato\": $C}" > "$T/ano_demo.json"
capturar --etapa ano --ids "$T/ano_demo.json"
semear tesouraria -saida "$T/tesouraria_demo.json"
capturar --etapa tesouraria --ids "$T/tesouraria_demo.json"
semear rh -saida "$T/rh_demo.json"
capturar --etapa rh --ids "$T/rh_demo.json"
# a 1ª Classe A de 2026 e o seu primeiro aluno, para os relatórios pedagógicos
R=$(PGPASSWORD=$DB_PASSWORD psql -h 127.0.0.1 -U "$DB_USER" educar_demo -At -c "select tt.id, se.id from timetables tt join students_enrollments se on se.school_academics_years_id = tt.school_academics_years_id and se.grade_id = tt.grade_id and se.class = tt.class and se.status = 'Activo' where tt.school_academics_years_id = 2 and tt.grade_id = 1 and tt.class = 'A' order by se.number limit 1")
echo "{\"ano\": 2, \"turma\": ${R%%|*}, \"matricula\": ${R##*|}}" > "$T/relatorios_demo.json"
capturar --etapa relatorios --ids "$T/relatorios_demo.json"
rm -f "$T/listas_demo.json"
for etapa in enviada aceite fechada; do
  semear listas -etapa "$etapa" -saida "$T/listas_demo.json"
  capturar --etapa "lista_$etapa" --ids "$T/listas_demo.json"
done
echo "recusas de acesso: $(grep -c 'Acesso negado' "$T/web.log" || true)"
