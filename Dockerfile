FROM python:3.11-slim

WORKDIR /IoTDevices

# Копируем файлы проекта в рабочую директорию
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Экспонируем порт
EXPOSE 8080

# Запуск приложения
CMD ["python", "app.py"]
