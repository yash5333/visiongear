#!/bin/bash
# ─────────────────────────────────────────────────────────
#  VisionGear — Quick Setup Script
# ─────────────────────────────────────────────────────────
set -e

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   VisionGear — Photography & Videography ║"
echo "║         Project Setup Script             ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🗄️  Setting up database..."
python manage.py makemigrations users store orders
python manage.py migrate

echo ""
echo "🌱 Seeding sample data..."
python manage.py seed_data

echo ""
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || echo "   (skipped — DEBUG mode uses static files directly)"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         ✅  Setup Complete!              ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Start server:  python manage.py runserver"
echo "║  Visit:         http://127.0.0.1:8000   ║"
echo "║  Admin:         http://127.0.0.1:8000/admin"
echo "║  Credentials:   admin / admin123        ║"
echo "╚══════════════════════════════════════════╝"
echo ""
