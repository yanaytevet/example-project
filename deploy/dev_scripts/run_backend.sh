docker run -v $(pwd)/../../example_project_backend:/usr/src/app -v logs:/var/log/example-project/ -p 8000:8000 --rm -t \
    --network=example_project_docker_group_network --name=example_project_backend example_project_backend python manage.py runserver 0.0.0.0:8000 \
    --settings=example_project_backend.dev_docker_settings
