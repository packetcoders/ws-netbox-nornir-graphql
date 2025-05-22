FROM coder-ide:latest

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip curl ca-certificates && \
    ln -sf /usr/bin/python3 /usr/local/bin/python && \
    ln -sf /usr/bin/pip3 /usr/local/bin/pip && \
    rm -rf /var/lib/apt/lists/*

RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin

WORKDIR /home/coder/project
COPY . .

RUN chown -R coder:coder /home/coder/project

USER coder

# Add venv and uv install path to PATH
ENV PATH=/home/coder/project/.venv/bin:/home/coder/.local/bin:$PATH

# Install uv (into ~/.local/bin)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment in .venv
RUN uv venv

# Install project dependencies using uv pip
RUN uv pip install -r requirements.txt

