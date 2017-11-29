FROM python:alpine3.6

WORKDIR /var/www/docker/plataforma-gobcl
COPY requirements.txt .

RUN apk add --no-cache make gcc g++ libstdc++ python3-dev git postgresql-dev libffi-dev musl-dev nodejs nodejs-npm zlib-dev jpeg-dev libxml2-dev libxslt-dev

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT gunicorn project.wsgi:application -c project/production/gunicorn_conf.py
