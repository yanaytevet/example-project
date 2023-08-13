#!/usr/bin/env bash
read -p "Enter the hostname (user@platform.com): " remote_ssh


remote_file_save_path="/tmp"
exclude_tables=("contenttypes" "auth.Permission" "admin.logentry" "sessions.session")

container_name="dockers-example_db-1"
local_container_name="dockers-example_db-1"

exclude_options=""

for table_name in "${exclude_tables[@]}"; do
  exclude_options+="--exclude-table=${table_name} "
done

dump_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

ssh "$remote_ssh" \
  "echo 'Dumping the remote database...'; \
  docker exec $container_name pg_dump -U db_admin -d example_db -j 2 --format=directory $exclude_options -f /dump-fragments; \
  echo 'Compressing remote dump...'; \
  docker exec $container_name tar -czvf /dump-fragments.tar.gz /dump-fragments; \
  echo 'Copying remote dump from docker...'; \
  docker cp $container_name:/dump-fragments.tar.gz $remote_file_save_path; \
  echo 'Cleaning remote dump...'; \
  docker exec $container_name rm -rf /dump-fragments.tar.gz; \
  docker exec $container_name rm -rf /dump-fragments"; \


echo "Copying remote dump from remote to local machine..."
#rsync --progress -e ssh $remote_ssh:$remote_file_save_path/dump-fragments.tar.gz "$dump_path"
scp $remote_ssh:$remote_file_save_path/dump-fragments.tar.gz $dump_path

echo "Cleaning remote dump..."
ssh "$remote_ssh" "rm $remote_file_save_path/dump-fragments.tar.gz"

wait  # Wait for the background process to finish

echo "Loading remote dump into local docker..."
docker cp $dump_path/dump-fragments.tar.gz "$local_container_name":dump-fragments.tar.gz

wait  # Wait for the background process to finish

echo "Destroying the local database..."
docker exec $local_container_name dropdb -U db_admin example_db

wait  # Wait for the background process to finish

echo "Creating local database..."
docker exec -it "$local_container_name" createdb -U db_admin example_db

wait  # Wait for the background process to finish

echo "UnCompressing dump..."
docker exec "$local_container_name" tar -xzvf dump-fragments.tar.gz

echo "Uploading dump to local database..."
docker exec "$local_container_name" pg_restore -U db_admin -d example_db --jobs=5 -Fd ./dump-fragments

wait  # Wait for the background process to finish

echo "Cleaning up..."
docker exec "$local_container_name" rm -r ./dump-fragments
rm -r "$dump_path"/dump-fragments.tar.gz

echo "Finished!"

