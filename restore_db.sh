#!/bin/sh
set PGPASSWORD=123456
# pg_ctl start -w -D ${PGDATA}
pg_restore -U hhuser -F c -d habitz "./habitz.sql"
# pg_ctl stop -w