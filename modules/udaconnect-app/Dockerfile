# I am referencing the image digest to ensure deterministic build
FROM node:14.8.0-alpine3.12@sha256:985f18d0168e1d1d2ab8492f7be3ffec9e22c3db3ce242e01c16c36e08ce35eb

# an init process, in that it is invoked with PID 1, then spawns our Node.js application as another process whilst ensuring that all signals are proxied to that Node.js proce
RUN apk add dumb-init

# sometimes significant to production performance
ENV NODE_ENV production

# Following least privilege principle, to ensure we don't provide root access to our container default user
RUN mkdir -p /usr/src/app && chown node:node /usr/src/app
WORKDIR /usr/src/app

# install dependencies and leverage docker caching layer
COPY --chown=node:node package*.json /usr/src/app/
RUN npm install
RUN npm install react-scripts@3.4.3 -g

COPY --chown=node:node . /usr/src/app

# su node
USER node

EXPOSE 3000

CMD [ "dumb-init", "node", "src/index.js" ]
