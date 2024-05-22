import os
import subprocess

def create_django_project(project_name):
    subprocess.run(['django-admin', 'startproject', project_name])

def main():
    project_name = input("Enter the name of your Django project: ")
    create_django_project(project_name)
    print(f"Django project '{project_name}' created successfully!")

if __name__ == "__main__":
    main()
