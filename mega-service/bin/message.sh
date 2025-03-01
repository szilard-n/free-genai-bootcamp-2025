#!/bin/bash

curl -X POST http://0.0.0.0:8888/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Hello, how are you?"
      }
    ]
  }'