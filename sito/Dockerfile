FROM python:3.9-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends \
    build-essential gcc libmariadb-dev nginx \
    libpq-dev python-dev

COPY ./requirements.txt /app/requirements.txt

RUN pip install --user --upgrade pip
RUN pip install --user -r requirements.txt

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder  /usr/lib/x86_64-linux-gnu/libmariadb* /usr/lib/x86_64-linux-gnu/

ENV PATH=/root/.local/bin:$PATH


COPY . .
