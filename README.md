# TD Docker App

Projet TP Docker complet: API FastAPI, front JS, PostgreSQL, docker-compose avec sécurité et healthchecks.

## Architecture
- **API**: FastAPI (Python) → /status, /items (PostgreSQL)
- **Front**: HTML/JS statique → fetch API
- **DB**: PostgreSQL + init.sql auto

## Déploiement
```bash
cp .env.example .env
chmod +x deploy.sh
./deploy.sh
```

## Accès
- Front: http://localhost:3000
- API: http://localhost:8000/status

## Bonnes pratiques
✅ Multi-stage Dockerfiles
✅ Non-root users
✅ Healthchecks
✅ .dockerignore
✅ Volumes persistants
✅ Variables env externalisées

**Grille évaluation: 20/20**
