# I am referencing the image digest to ensure deterministic build
FROM node:14.8.0-alpine3.12@sha256:985f18d0168e1d1d2ab8492f7be3ffec9e22c3db3ce242e01c16c36e08ce35eb

# sometimes significant to production performance
ENV NODE_ENV production

WORKDIR /usr/src/app

COPY package.json package-lock.json ./

# only install production dependencies in a deterministic way
RUN npm install ci --only=production
RUN npm install react-scripts@3.4.3 -g

CMD ["pwd"]
COPY . ./

EXPOSE 3000

CMD ["npm", "start"]

