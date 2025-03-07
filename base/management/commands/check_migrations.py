from django.core.management.base import BaseCommand
from django.db.migrations.executor import MigrationExecutor
from django.db import connection

class Command(BaseCommand):
    help = "تحقق مما إذا كانت جميع الهجرات قد اكتملت"

    def handle(self, *args, **kwargs):
        executor = MigrationExecutor(connection)
        unapplied_migrations = executor.migration_plan(executor.loader.graph.leaf_nodes())

        if not unapplied_migrations:
            self.stdout.write(self.style.SUCCESS("✅ جميع الهجرات مكتملة!"))
            exit(0)  # نجاح
        else:
            self.stdout.write(self.style.ERROR("⚠️ هناك هجرات غير مكتملة!"))
            exit(1)  # فشل
