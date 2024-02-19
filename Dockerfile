FROM python:3.10

# Создаем директории и копируем файлы
RUN mkdir -p /opt/services/bot/OSOR_buyer
WORKDIR /opt/services/bot/OSOR_buyer

COPY . /opt/services/bot/OSOR_buyer/

# Создаем отдельную директорию для зависимостей
RUN mkdir -p /opt/services/bot/OSOR_buyer/requirements
COPY requirements.txt /opt/services/bot/OSOR_buyer/requirements/

# Устанавливаем зависимости, включая asyncpg
RUN pip install --no-cache-dir -r requirements.txt

# Удаляем предыдущие переменные окружения для PostgreSQL, они теперь задаются в Docker Compose
ENV POSTGRES_DB "bot_osor_buyer"
ENV POSTGRES_USER "postgres"
ENV POSTGRES_PASSWORD "123"
ENV POSTGRES_HOST "db"
ENV POSTGRES_PORT "5432"

# Команда для запуска приложения
CMD ["python", "/opt/services/bot/OSOR_buyer/main.py"]
