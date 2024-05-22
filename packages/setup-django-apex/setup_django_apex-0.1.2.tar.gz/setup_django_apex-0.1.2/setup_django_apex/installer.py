import os
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command failed with error: {stderr.decode('utf-8')}")
    return stdout.decode('utf-8')

def create_django_project(project_name):
    run_command(f'django-admin startproject {project_name}')
    os.chdir(project_name)

def create_django_app(app_name):
    run_command(f'python manage.py startapp {app_name}')

def update_settings(app_names, project_name):
    settings_path = os.path.join(project_name, 'settings.py')
    with open(settings_path, 'r') as file:
        settings = file.readlines()

    installed_apps_index = None
    for i, line in enumerate(settings):
        if line.strip() == 'INSTALLED_APPS = [':
            installed_apps_index = i
            break

    if installed_apps_index is None:
        raise Exception("Couldn't find INSTALLED_APPS in settings.py")

    for app_name in app_names:
        app_entry = f"    '{app_name}',\n"
        if app_entry not in settings:
            settings.insert(installed_apps_index + 1, app_entry)

    with open(settings_path, 'w') as file:
        file.writelines(settings)

def main(project_name=None, num_apps=None, app_names=None):
    if not project_name:
        project_name = input("Enter the name of your Django project: ")
    create_django_project(project_name)

    if num_apps is None:
        num_apps = int(input("How many apps do you want to create? "))
    if app_names is None:
        app_names = []
        for _ in range(num_apps):
            app_name = input("Enter the name of the app: ")
            create_django_app(app_name)
            app_names.append(app_name)

    update_settings(app_names, project_name)
    print(f"Successfully created project {project_name} with apps: {', '.join(app_names)}")

if __name__ == "__main__":
    main()
