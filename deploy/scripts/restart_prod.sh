#!/usr/bin/env bash
docker-compose -f ../dockers/docker-compose-stage.yml -f ../dockers/docker-compose-prod.yml up --force-recreate -d \
  --no-deps --remove-orphans example_project_backend x_celery_worker emails_celery_worker events_celery_worker \
  nginx_service celery_scheduler
