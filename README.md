# Инструкция
## О программе

Данный репозиторий позволит отсортировать изображения по цветам спектра с помощью чат-бота Telegram.

## Установка

Введите в консоли следующие команды для клонирования репозитория и установки нужных библиотек:
```bash
git clone https://github.com/ViktorBZKL/sort-by-spectrum.git
```
```bash
pip install -r requirements.txt
```
Теперь в файле `.env` в переменную `TOKEN` введите API-ключ от бота Telegram, который можно получить при создании бота через https://t.me/BotFather

## Использование
Запустите программу:
```bash
python3 main.py
```
Теперь откройте своего чат-бота, введите команду /start и отправьте ему архив .zip с изображениями для сортировки. Убедитесь в отсутствии лишних файлов в архиве.
