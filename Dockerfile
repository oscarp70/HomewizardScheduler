FROM python:3

ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && apt-get update -y && \
    apt-get install -y python-pip python-dev cron libcurl4-openssl-dev libssl-dev nano sudo

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && pip install -r requirements.txt

COPY . /app

EXPOSE 8095

ENTRYPOINT [ "python" ]

CMD [ "scheduler.py" ]
