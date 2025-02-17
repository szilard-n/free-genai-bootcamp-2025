## Exmaple Request

```sh
curl -X POST http://localhost:8000/v1/example_service \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
        {
            "role": "user",
            "content": "Say hello!"
        }
    ],
    "model": "llama3.2:1b",
    "temperature": 0.7
}'
```

## Exmaple Response

```json
{
   "id":"chatcmpl-eUtorGV6chMCvroXcL7Yca",
   "object":"chat.completion",
   "created":1739796902,
   "model":"llama3.2:1b",
   "choices":[
      {
         "index":0,
         "message":{
            "role":"assistant",
            "content":"Hello! How can I assist you today?"
         },
         "finish_reason":"stop",
         "metadata":null
      }
   ],
   "usage":{
      "prompt_tokens":0,
      "total_tokens":0,
      "completion_tokens":0
   }
}
```



