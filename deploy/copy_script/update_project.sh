
backend_directory=$(ls ~/dev/$1 | grep backend)
frontend_directory=$(ls ~/dev/$1 | grep web)
rsync -av ~/dev/example-project/example_project_backend/common/ ~/dev/$1/$backend_directory/common/
rsync -av ~/dev/example-project/example-project-web/src/assets/styles/ ~/dev/$1/$frontend_directory/src/assets/styles/
rsync -av ~/dev/example-project/example-project-web/src/app/shared/ ~/dev/$1/$frontend_directory/src/app/shared/ --exclude='apis/' \
  --exclude='*/routing.service.ts' --exclude='*/breadcrumbs.service.ts' --exclude='interfaces/' --exclude='string-display/' \
  --exclude='*/shared.module.ts'