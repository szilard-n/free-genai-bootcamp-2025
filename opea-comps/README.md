# Running Ollama Third-Party Service

## Prerequisites

- Docker
- Docker Compose

## Running the Service

1. Create a `.env` file with the following variables:
    - `CONTAINER_NAME`: The name of the container to use.
    - `HOST_PORT`: The port to run the service on.
    - `LLM_ENDPOINT_PORT`: The port to run the LLM endpoint on.
    - `LLM_MODEL_ID`: The ID of the model to use.
    - `NO_PROXY`: The proxy to use.
    - `VOLUME_NAME`: The name of the volume to use.

2. Run the service with `docker compose up -d`.

### Example `.env` file

```
CONTAINER_NAME=ollama-instance
HOST_PORT=11434
LLM_ENDPOINT_PORT=8008
LLM_MODEL_ID=llama3.2:1b
VOLUME_NAME=ollama-instance
```

## Accessing the Service

The service will be available at `http://localhost:${HOST_PORT}`.

The service can be access by sending requests to the `/api/generate` endpoint.

### Pull a Model

```
curl http://localhost:11434/api/pull -d '{
  "model": "llama3.2:1b"
}'
```

### Use the Model

```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt":"Why is the sky blue?"
}'
```


