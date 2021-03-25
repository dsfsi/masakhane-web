# Building the application
FROM node:lts-buster as build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
# Increate node max memory, the default memory limit is too low for building 
ENV NODE_OPTIONS --max-old-space-size=8192 

COPY package.json package-lock.json ./

# NOTE: opencollective is not required but leads to warnings if missing
RUN npm install

# RUN apt-get update && apt-get install -y curl

# install the dependencies
# RUN npm ci 

COPY . ./

CMD ["npm", "start", "run"]

# This is updated in to update the models dictionary state.
# ENTRYPOINT ["curl --location --request GET 'http://127.0.0.1:5000/update' --data-raw ''"]