docker run -it -v $(pwd)/../../example_project_backend:/usr/src/app -v logs:/var/log/example-project/ --rm -t \
    --network=dockers_dev-network example_project_backend python manage.py $1 $2 $3 $4 $5 --settings=example_project_backend.dev_docker_settings
