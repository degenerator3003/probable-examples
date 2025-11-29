#!/bin/bash

#docker rm -f bench_mem bench_cpu bench_disk
docker compose rm -f
#docker compose up --force-recreate
docker compose down
docker compose up --build
