from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo,
)
from comps.cores.mega.constants import ServiceType
from comps import MicroService, ServiceOrchestrator
from fastapi import HTTPException
import os
import aiohttp

LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "localhost")
LLM_SERVICE_PORT = os.getenv("LLM_SERVICE_PORT", 11434)


class ExampleService:
    def __init__(self, host="0.0.0.0", port=8888):
        self.host = host
        self.port = port
        self.endpoint = "/v1/example_service"
        self.megaservice = ServiceOrchestrator()
        self.ollama_url = f"http://{LLM_SERVICE_HOST_IP}:{LLM_SERVICE_PORT}/api/chat"

    def add_remote_service(self):
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )
        self.megaservice.add(llm)

    def start(self):
        self.service = MicroService(
            self.__class__.__name__,
            host=self.host,
            port=self.port,
            endpoint=self.endpoint,
            input_datatype=ChatCompletionRequest,
            output_datatype=ChatCompletionResponse,
        )

        self.service.add_route(
            self.endpoint, self.handle_request, methods=["POST"])
        self.service.start()

    async def handle_request(self, request: ChatCompletionRequest) -> ChatCompletionResponse:

        try:
            print("Received request:", request)

            # Create Ollama-compatible request
            ollama_request = {
                "model": request.model or "llama3.2:1b",
                "messages": request.messages,
                "stream": False
            }

            print("Sending to Ollama:", ollama_request)

            # Make direct request to Ollama
            async with aiohttp.ClientSession() as session:
                async with session.post(self.ollama_url, json=ollama_request) as resp:
                    response_data = await resp.json()
                    print("Raw Ollama response:", response_data)
                    response_text = response_data.get(
                        'message', {}).get('content', '')

            print("Final response text:", response_text)

            response = ChatCompletionResponse(
                model=getattr(request, 'model', "llama3.2:1b"),
                choices=[
                    ChatCompletionResponseChoice(
                        index=0,
                        message=ChatMessage(
                            role="assistant",
                            content=response_text
                        ),
                        finish_reason="stop"
                    )
                ],
                usage=UsageInfo(
                    prompt_tokens=0,
                    completion_tokens=0,
                    total_tokens=0
                )
            )

            return response

        except Exception as e:
            print(f"Error in handle_request: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    service = ExampleService()
    service.add_remote_service()
    service.start()
