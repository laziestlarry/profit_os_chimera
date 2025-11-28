#!/bin/bash
# Deployment script for Profit OS Chimera

set -e

VERSION="0.1.0"
ENV=${1:-production}

echo "🚀 Deploying Profit OS Chimera v${VERSION} to ${ENV}"

# Build Docker images
echo "Building Docker images..."
docker build -f infrastructure/docker/Dockerfile -t profit-os-chimera-api:${VERSION} .
docker build -f infrastructure/docker/Dockerfile.streamlit -t profit-os-chimera-frontend:${VERSION} .

# Tag as latest
docker tag profit-os-chimera-api:${VERSION} profit-os-chimera-api:latest
docker tag profit-os-chimera-frontend:${VERSION} profit-os-chimera-frontend:latest

# Push to registry (configure your registry)
# docker push your-registry/profit-os-chimera-api:${VERSION}
# docker push your-registry/profit-os-chimera-frontend:${VERSION}

# Deploy with docker-compose
echo "Deploying with docker-compose..."
cd infrastructure/docker
docker-compose up -d

echo "✅ Deployment complete!"
echo "API: http://localhost:8000"
echo "Frontend: http://localhost:8501"



