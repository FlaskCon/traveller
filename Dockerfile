FROM python:alpine3.7
COPY . /app
WORKDIR /app

#Installing requirements for Pillow
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN pip install -r requirements.txt
RUN pip install -r dev_requirements.txt
