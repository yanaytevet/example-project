#!/usr/bin/env bash
mkdir -p ~/nginx-conf
mkdir -p ~/letsencrypt

docker-compose -f ../dockers/docker-compose-stage.yml -f ../dockers/docker-compose-prod.yml up --force-recreate -d
