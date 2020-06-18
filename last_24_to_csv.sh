#!/bin/bash
sqlite3 ./temp.sqlite <<!
.headers on
.mode csv
.output last24.csv
select * from temperatures where time >= datetime('now', '-1 day');
!
