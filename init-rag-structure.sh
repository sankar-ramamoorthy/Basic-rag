#!/bin/bash

services=("ingestion-service" "vector-store-service" "llm-service" "rag-orchestrator")
common_dirs=("common/utils")
root_files=("README.md" ".gitignore" "docker-compose.yml" ".env.example")

# Create root files
for file in "${root_files[@]}"; do
  touch "$file"
done

# Create common dirs
for dir in "${common_dirs[@]}"; do
  mkdir -p "$dir"
  touch "$dir/__init__.py"
done

# Create service directories and files
for service in "${services[@]}"; do
  mkdir -p "$service/app"
  touch "$service/app/__init__.py"
  touch "$service/app/main.py"
  touch "$service/pyproject.toml"
  touch "$service/Dockerfile"
  touch "$service/.gitignore"
  touch "$service/README.md"
done

echo "✅ Project structure created successfully."
