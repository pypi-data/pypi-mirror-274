import unittest
import os
import shutil
from setup_django_apex.installer import create_django_project, create_django_app, update_settings

class TestInstaller(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_name = 'testproject'
        cls.app_names = ['app1', 'app2']
        create_django_project(cls.project_name)
        os.chdir(cls.project_name)

    @classmethod
    def tearDownClass(cls):
        os.chdir('..')
        shutil.rmtree(cls.project_name)

    def test_create_django_app(self):
        for app_name in self.app_names:
            create_django_app(app_name)
            self.assertTrue(os.path.isdir(app_name))
            self.assertTrue(os.path.isfile(os.path.join(app_name, 'views.py')))

    def test_update_settings(self):
        update_settings(self.app_names, self.project_name)
        settings_path = os.path.join(self.project_name, 'settings.py')
        with open(settings_path, 'r') as file:
            settings_content = file.read()
            for app_name in self.app_names:
                self.assertIn(f"'{app_name}'", settings_content)

if __name__ == '__main__':
    unittest.main()
