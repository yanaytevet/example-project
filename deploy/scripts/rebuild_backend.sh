#!/usr/bin/env bash
docker-compose -f ../dockers/docker-compose-stage.yml -f ../dockers/docker-compose-prod.yml build example_project_backend