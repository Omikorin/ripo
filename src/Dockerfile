FROM python:3.11-slim-bookworm AS builder

RUN apt-get update && apt-get install -y \
    gfortran \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

EXPOSE 5050

ENTRYPOINT ["python3", "webapp.py"]

FROM builder as dev-envs

RUN <<EOF
apt-get update
apt-get install git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
