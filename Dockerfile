FROM python:3.12

RUN mkdir /my_app

WORKDIR /my_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker_cmds/*.sh
