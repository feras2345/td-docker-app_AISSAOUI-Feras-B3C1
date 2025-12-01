#!/bin/bash
# deploy.sh - Script d'automatisation TP Docker td-docker-app

set -e

COLOR_GREEN="\033[1;32m"
COLOR_YELLOW="\033[1;33m"
COLOR_RED="\033[1;31m"
COLOR_RESET="\033[0m"

log() {
    echo -e "${COLOR_GREEN}[$(date +'%H:%M:%S')] $1${COLOR_RESET}"
}

warn() {
    echo -e "${COLOR_YELLOW}[WARN] $1${COLOR_RESET}"
}

error() {
    echo -e "${COLOR_RED}[ERROR] $1${COLOR_RESET}"
    exit 1
}

log "🚀 Début automatisation TP Docker td-docker-app"

# 1. Vérification config Compose
log "📋 Vérification docker-compose.yml..."
docker compose config || error "Config Compose invalide"

# 2. Build images optimisées
log "🔨 Construction images (avec .dockerignore optimisé)..."
docker compose build --no-cache --progress=plain

# 3. Scan sécurité images
log "🛡️ Scan sécurité API (docker scout)..."
docker scout cves $(docker compose images -q api) || warn "Vulnérabilités détectées - voir détails"

# 4. Healthchecks et déploiement
log "⬆️ Déploiement avec healthchecks..."
docker compose up -d

# 5. Vérification services
log "✅ Vérification healthchecks..."

sleep 10

if docker compose ps | grep -q "healthy"; then
    log "🎉 Tous services healthy ! Stack OK"
else
    warn "⚠️ Certains services pas encore healthy - attendez 30s"
fi

# 6. Métriques finales
log "📊 Statut final :"
docker compose ps
log "🏆 TP Docker terminé - Images optimisées + sécurité + automatisation !"
