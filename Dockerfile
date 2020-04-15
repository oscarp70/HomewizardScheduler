FROM python:3

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && apt-get update -y && \
    apt-get install -y python-pip python-dev cron

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && pip install -r requirements.txt
RUN apk add libcurl4-openssl-dev 
RUN apk add libssl-dev

COPY . /app

EXPOSE 8095

ENTRYPOINT [ "python" ]

CMD [ "scheduler.py" ]

