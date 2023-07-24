# Django側のDockerfile
FROM python:3.9-alpine
ENV PYTHONBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:80