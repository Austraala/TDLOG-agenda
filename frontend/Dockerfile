FROM node:14

WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm build --prod
EXPOSE 4200
CMD [ "npm", "start" ]
