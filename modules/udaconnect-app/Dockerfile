# * given the lack of time for project submission, I am unable to optimize the Dockerfile more than this since I am not the developer of the client app
# * I will need to have a look at it later

# TODO: use multi-stage build

# TODO: use node:16.17.0-bullseye-slim
# ? why ?
# ? The Node.js image bundles the Alpine operating system which is powered by the minimal busybox software tooling and the musl C library implementation.
# ? These two Node.js Alpine image characteristics contribute to the Docker image being unofficially supported by the Node.js team. 
# ? Furthermore, many security vulnerabilities scanners can’t easily detect software artifacts or runtimes on Node.js Alpine images, 
# ? which is counterproductive to efforts to secure your container images.
# I am referencing the image digest to ensure deterministic build
FROM node:14.8.0-alpine3.12@sha256:985f18d0168e1d1d2ab8492f7be3ffec9e22c3db3ce242e01c16c36e08ce35eb

# TODO: make this line functional
# an init process, in that it is invoked with PID 1, then spawns our Node.js application as another process whilst ensuring that all signals are proxied to that Node.js process
# RUN apk add dumb-init

# sometimes significant to production performance
ENV NODE_ENV production

# Following least privilege principle, to ensure we don't provide root access to our container default user
RUN mkdir -p /usr/src/app && chown node:node /usr/src/app
WORKDIR /usr/src/app

# install dependencies and leverage docker caching layer
COPY --chown=node:node package*.json /usr/src/app/

# TODO: 'npm install' is not recommended instead should use 'npm ci --only=production' but the package.json and package-lock.json are not in sync
RUN npm install

# TODO: this line should be removed
RUN npm install react-scripts@3.4.3 -g

COPY --chown=node:node . /usr/src/app

# su node
USER node

EXPOSE 3000

# TODO: instead use CMD ['dumb-int', 'node', 'src/index.js'] to ensure that all signals are proxied to that Node.js process
CMD ["npm", "start"]
