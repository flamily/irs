FROM postgres
COPY db/schema.sql /docker-entrypoint-initdb.d/