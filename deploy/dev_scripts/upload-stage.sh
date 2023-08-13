#!/usr/bin/env bash
build_ui=true

print_usage() {
  printf "allowed flags are -s (skip build ui)"
}


while getopts 'sra' flag; do
  case "${flag}" in
    s) build_ui='false' ;;
    *) print_usage
       exit 1 ;;
  esac
done

./upload-base.sh platform@stage.example-project.com $build_ui stage
