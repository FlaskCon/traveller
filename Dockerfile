FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install -r dev_requirements.txt
