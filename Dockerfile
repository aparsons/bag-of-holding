FROM python:alpine as base

FROM base as builder

COPY requirements.txt .
COPY requirements/ requirements/ 

RUN apk add --update \
        build-base \
        python3-dev \
        mariadb-dev && \
    mkdir libs && \
    pip3 install -r requirements.txt -t libs

FROM base

ENV PYTHONUNBUFFERED 1

RUN mkdir /bag-of-holding
WORKDIR /bag-of-holding
COPY . /bag-of-holding/

COPY --from=builder /libs /libs
ENV PYTHONPATH $PYTHONPATH:/libs

RUN python3 /bag-of-holding/project/manage.py makemigrations && \
    python3 /bag-of-holding/project/manage.py migrate && \
    python3 /bag-of-holding/project/manage.py loaddata /bag-of-holding/project/sample_data.json

ENTRYPOINT [ "python3", "/bag-of-holding/project/manage.py", "runserver", "0.0.0.0:8000" ]