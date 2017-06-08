FROM alpine

RUN apk --update add python3 && apk add bash

ENV PYTHONUNBUFFERED 1
RUN mkdir /bag-of-holding
WORKDIR /bag-of-holding
ADD . /bag-of-holding/
RUN pip3 install -r requirements.txt
RUN python3 /bag-of-holding/src/manage.py makemigrations
RUN python3 /bag-of-holding/src/manage.py migrate
RUN python3 /bag-of-holding/src/manage.py loaddata /bag-of-holding/src/sample_data.json

CMD python3 /bag-of-holding/src/manage.py runserver 0.0.0.0:8000

# Instructions:
# docker run -d -p 8000:8000 --name boh-server disenchant/bag-of-holding:latest
# docker exec -it boh-server bash
# python3 /bag-of-holding/src/manage.py createsuperuser
