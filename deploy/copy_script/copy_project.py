import json
import os
import shutil

project_params = {}
MAIN_DIRECTORIES = ['deploy', 'example-project-web', 'example_project_backend']


def get_new_project_path():
    project_path = project_params['project_path']
    project_path = os.path.expanduser(project_path)
    return project_path


def copy_entire_project():
    project_path = get_new_project_path()
    example_project_relative_path = '../..'
    example_project_path = os.path.abspath(example_project_relative_path)
    if not os.path.exists(project_path):
        os.mkdir(project_path)
    for directory_name in MAIN_DIRECTORIES:
        sub_project_path = os.path.join(project_path, directory_name)
        sub_example_project_path = os.path.join(example_project_path, directory_name)
        shutil.copytree(sub_example_project_path, sub_project_path)
    gitignore_project_path = os.path.join(project_path, '.gitignore')
    gitignore_example_project_path = os.path.join(example_project_path, '.gitignore')
    shutil.copy(gitignore_example_project_path, gitignore_project_path)


def remove_unwanted_directories():
    project_path = get_new_project_path()
    for directory_name in MAIN_DIRECTORIES:
        sub_project_path = os.path.join(project_path, directory_name)
        idea_directory = os.path.join(sub_project_path, '.idea')
        if os.path.exists(idea_directory):
            shutil.rmtree(idea_directory)


def change_backend_directories():
    project_backend_name = 'example_project_backend'
    new_project_backend_name = project_params['project_backend_name']

    project_path = get_new_project_path()

    inner_project_backend_path = os.path.join(project_path, project_backend_name, project_backend_name)
    new_inner_project_backend_path = os.path.join(project_path, project_backend_name, new_project_backend_name)

    os.rename(inner_project_backend_path, new_inner_project_backend_path)

    project_backend_path = os.path.join(project_path, project_backend_name)
    new_project_backend_path = os.path.join(project_path, new_project_backend_name)

    os.rename(project_backend_path, new_project_backend_path)


UNWANTED_FILE_EXT = ['pyc', 'ico', 'DS_Store', 'gif']
UNWANTED_DIRS = ['.git', '.angular', 'node_modules']


files_cache = {}


def apply_changes():
    for filepath, content in files_cache.items():
        with open(filepath, "w") as f:
            f.write(content)


def replace_string_in_directory(directory_path, old_string, new_string):
    for path, dirs, files in os.walk(directory_path):
        if any([path.endswith(ext) or ext in f'/{path}/' for ext in UNWANTED_DIRS]):
            continue
        for filename in files:
            filepath = os.path.join(path, filename)
            if any([filepath.endswith(ext) for ext in UNWANTED_FILE_EXT]):
                continue
            print(filepath)
            if filepath not in files_cache:
                with open(filepath) as f:
                    s = f.read()
                files_cache[filepath] = s
            files_cache[filepath] = files_cache[filepath].replace(old_string, new_string)


def change_string_in_directory_by_param(old_value, param_name, sub_directory=None, mod_param_func=None):
    new_value = project_params[param_name]

    if mod_param_func:
        new_value = mod_param_func(new_value)

    project_path = get_new_project_path()
    if sub_directory:
        project_path = os.path.join(project_path, 'sub_directory')

    replace_string_in_directory(project_path, old_value, new_value)


def change_string_in_frontend_by_param(old_value, param_name, mod_param_func=None):
    change_string_in_directory_by_param(old_value, param_name, project_params['project_frontend_name'],
                                        mod_param_func=mod_param_func)


def change_backend_name_in_files():
    change_string_in_directory_by_param('example_project_backend', 'project_backend_name')


def change_project_name_in_files():
    change_string_in_directory_by_param('example-project', 'project_path',
                                        project_params['project_frontend_name'],
                                        mod_param_func=lambda x: os.path.split(x)[-1])
    change_string_in_directory_by_param('example-project', 'project_path', 'deploy',
                                        mod_param_func=lambda x: os.path.split(x)[-1])


def change_frontend_name():
    project_frontend_name = 'example-project-web'
    new_project_frontend_name = project_params['project_frontend_name']

    project_path = get_new_project_path()

    project_frontend_path = os.path.join(project_path, project_frontend_name)
    new_project_frontend_path = os.path.join(project_path, new_project_frontend_name)

    os.rename(project_frontend_path, new_project_frontend_path)
    change_string_in_directory_by_param(project_frontend_name, 'project_frontend_name')


def change_frontend_name_in_files():
    change_string_in_directory_by_param('example-project-web', 'project_frontend_name')


def change_database():
    change_string_in_directory_by_param('example_db', 'db_name')
    change_string_in_directory_by_param('db_admin', 'db_username')
    change_string_in_directory_by_param('<db_password>', 'db_password')


def change_title():
    change_string_in_frontend_by_param('<title>Example</title>', 'title',
                                       mod_param_func=lambda title: f'<title>{title}</title>')


def change_docker_group_name():
    change_string_in_directory_by_param('example_project_docker_group', 'dockers_group_name')


def change_domain():
    change_string_in_directory_by_param('example-domain.com', 'domain')


def change_logs_dir():
    change_string_in_directory_by_param('/var/log/example-project/', 'dockers_group_name',
                                        mod_param_func=lambda x: f'/var/log/{x}/')


if __name__ == '__main__':
    project_params = json.load(open('project_params.json', 'r'))

    copy_entire_project()
    remove_unwanted_directories()
    change_backend_directories()
    change_frontend_name()
    change_backend_name_in_files()
    change_frontend_name_in_files()
    change_project_name_in_files()
    change_database()
    change_title()
    change_domain()
    change_logs_dir()
    change_docker_group_name()
    apply_changes()
