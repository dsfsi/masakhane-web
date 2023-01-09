# Building the application
FROM node:lts-buster as build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
# Increate node max memory, the default memory limit is too low for building 
ENV NODE_OPTIONS --max-old-space-size=8192 

# add dependencies
COPY package.json package-lock.json ./
# install dependencies 
RUN npm install --legacy-peer-deps
RUN npm i webpack webpack-cli --legacy-peer-deps
RUN npm i @babel/core @babel/preset-env @babel/preset-react babel-loader --legacy-peer-deps

# add app
COPY . ./

# RUN npm command 
CMD ["npm", "run", "develop"]
