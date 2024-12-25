# Build the frontend
FROM node:20-bookworm-slim AS build-frontend

WORKDIR /src

COPY *.json .
COPY *.js .
COPY src/frontend ./src/frontend

RUN npm install --omit=dev && \
  npm run build-frontend

# Main app build
FROM python:3.11-bookworm

WORKDIR /app

COPY ./requirements.txt .
COPY --from=build-frontend /src/public public

RUN pip install -r requirements.txt

COPY *.py .
COPY src/__init__.py ./src/__init__.py
COPY src/backend ./src/backend
COPY *.json .

CMD ["python", "meshchat.py", "--host=0.0.0.0", "--reticulum-config-dir=/config/.reticulum", "--storage-dir=/config/.meshchat", "--headless"]

