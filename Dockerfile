# Django側のDockerfile
FROM python:3.9-alpine
ENV PYTHONBUFFERED 1

RUN apk update \
    && apk add --no-cache sqlite \
    && rm -rf /var/cache/apk/*

ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.9/litestream-v0.3.9-linux-amd64-static.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz

RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:8080
# CMD ["/bin/bash", "/backend/run.sh"]