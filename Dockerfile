FROM python:alpine3.7

# #Installing requirements for Pillow
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY dev_requirements.txt /app
RUN pip install -r dev_requirements.txt

COPY . /app 

WORKDIR /app/traveller

RUN mkdir instance
RUN touch instance/config.py
RUN echo SQLALCHEMY_DATABASE_URI = '"mysql+pymysql://hB3NLp4kiW:5GBiMgmHyB@remotemysql.com:3306/hB3NLp4kiW"' >> ./instance/config.py

RUN ls ./
RUN python manage.py initialise
RUN flask seed dev
RUN python manage.py db migrate
RUN python manage.py db upgrade

CMD ["python", "manage.py", "rundebug"]