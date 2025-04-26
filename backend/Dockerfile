# https://docs.astral.sh/uv/guides/integration/aws-lambda/#deploying-a-docker-image
FROM ghcr.io/astral-sh/uv:0.6.17 AS uv
# First, bundle the dependencies into the task root.
FROM public.ecr.aws/docker/library/python:3.11 AS builder

# Install Rust for building pydantic-core
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Enable bytecode compilation, to improve cold-start performance.
ENV UV_COMPILE_BYTECODE=1
# Disable installer metadata, to create a deterministic layer.
ENV UV_NO_INSTALLER_METADATA=1
# Enable copy mode to support bind mount caching.
ENV UV_LINK_MODE=copy

ENV LAMBDA_TASK_ROOT=/var/task
WORKDIR ${LAMBDA_TASK_ROOT}

# Bundle the dependencies into the Lambda task root via `uv pip install --target`.
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt && \
    uv pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Final stage
FROM public.ecr.aws/docker/library/python:3.11-slim
ENV LAMBDA_TASK_ROOT=/var/task
ENV PYTHONPATH=${LAMBDA_TASK_ROOT}
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the Lambda Web Adapter in the final stage
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter
ENV AWS_LWA_INVOKE_MODE=BUFFERED
# ENV AWS_LWA_PORT=8000

# Copy dependencies from builder
COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}

# Copy project files to the Docker image
COPY app/ ${LAMBDA_TASK_ROOT}/app
COPY main.py ${LAMBDA_TASK_ROOT}/
    
# Set the CMD to lambda handler replace in the lambda's "cmd" property
CMD ["python3", "main.py"]