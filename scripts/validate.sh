#!/bin/bash
set -e

BASE_URL="http://localhost:8000"

echo "=== 1. HEALTH CHECK ==="
curl -sf "$BASE_URL/health"
echo ""

echo "=== 2. CREATE USER ==="
curl -X POST "$BASE_URL/users" \
-H "Content-Type: application/json" \
-d '{"username":"teste","password":"1234"}'
echo ""

echo "=== 3. LOGIN ==="
curl -X POST "$BASE_URL/login" \
-H "Content-Type: application/json" \
-d '{"username":"teste","password":"1234"}'
echo ""

echo "=== OK FINAL ==="
