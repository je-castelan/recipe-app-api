FROM python:3.7-alpine
LABEL AUTHOR Jose Emanuel Castelan

ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# Setup directory structure
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

# Create media and static directories
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# Create new user
RUN adduser -D user

#New user will have assigned new direvtoires
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user