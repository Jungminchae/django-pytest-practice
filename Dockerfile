FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY ./pyproject.toml uv.lock /app/

RUN apk update && apk add --no-cache git gcc musl-dev curl build-base libffi-dev openssl-dev python3-dev

RUN uv venv .venv 

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
COPY ./src /app/src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.12-alpine

COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV TZ=Asia/Seoul

RUN apk add --no-cache libpq curl postgresql-dev py3-psycopg2 

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app
COPY ./entrypoint.sh wait-for-it.sh ./
ENTRYPOINT [ "sh", "-c", ". entrypoint.sh" ]

EXPOSE 8000
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
