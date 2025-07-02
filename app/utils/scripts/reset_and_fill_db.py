import os
import shutil
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent  # sadaka_app/
DB_FILE = PROJECT_ROOT / "data" / "db.sqlite3"
MIGRATIONS_DIR = PROJECT_ROOT / "app" / "migration" / "versions"
DB_FILL_SCRIPT = PROJECT_ROOT / "app" / "utils" / "scripts" / "local_db_fill.py"


def remove_all_migrations():
    if MIGRATIONS_DIR.exists():
        shutil.rmtree(MIGRATIONS_DIR)
        MIGRATIONS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"✅ Все миграции удалены: {MIGRATIONS_DIR}")
    else:
        print(f"⚠️ Папка миграций не найдена: {MIGRATIONS_DIR}")


def remove_database():
    if DB_FILE.exists():
        try:
            subprocess.run(["rm", str(DB_FILE)], check=True)
            print(f"✅ База данных удалена через rm: {DB_FILE}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка при удалении базы через rm: {e}")
    else:
        print(f"⚠️ Файл базы данных не найден: {DB_FILE}")


def make_migration():
    subprocess.run("alembic revision --autogenerate -m 'Initial migration'", shell=True, check=True, cwd=PROJECT_ROOT)
    print("✅ Миграция создана.")


def apply_migration():
    subprocess.run("alembic upgrade head", shell=True, check=True, cwd=PROJECT_ROOT)
    print("✅ Миграции применены.")


def run_fill_script():
    subprocess.run(f"python {DB_FILL_SCRIPT}", shell=True, check=True, cwd=PROJECT_ROOT)
    print("✅ Скрипт заполнения БД выполнен.")


if __name__ == "__main__":
    os.chdir(PROJECT_ROOT)
    print(f"📁 Переход в корень проекта: {PROJECT_ROOT}")
    remove_all_migrations()
    remove_database()
    make_migration()
    apply_migration()
    run_fill_script()
