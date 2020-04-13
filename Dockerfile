FROM python:3

ADD Rest.py /
ADD mieleRequest.py /

RUN pip3 install pymysql
RUN pip3 install requests
RUN pip3 install phue

CMD [ "python", "/Rest.py" ]