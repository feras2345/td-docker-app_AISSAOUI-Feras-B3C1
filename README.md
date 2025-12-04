# TD Docker – Application 3 tiers

## 1. Objectif

Mettre en place une application web 3‑tiers conteneurisée avec Docker et Docker Compose :

- **PostgreSQL** : stockage des données
- **API FastAPI** : accès aux données
- **Frontend Nginx (HTML/JS)** : affichage des données

En appliquant :
- Dockerfiles (multi‑étapes quand nécessaire)
- Docker Compose (services, réseaux, volumes, healthchecks)
- Variables d'environnement
- Quelques bonnes pratiques (utilisateur non‑root, .dockerignore, script d'automatisation, etc.)

---

## 2. Architecture

### 2.1 Fonctionnelle

- La base PostgreSQL initialise une table `items` (id, name, description) via `db/init.sql`.
- L'API (FastAPI) expose au minimum :
  - `GET /status` : statut simple de l'API.
  - `GET /items` : liste des items issus de la base.
- Le frontend :
  - appelle l'API (`/status` et `/items`),
  - affiche l'état de l'API et la liste des items.

### 2.2 Schéma technique simplifié

```text
Navigateur
   │
   ▼
Front (Nginx) - port 3000 → API (FastAPI) - port 8000 → PostgreSQL - port 5432
                 (tous sur le même réseau Docker via docker-compose)
```

---

## 3. Contenu du projet

- `docker-compose.yml` : définition des services `db`, `api`, `front` (+ réseaux, volumes, healthchecks).
- `db/init.sql` : création de la base, de la table `items` et insertion de données.
- `api/app.py` : API FastAPI (routes `/status`, `/items`, connexion DB).
- `api/requirements.txt` : dépendances Python.
- `api/tests/test_api.py` : quelques tests automatiques sur les routes `/status` et `/items`.
- `api/Dockerfile` : image API (Python slim, utilisateur non‑root, port 8000).
- `front/index.html`, `styles.css` : page web statique + logique JS (fetch vers l'API).
- `front/default.conf` : configuration Nginx.
- `front/Dockerfile` : build/copie du front + image finale Nginx.
- `.env.example` : exemple de configuration d'environnement.
- `.dockerignore` : exclusion des fichiers inutiles (node_modules, .git, etc.).
- `deploy.sh` : script d'automatisation (build + déploiement).

---

## 4. Docker Compose

Points principaux du `docker-compose.yml` :

- **Service `db`** :
  - Image `postgres`.
  - Variables d'environnement (DB, user, password) chargées depuis `.env`.
  - Volume persistant `postgres_data`.
  - Montage de `db/init.sql` dans `/docker-entrypoint-initdb.d/`.
  - Healthcheck via `pg_isready`.

- **Service `api`** :
  - Build depuis `./api`.
  - Variables d'environnement DB (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) via `.env`.
  - Port exposé `8000:8000`.
  - `depends_on` avec condition `service_healthy` sur `db`.
  - Healthcheck sur `/status`.

- **Service `front`** :
  - Build depuis `./front`.
  - `depends_on` sur `api` (service healthy).
  - Port exposé `3000:80`.

- **Volumes** :
  - `postgres_data` pour persister les données PostgreSQL.

---

## 5. Variables d'environnement

À partir de `.env.example`, créer un fichier `.env` :

```dotenv
POSTGRES_DB=td_docker
POSTGRES_USER=td_user
POSTGRES_PASSWORD=td_password

DB_HOST=db
DB_PORT=5432
DB_NAME=td_docker
DB_USER=td_user
DB_PASSWORD=td_password
```

Utilisation :

- `db` lit `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
- `api` utilise `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` pour se connecter à PostgreSQL.

---

## 6. Frontend

Le front (servi par Nginx sur `http://localhost:3000`) :

- récupère le statut de l'API :

  ```js
  fetch('http://localhost:8000/status')
  ```

- récupère la liste des items :

  ```js
  fetch('http://localhost:8000/items')
  ```

- affiche dans la page :
  - le statut de l'API (par ex. "OK"),
  - la liste des items (id, name, description).

---

## 7. Lancement et tests

### 7.1 Déploiement

Depuis la racine du projet :

```bash
docker compose down          # optionnel : arrêter une ancienne stack
git pull                     # mettre à jour le code

cp .env.example .env         # puis adapter les valeurs si besoin

./deploy.sh                  # script d'automatisation (build + up -d)
```

### 7.2 Vérifications

```bash
docker compose ps
```

Les services `db`, `api`, `front` doivent être en `healthy` après quelques secondes.

Tests API manuels :

```bash
curl http://localhost:8000/status
curl http://localhost:8000/items
```

Tests automatisés (pytest) :

```bash
cd api
pytest -v
```

Test frontend (navigateur) :

- Aller sur : `http://localhost:3000`
- Vérifier :
  - l'affichage du statut de l'API,
  - l'affichage de la liste des items issus de la base.

---

## 8. Automatisation et améliorations possibles

- `deploy.sh` :
  - vérifie la configuration (`docker compose config`),
  - construit les images (`docker compose build`),
  - lance les services (`docker compose up -d`),
  - affiche l'état des services (`docker compose ps`).

Améliorations possibles :
- Étendre les routes de l'API (CRUD complet).
- Rendre le front plus interactif (formulaires pour ajouter/modifier les items).
- Étendre les tests automatisés (cas d'erreur, scénarios DB complets).
- Pousser les images dans un registre Docker.
