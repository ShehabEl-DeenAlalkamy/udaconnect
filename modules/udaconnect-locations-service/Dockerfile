# There are 2 reasons for choosing 3.8-alpine tag over 3.8:
# 1- it has much lower security risk compared to the latter.
# python:3.8 has          [5 H] [22 M] [242 L]
# python:3.8-alpine       [0 H] [0 M]  [0 L]
# where: H: High Severity Issue(s)
#        M: Medium Severity Issue(s)
#        L: Low Severity Issue(s)
# 2- fewer unused packages so lower size and less resource intensive
# Finally I am referencing the image digest to ensure deterministic build
FROM python:3.8-alpine@sha256:9e8a162cd85c78458ac47457b08450be8ca4ae5de5ee0f7b23665b6ea2569aed

# Adding doas pacakge, an alternative to sudo package
RUN apk add doas && \
    # Following least privilege principle, to ensure we don't provide root access to our container default user
    addgroup -g 3000 -S python && \
    adduser -u 3000 -G python -S python

RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app

# Ensuring curl is installed for docker native HEALTHCHECK command
RUN apk add curl && \
    rm -rf /var/cache/apk/*

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

CMD [ "flask", "run", "--host", "0.0.0.0" ]
# Adding a healthcheck to udaconnect-locations-service /health endpoint to test the container functionality
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:5000/health