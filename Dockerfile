# syntax=docker/dockerfile:1

FROM python:3.9.16-alpine3.18
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /cbshop
RUN apk update && \
    apk add gcc && \
    apk add libffi-dev && \
    apk add musl-dev && \
    apk add --no-cache bash && \
    apk add mariadb-dev && \
    pip install pip-tools
COPY . .
RUN pip-sync ./requirements/requirements.txt
RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]