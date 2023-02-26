# Build Image
# -----------
FROM node:latest AS build

RUN apt-get update && \ 
    apt-get install -y --no-install-recommends dumb-init

WORKDIR /usr/src/app

COPY package*.json /usr/src/app/

# RUN npm install react-scripts@3.4.3 -g

RUN npm i

# Production Image
# ----------------
# I am referencing the image digest to ensure deterministic build
FROM node:14.8.0-alpine3.12@sha256:985f18d0168e1d1d2ab8492f7be3ffec9e22c3db3ce242e01c16c36e08ce35eb

# sometimes significant to production performance
ENV NODE_ENV production

COPY --from=build /usr/bin/dumb-init /usr/bin/dumb-init

# Following least privilege principle, to ensure we don't provide root access to our container default user
USER node

WORKDIR /usr/src/app

RUN npm install react-scripts@3.4.0 -g

COPY --chown=node:node --from=build /usr/src/app/node_modules /usr/src/app/node_modules
COPY --chown=node:node . /usr/src/app

EXPOSE 3000

CMD [ "dumb-init", "node", "src/index.js" ]
