docker exec example_project_docker_group-nginx_service-1 -it bash create-cert.sh
(crontab -l 2>/dev/null; echo "0 6 * * * root /home/platform/example-project/deploy/scripts/renew-cert.sh") | crontab -