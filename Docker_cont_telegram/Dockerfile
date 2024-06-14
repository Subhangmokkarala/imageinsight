FROM python:3.10.12

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y 
RUN apt install python3-pip -y
RUN pip3 install requirements.txt

COPY . /imageinsightapp
WORKDIR /imageinsightapp

CMD ["python3", "imageinsight.py"]