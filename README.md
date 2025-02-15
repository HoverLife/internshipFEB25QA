
## Добрый день! В этом проекте собраны автоматизированные тесты для проверки API вашего микросервиса. В тестах используется Python, библиотека pytest и requests. Следуйте, пожалуйста, этим шагам, чтобы запустить тесты:

## Инструкция по запуску тестов

### 1. Установка зависимостей

Убедитесь, что у вас установлен Python 3.8+ и `pip`. Затем установите необходимые зависимости:

```sh
pip install pytest
pip install requests
```

### 2. Запуск тестов

Для запуска тестов используйте команду:

```sh
pytest test.py
```
Если не работает, можете попробовать воспользоваться этой командой:

```sh
python -m pytest -v test_api.py
```

### 3. Ожидаемые результаты

При успешном прохождении тестов, вы увидите отчет о тестах без ошибок (такого не будет). В случае наличия ошибок будут указаны детали. Для более детального логирования можно запустить:

```sh
pytest -v --tb=short tests/
```