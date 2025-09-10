#!/bin/bash

# Simple test script to verify the PoC setup
set -e

echo "🔍 Keycloak + Python API PoC - Basic Tests"
echo "=========================================="

# Test 1: Check if all required files exist
echo "✅ Test 1: Checking project structure..."
required_files=(
    "docker-compose.yml"
    "api/app.py"
    "api/requirements.txt"
    "api/Dockerfile"
    "api/static/index.html"
    "keycloak/demo-realm.json"
    ".gitignore"
    "README.md"
)

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "   ✓ $file exists"
    else
        echo "   ✗ $file missing"
        exit 1
    fi
done

# Test 2: Validate docker-compose syntax
echo ""
echo "✅ Test 2: Validating Docker Compose configuration..."
if docker compose config > /dev/null 2>&1; then
    echo "   ✓ Docker Compose configuration is valid"
else
    echo "   ✗ Docker Compose configuration has errors"
    exit 1
fi

# Test 3: Check Python syntax
echo ""
echo "✅ Test 3: Validating Python code syntax..."
if python3 -m py_compile api/app.py; then
    echo "   ✓ Python API code syntax is valid"
else
    echo "   ✗ Python API code has syntax errors"
    exit 1
fi

# Test 4: Check if required Python packages are listed
echo ""
echo "✅ Test 4: Checking Python dependencies..."
required_packages=("fastapi" "uvicorn" "python-keycloak" "python-jose")
for package in "${required_packages[@]}"; do
    if grep -q "$package" api/requirements.txt; then
        echo "   ✓ $package is listed in requirements.txt"
    else
        echo "   ✗ $package is missing from requirements.txt"
        exit 1
    fi
done

# Test 5: Validate Keycloak realm JSON
echo ""
echo "✅ Test 5: Validating Keycloak realm configuration..."
if python3 -c "import json; json.load(open('keycloak/demo-realm.json'))" 2>/dev/null; then
    echo "   ✓ Keycloak realm JSON is valid"
else
    echo "   ✗ Keycloak realm JSON has syntax errors"
    exit 1
fi

# Test 6: Check HTML syntax (basic)
echo ""
echo "✅ Test 6: Basic HTML validation..."
if grep -q "<!DOCTYPE html>" api/static/index.html && grep -q "</html>" api/static/index.html; then
    echo "   ✓ HTML structure looks valid"
else
    echo "   ✗ HTML structure appears invalid"
    exit 1
fi

echo ""
echo "🎉 All basic tests passed!"
echo ""
echo "📋 Next steps:"
echo "   1. Run: docker compose up -d"
echo "   2. Wait for services to start (2-3 minutes)"
echo "   3. Visit: http://localhost:8000"
echo "   4. Login with: demouser / password123"
echo ""
echo "📚 For more details, see README.md"