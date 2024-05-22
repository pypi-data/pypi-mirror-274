import os
import subprocess
import unittest
import sys
sys.path.append("c:\\Users\\omani\\OneDrive\\Documents\\django_pip")
from setup_django_apex.installer import create_django_project, create_django_app, update_settings
class TestInstaller(unittest.TestCase):
    def setUp(self):
        # Set up any resources needed for the tests
        self.project_name = "test_project"

    # def tearDown(self):
    #     # Clean up resources after each test
    #     if os.path.exists(self.project_name):
    #         subprocess.run(f"rm -rf {self.project_name}", shell=True)

    def test_create_django_project(self):
        # Test creating a Django project
        if not os.path.exists(self.project_name):
            create_django_project(self.project_name)
            self.assertTrue(os.path.isdir(self.project_name))

    # def test_create_django_app(self):
    #     # Test creating a Django app
    #     if not os.path.exists(self.project_name):
    #         create_django_project(self.project_name)  # Ensure project is created first
    #     create_django_app("test_app")
    #     app_dir = os.path.join(self.project_name, "test_app")
    #     self.assertTrue(os.path.isdir(app_dir))
    #     self.assertTrue(os.path.isfile(os.path.join(app_dir, "views.py")))

    def test_update_settings(self):
        # Test updating settings.py
        app_names = ["app1", "app2"]
        if not os.path.exists(self.project_name):
            (self.project_name)  # Ensure project is created first
        
        for app_name in app_names:
            create_django_app(app_name)  # Ensure all required apps are created
        # create_django_app("test_app")  # Ensure at least one app is created
        update_settings(app_names, self.project_name)
        settings_path = os.path.join(self.project_name, "settings.py")
        with open(settings_path, "r") as file:
            settings_content = file.read()
        for app_name in app_names:
            self.assertIn(f"'{app_name}'", settings_content)

if __name__ == "__main__":
    unittest.main()
