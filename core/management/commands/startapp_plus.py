import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Crée une app Django dans /apps avec structure modulaire et fichiers initiaux"

    def add_arguments(self, parser):
        parser.add_argument('name', help="Nom de l'app à créer")
        parser.add_argument('--template', help="Chemin d'un template custom", default=None)
        parser.add_argument('--extensions', nargs='+', help="Extensions de fichiers à générer", default=None)

    def handle(self, *args, **options):
        name = options['name']
        template = options['template']
        extensions = options['extensions']

        # Dossier apps/
        base_dir = os.getcwd()
        apps_dir = os.path.join(base_dir, 'apps')
        os.makedirs(apps_dir, exist_ok=True)

        # Dossier de l'app
        app_dir = os.path.join(apps_dir, name)
        os.makedirs(app_dir, exist_ok=True)

        # Construction des kwargs pour startapp
        cmd_kwargs = {'directory': app_dir}
        if template:
            cmd_kwargs['template'] = template
        if extensions:
            cmd_kwargs['extensions'] = extensions

        # Appel de startapp avec nom interne "app"
        call_command('startapp', 'app', **cmd_kwargs)

        # Sous-dossiers à créer
        subdirs = ['models', 'serializers', 'views', 'services', 'tests']
        for subdir in subdirs:
            path = os.path.join(app_dir, subdir)
            os.makedirs(path, exist_ok=True)
            init_file = os.path.join(path, '__init__.py')
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(f"# Package {subdir} pour l'app {name}\n")

        # urls.py à la racine
        urls_path = os.path.join(app_dir, 'urls.py')
        with open(urls_path, 'w', encoding='utf-8') as f:
            f.write("from django.urls import path\n\nurlpatterns = []\n")

        # Suppression de admin.py si inutile
        if 'django.contrib.admin' not in settings.INSTALLED_APPS:
            admin_path = os.path.join(app_dir, 'admin.py')
            if os.path.exists(admin_path):
                os.remove(admin_path)

        # Fichiers à supprimer car remplacés par des dossiers
        redundant_files = ['models.py', 'views.py', 'tests.py']
        for fname in redundant_files:
            path = os.path.join(app_dir, fname)
            if os.path.exists(path):
                os.remove(path)

        self.stdout.write(self.style.SUCCESS(
            f"✅ App '{name}' créée dans 'apps/{name}' avec structure modulaire et fichiers init."
        ))

