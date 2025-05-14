vllm serve $1 \
  --host 127.0.0.1 \
  --port 11451 \
  --enable-reasoning \
  --max-model-len 4096 \
  --reasoning-parser deepseek_r1 \
  --served-model-name qwen3-4b \
  --enable-prefix-caching \
  --enable-auto-tool-choice \
  --tool-call-parser hermes
