# I am referencing the image digest to ensure deterministic build
FROM python:3.8-alpine@sha256:9e8a162cd85c78458ac47457b08450be8ca4ae5de5ee0f7b23665b6ea2569aed

# Adding doas pacakge, an alternative to sudo package
RUN apk add doas && \
    # Following least privilege principle, to ensure we don't provide root access to our container default user
    addgroup -g 3000 -S python && \
    adduser -u 3000 -G python -S python

RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app

# Install dependencies
RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

# Making use of docker layer caching by separating the dependencies from the source code
COPY --chown=python:python requirements.txt .
RUN pip install -r requirements.txt

# Adding source code
COPY --chown=python:python . .

# su python
USER 3000

EXPOSE 5000

# gRPC server port
EXPOSE 5010

CMD [ "flask", "run", "--host", "0.0.0.0" ]