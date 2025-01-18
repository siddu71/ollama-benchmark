# llm-benchmark (ollama-benchmark)

LLM Benchmark for Throughput via Ollama (Local LLMs)

## Installation prerequisites

Working [Ollama](https://ollama.com) installation.

## Usage Steps

```
cd ollama-benchmark
```

update allowed models in in your corresponding modes file

```
(ollama) siddu@ubuntu-homelab:~/ollama-benchmark$ tree llm_benchmark/data/
llm_benchmark/data/
├── benchmark1.yml
├── benchmark_models_16gb_ram.yml
├── benchmark_models_2gb_ram.yml
├── benchmark_models_3gb_ram.yml
├── benchmark_models_4gb_ram.yml
├── benchmark_models_8gb_ram.yml

```
Add models you want to benchmarks into relavant file based on you gpu vram :: ~/ollama-benchmark/llm_benchmark/data/benchmark_models_16gb_ram.yml

```
 l/d/benchmark_models_16gb_ram.yml
 # Author: Jason Chuang
 # License: MIT
 version: 1.0
 models:
   - model: qwen2.5-coder:32b
   - model: qwen2.5-coder:14b
     #- model: deepseek-coder-v2-fixed:latest
     #- model: phi4:latest
     #- model: qwen2.5:14b
     #- model: qwen2.5:7b
     #- model: qwq:32b
     #- model: phi3:3.8b
     #- model: qwen2:7b
     #- model: gemma2:9b
     #- model: mistral:7b
     #- model: llama3.1:8b
     #- model: llava:7b
     #- model: llava:13b
```

Add models and corresponding prompts into ~/ollama-benchmark/llm_benchmark/data/benchmark1.yml

```
 l/d/benchmark1.yml
 # Author: Jason Chuang
 # License: MIT
 version: 1.0
 modeltypes:
   - type: chat
     models:
       - model: qwen2.5-coder:32b
       - model: qwen2.5-coder:14b
       #- model: deepseek-coder-v2-fixed:latest
       #- model: phi4:latest
       #- model: qwen2.5:14b
       #- model: qwen2.5:7b
     prompts:
       - prompt: Develop a web scraper using BeautifulSoup and Python to extract product information from an e-commerce website.
         keywords: python, web scraping, beautifulsoup
       - prompt: Write a Go program that uses the Gorilla WebSocket library to establish a real-time communication channel between a client and server.
         keywords: go, websockets, gorilla
       - prompt: Implement a Ruby on Rails API using Active Record to manage a database of users, including authentication and authorization features.
         keywords: ruby, rails, api, active record
       - prompt: Create a Node.js application that uses the Express framework to build a RESTful API for managing books in a library, including CRUD operations.
         keywords: nodejs, express, restful api
       - prompt: Develop a Java Spring Boot application that integrates with a MySQL database to manage employee information, including data validation and security features.
         keywords: java, spring boot, mysql
       - prompt: Implement a Flask API using SQLAlchemy to manage a database of products, including data modeling and serialization.
         keywords: python, flask, sqlalchemy
```

Make sure model you want to benchmark is on both benchmark1.yml and benchmark_models_16gb_ram.yml


cd into ollama-benchmark dir and run the following command to start the benchmark

```
(ollama) siddu@ubuntu-homelab:~/ollama-benchmark$ python -m llm_benchmark.main run
```


