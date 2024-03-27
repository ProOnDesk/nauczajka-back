FROM python:3.11.8-alpine3.19

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./bdio_backend ./bdio_backend
COPY ./requirements.txt /tmp/requirements.txt

WORKDIR ./bdio_backend
EXPOSE 8000

RUN python -m venv /py && \
    apk add --update --no-cache jpeg-dev && /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER django-user
