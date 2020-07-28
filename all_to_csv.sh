#!/bin/bash
sqlite3 ./temp.sqlite <<!
.headers on
.mode csv
.output full.csv
select * from temperatures;
!
