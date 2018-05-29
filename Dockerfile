FROM python:alpine3.6

WORKDIR /var/www/docker/plataforma-gobcl
COPY requirements.txt .

RUN apk add --no-cache make gcc g++ libstdc++ python3-dev git libffi-dev musl-dev nodejs nodejs-npm zlib-dev jpeg-dev libxml2-dev libxslt-dev gettext

RUN npm install -g yarn

# workaround for https://bugs.alpinelinux.org/issues/8939
RUN apk add --no-cache openssl-dev
RUN pip install --no-cache-dir cryptography
RUN apk del openssl-dev
RUN apk add --no-cache postgresql-dev

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT gunicorn project.wsgi:application -c project/production/gunicorn_conf.py --max-requests 400 --workers 4 --worker-class gevent
