#!/bin/bash

# Deploy GitHub Actions for Standardized Modules Framework Testing
# Target Repository: https://github.com/Jita81/CODETEST
# Sister Action to: https://github.com/Jita81/CODEREVIEW

set -e

echo "🚀 Deploying Standardized Modules Framework Testing Actions to CODETEST"
echo "Sister repository to CODEREVIEW for comprehensive CI/CD"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git branch -M main
fi

# Add remote if it doesn't exist
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "Adding remote origin..."
    git remote add origin https://github.com/Jita81/CODETEST.git
else
    echo "Remote origin already exists"
    git remote set-url origin https://github.com/Jita81/CODETEST.git
fi

# Stage all files
echo "Staging files for deployment..."
git add .

# Create commit
echo "Creating commit..."
git commit -m "🚀 Deploy Standardized Modules Framework Testing Actions

- Complete GitHub Actions suite for module testing
- Support for CORE, INTEGRATION, SUPPORTING, TECHNICAL modules
- Docker and Kubernetes testing workflows
- Integration with CODEREVIEW for comprehensive CI/CD
- Multi-Python version testing (3.8-3.12)
- Performance, security, and quality validation
- Framework-specific structure validation

Sister action to CODEREVIEW repository for complete development workflow."

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main --force

echo "✅ Successfully deployed to https://github.com/Jita81/CODETEST"
echo ""
echo "🔗 Integration with CODEREVIEW:"
echo "   - CODEREVIEW: AI-powered code quality analysis"
echo "   - CODETEST: Standardized module framework testing"
echo ""
echo "📋 Next steps:"
echo "1. Configure repository secrets if needed"
echo "2. Enable GitHub Actions in repository settings"
echo "3. Test workflows with a sample module"
echo "4. Set up branch protection rules"
