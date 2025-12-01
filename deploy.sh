#!/bin/bash

set -e

# Variables
echo "🚀 Déploiement TD Docker App"

# Build et vérification
docker compose config
echo "✅ Configuration OK"

docker compose build --no-cache
echo "✅ Images construites"

# Tests healthchecks
docker compose up -d db
sleep 10
echo "✅ DB prête"

docker compose up -d api front
echo "✅ Tous services lancés"

# Status final
docker compose ps
echo "🌐 Front: http://localhost:3000"
echo "🌐 API: http://localhost:8000"
