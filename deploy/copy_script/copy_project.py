import json
import os
import shutil

project_params = {}


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
    for directory_name in ['deploy', 'example-project-web', 'example_project_backend']:
        sub_project_path = os.path.join(project_path, directory_name)
        sub_example_project_path = os.path.join(example_project_path, directory_name)
        shutil.copytree(sub_example_project_path, sub_project_path)
    gitignore_project_path = os.path.join(project_path, '.gitignore')
    gitignore_example_project_path = os.path.join(example_project_path, '.gitignore')
    shutil.copy(gitignore_example_project_path, gitignore_project_path)


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
UNWANTED_DIRS = ['.git']


def replace_string_in_directory(directory_path, old_string, new_string):
    for path, dirs, files in os.walk(directory_path):
        if any([path.endswith(ext) or ext in f'/{path}/' for ext in UNWANTED_DIRS]):
            continue
        for filename in files:
            filepath = os.path.join(path, filename)
            if any([filepath.endswith(ext) for ext in UNWANTED_FILE_EXT]):
                continue
            print(filepath)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(old_string, new_string)
            with open(filepath, "w") as f:
                f.write(s)


def change_backend_name_in_files():
    project_backend_name = 'example_project_backend'
    new_project_backend_name = project_params['project_backend_name']

    project_path = get_new_project_path()

    replace_string_in_directory(project_path, project_backend_name, new_project_backend_name)


def change_frontend_name():
    project_frontend_name = 'example-project-web'
    new_project_frontend_name = project_params['project_frontend_name']

    project_path = get_new_project_path()

    project_frontend_path = os.path.join(project_path, project_frontend_name)
    new_project_frontend_path = os.path.join(project_path, new_project_frontend_name)

    os.rename(project_frontend_path, new_project_frontend_path)


def change_frontend_name_in_files():
    project_frontend_name = 'example-project-web'
    new_project_frontend_name = project_params['project_frontend_name']

    project_path = get_new_project_path()

    replace_string_in_directory(project_path, project_frontend_name, new_project_frontend_name)


def change_database():
    db_name = 'example_db'
    new_db_name = project_params['db_name']

    db_username = 'db_admin'
    new_db_username = project_params['db_username']

    db_password = '<db_password>'
    new_db_password = project_params['db_password']

    project_path = get_new_project_path()

    replace_string_in_directory(project_path, db_name, new_db_name)
    replace_string_in_directory(project_path, db_username, new_db_username)
    replace_string_in_directory(project_path, db_password, new_db_password)


def change_title():
    title = 'Example'
    new_project_frontend_name = project_params['project_frontend_name']
    new_title = project_params['title']

    title_with_html = f'<title>{title}</title>'
    new_title_with_html = f'<title>{new_title}</title>'

    project_path = get_new_project_path()
    new_project_backend_path = os.path.join(project_path, new_project_frontend_name)

    replace_string_in_directory(new_project_backend_path, title_with_html, new_title_with_html)


if __name__ == '__main__':
    project_params = json.load(open('project_params.json', 'r'))

    copy_entire_project()
    change_backend_directories()
    change_backend_name_in_files()
    change_frontend_name()
    change_frontend_name_in_files()
    change_database()
    change_title()
