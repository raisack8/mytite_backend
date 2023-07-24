# Django側のDockerfile
FROM python:3.9-alpine
ENV PYTHONBUFFERED 1

RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:8080