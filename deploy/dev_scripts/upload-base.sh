#!/usr/bin/env bash
hostname=$1
build_ui=$2
prod_env=$3

echo hostname $hostname
echo build_ui $build_ui
echo prod_env $prod_env

if $build_ui = true; then
  ./build-web.sh
fi


ssh $hostname -C "sudo chmod -R 777 ~/example-project/"
rsync -avrm --delete ../../ $hostname:~/example-project --exclude='node_modules/' --exclude='.angular/' --exclude='.git/' \
  --exclude='pocs/' --exclude='.idea/' --exclude='example-project-web/src/' --exclude='__pycache__/' --include='dist/*'

ssh $hostname -C "cd ~/example-project/deploy/scripts/; ./restart_${prod_env}.sh"

