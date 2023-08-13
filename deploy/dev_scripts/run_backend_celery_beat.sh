docker run -v $(pwd)/../../example_project_backend:/usr/src/app -v logs:/var/log/example-project/ --rm -t \
    --network=dockers_dev-network --name=example_project_backend_celery_beat example_project_backend celery -A example_project_backend beat \
    --scheduler django_celery_beat.schedulers:DatabaseScheduler --settings=example_project_backend.dev_docker_settings
