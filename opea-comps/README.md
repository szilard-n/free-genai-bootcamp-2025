# Ollama Chat Service with opea-comps

A microservice built using the opea-comps framework that provides a chat completion API interface to Ollama's LLM models. The service:

- Acts as a bridge between clients and Ollama's LLM service
- Provides an OpenAI-compatible chat completion API endpoint
- Uses the opea-comps framework to handle service orchestration and request routing
- Runs in Docker containers for easy deployment and scaling

## Running Ollama Third-Party Service

## Prerequisites

- Docker
- Docker Compose

## Running the Service

1. Create a `.env` file with the following variables:
    - `LLM_SERVICE_PORT`: The port for the Ollama service (default: 11434)
    - `LLM_MODEL_ID`: The ID of the model to use (e.g., llama3.2:1b)
    - `MEGA_SERVICE_PORT`: The port for the mega-service (default: 8888)
    - `VOLUME_NAME`: The name of the volume to store Ollama models
    - `NO_PROXY`: Optional proxy configuration

2. Run the service with `docker compose up -d`.

## Using the Service

The mega-service is available at `http://localhost:${MEGA_SERVICE_PORT}`. You can interact with it using the `/v1/example_service` endpoint.

### Example Request

```sh
curl -X POST http://localhost:8888/v1/example_service \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
        {
            "role": "user",
            "content": "Say hello!"
        }
    ],
    "model": "llama3.2:1b"
}'
```

### Example Response

```json
{
   "id": "chatcmpl-xxx",
   "object": "chat.completion",
   "created": 1234567890,
   "model": "llama3.2:1b",
   "choices": [
       {
           "index": 0,
           "message": {
               "role": "assistant",
               "content": "Hello! How can I assist you today?"
           },
           "finish_reason": "stop"
       }
   ],
   "usage": {
       "prompt_tokens": 0,
       "completion_tokens": 0,
       "total_tokens": 0
   }
}
```

The service uses Ollama's chat completion API internally and follows a similar format to OpenAI's chat completion API.
