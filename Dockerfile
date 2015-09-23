FROM python:3

# Essentials
RUN apt-get update -qq && \
    apt-get install -y build-essential vim python3-pip

ENV PYTHONUNBUFFERED 1
RUN mkdir /bag-of-holding
WORKDIR /bag-of-holding
ADD . /bag-of-holding/
RUN pip install -r requirements.txt
RUN python /bag-of-holding/src/manage.py makemigrations
RUN python /bag-of-holding/src/manage.py migrate
RUN python /bag-of-holding/src/manage.py loaddata /bag-of-holding/src/sample_data.json


# docker build -t disenchant/boh .
# docker run -d -p 8000:8000 --name boh-server disenchant/boh python /bag-of-holding/src/manage.py runserver 0.0.0.0:8000
# docker exec -it boh-server bash
# python /bag-of-holding/src/manage.py createsuperuser