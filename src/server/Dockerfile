# base image
FROM python:3.6.9

# set working directory 
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat
RUN apt-get update
RUN apt-get install -y gnupg lsb-release wget

RUN lsb_release -c -s > /tmp/lsb_release
RUN GCSFUSE_REPO=$(cat /tmp/lsb_release); echo "deb http://packages.cloud.google.com/apt gcsfuse-$GCSFUSE_REPO main" | tee /etc/apt/sources.list.d/gcsfuse.list
RUN wget -O - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN apt-get update
RUN apt-get install -y gcsfuse


# add and 
COPY ./requirements.txt /usr/src/app/requirements.txt
# RUN pip install to install requirements 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app


# run server (https://github.com/testdrivenio/testdriven-app/issues/25)
CMD ["sh","-c","chmod 777 /usr/src/app/entrypoint.sh"]
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
