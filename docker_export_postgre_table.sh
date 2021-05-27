CONTAINER="db"
DB="masakhane"
TABLE="feedback"
FILE="feedback_data.csv"

# docker-compose -f docker-compose.prod.yml exec -u psql ${CONTAINER} psql -d ${DB} -c "COPY ${TABLE} TO STDOUT WITH CSV HEADER " > ${FILE}

docker-compose -f docker-compose.prod.yml exec db psql --username=masakhane --dbname=masakhane -c "COPY ${TABLE} TO STDOUT WITH CSV HEADER " > ${FILE}
