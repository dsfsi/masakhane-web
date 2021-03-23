# base image
# FROM python:3.6.9-alpine
FROM python:3.6.9
# FROM python:3.8.1-slim-buster

# set working directory 
WORKDIR /usr/src/app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# RUN apt-get update && apt-get -y dist-upgrade
# RUN apt-get -y install build-essential libssl-dev libffi-dev libblas3 libc6 liblapack3 gcc python3-dev python3-pip cython3
# RUN apt-get -y install python3-numpy python3-scipy 
# RUN apt install -y netcat
# RUN apt-get update && \
#     # apt-get build-deps gcc python-dev musl-dev && \
#     # apt-get g++ && \
#     apt-get postgresql-dev && \
    # apt-get --update netcat-openbsd

RUN apt-get update
RUN apt-get install -y gnupg lsb-release wget

RUN lsb_release -c -s > /tmp/lsb_release
RUN GCSFUSE_REPO=$(cat /tmp/lsb_release); echo "deb http://packages.cloud.google.com/apt gcsfuse-$GCSFUSE_REPO main" | tee /etc/apt/sources.list.d/gcsfuse.list
RUN wget -O - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN apt-get update
RUN apt-get install -y gcsfuse

RUN pip install --upgrade pip

# add and install requirements 
COPY ./requirements.txt /usr/src/app/requirements.txt
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app


# run server (https://github.com/testdrivenio/testdriven-app/issues/25)
CMD ["sh","-c","chmod 777 /usr/src/app/entrypoint.sh"]
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]