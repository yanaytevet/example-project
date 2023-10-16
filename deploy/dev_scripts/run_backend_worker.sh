docker run -v $(pwd)/../../example_project_backend:/usr/src/app -v logs:/var/log/example-project/ --rm -t \
    --network=example_project_docker_group_network --name=example_project_backend_worker_$1 --env DJANGO_SETTINGS_MODULE=example_project_backend.dev_docker_settings \
    example_project_backend celery -A example_project_backend worker --concurrency=1 -Q $1
