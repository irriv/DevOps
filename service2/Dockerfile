FROM node:22-slim

RUN apt-get update && apt-get install -y procps coreutils

WORKDIR /app2

COPY package*.json ./

RUN npm install --only=production

COPY . .

EXPOSE 8200

CMD ["node", "index.js"]
