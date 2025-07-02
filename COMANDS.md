Удаление всех пакетов из окружения:
```bash
pip list --format=freeze | xargs pip uninstall -y

