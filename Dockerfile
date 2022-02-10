FROM python:alpine3.7

# #Installing requirements for Pillow
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app 

WORKDIR /app/traveller

RUN mkdir instance
RUN touch instance/config.py

RUN python manage.py initialise
RUN python manage.py db migrate
RUN python manage.py db upgrade

CMD ["python", "manage.py", "rundebug"]