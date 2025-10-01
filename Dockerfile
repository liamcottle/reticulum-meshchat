# Build arguments
ARG NODE_VERSION=20
ARG NODE_ALPINE_SHA256=sha256:6a91081a440be0b57336fbc4ee87f3dab1a2fd6f80cdb355dcf960e13bda3b59
ARG PYTHON_VERSION=3.11
ARG PYTHON_ALPINE_SHA256=sha256:822ceb965f026bc47ee667e50a44309d2d81087780bbbf64f2005521781a3621

# Build the frontend
FROM node:${NODE_VERSION}-alpine@${NODE_ALPINE_SHA256} AS build-frontend

WORKDIR /src

# Copy required source files
COPY *.json .
COPY *.js .
COPY src/frontend ./src/frontend

# Install NodeJS deps, exluding electron
RUN npm install --omit=dev && \
  npm run build-frontend

# Main app build
FROM python:${PYTHON_VERSION}-alpine@${PYTHON_ALPINE_SHA256}

WORKDIR /app

# Install Python deps
COPY ./requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
    pip install -r requirements.txt && \
    apk del .build-deps

# Copy prebuilt frontend
COPY --from=build-frontend /src/public public

# Copy other required source files
COPY *.py .
COPY src/__init__.py ./src/__init__.py
COPY src/backend ./src/backend
COPY *.json .

CMD ["python", "meshchat.py", "--host=0.0.0.0", "--reticulum-config-dir=/config/.reticulum", "--storage-dir=/config/.meshchat", "--headless"]
