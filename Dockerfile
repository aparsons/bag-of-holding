FROM ubuntu

#RUN apk --update add python3 && apk add bash
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y libmysqlclient-dev

ENV PYTHONUNBUFFERED 1
RUN mkdir /bag-of-holding
WORKDIR /bag-of-holding
ADD . /bag-of-holding/
RUN pip3 install -r requirements.txt
RUN python3 /bag-of-holding/project/manage.py makemigrations
RUN python3 /bag-of-holding/project/manage.py migrate
RUN python3 /bag-of-holding/project/manage.py loaddata /bag-of-holding/project/sample_data.json

CMD python3 /bag-of-holding/project/manage.py runserver 0.0.0.0:8000

# Instructions:
# docker run -d -p 8000:8000 --name boh-server disenchant/bag-of-holding:latest
# docker exec -it boh-server bash
# python3 /bag-of-holding/src/manage.py createsuperuser
