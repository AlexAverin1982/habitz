#!/bin/sh
set PGPASSWORD=123456
pg_restore -U hhuser -F c -d habitz "./habitz.sql"