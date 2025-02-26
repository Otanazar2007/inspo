FROM python:3.12
# создаем рабочую папку
WORKDIR /app
# копируем проект в эту папку
COPY . .
# что необходимо сделать перед запуском
RUN pip install -r requirements.txt
# команда для запуска проекта
CMD ["python", 'main.py']