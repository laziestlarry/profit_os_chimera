#!/bin/bash
# Initialize GitHub repository for Profit OS Chimera

set -e

echo "🚀 Initializing GitHub repository for Profit OS Chimera v0.1.0"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files
echo "Adding files to git..."
git add .

# Create initial commit
echo "Creating initial commit..."
git commit -m "Initial commit: Profit OS Chimera v0.1.0_Publish - Production Ready

- Complete REST API (FastAPI)
- Database layer (SQLAlchemy)
- Frontend dashboard (Streamlit)
- Docker containerization
- CI/CD pipeline
- Revenue assets (Fiverr gig + Shopify product)
- Full documentation

Status: Production Ready ✅"

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  No remote repository configured."
    echo "To add a remote repository, run:"
    echo "  git remote add origin <your-repo-url>"
    echo "  git push -u origin main"
    echo ""
else
    echo "Remote repository found:"
    git remote -v
    echo ""
    read -p "Push to remote? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push -u origin main
        echo "✅ Pushed to remote repository"
    fi
fi

echo ""
echo "✅ GitHub repository initialized!"
echo ""
echo "Next steps:"
echo "1. Create repository on GitHub (if not exists)"
echo "2. Add remote: git remote add origin <repo-url>"
echo "3. Push: git push -u origin main"
echo "4. Deploy: ./scripts/deploy.sh production"



