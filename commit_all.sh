#!/bin/bash

# Sanketavani - Individual File Commit Script
# This script commits each modified file separately with descriptive messages

cd "$(dirname "$0")"

echo "🚀 Starting individual file commits for Sanketavani..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Commit README files
git add README.md && git commit -m "docs: Add comprehensive README with Sanketavani branding" && echo "✅ README.md committed"
git add SETUP.md && git commit -m "docs: Add setup instructions" && echo "✅ SETUP.md committed"
git add QUICK_START.md && git commit -m "docs: Add quick start guide" && echo "✅ QUICK_START.md committed"

# Commit Python/Django files
git add requirements.txt && git commit -m "build: Add Python dependencies" && echo "✅ requirements.txt committed"
git add setup.py && git commit -m "build: Add setup.py for package installation" && echo "✅ setup.py committed"
git add manage.py && git commit -m "feat: Add Django management script" && echo "✅ manage.py committed"

# Commit Django app files
git add A2SL/settings.py && git commit -m "config: Configure Django settings with CORS and disabled CSRF for API" && echo "✅ A2SL/settings.py committed"
git add A2SL/urls.py && git commit -m "feat: Add URL routing with API endpoint" && echo "✅ A2SL/urls.py committed"
git add A2SL/views.py && git commit -m "feat: Add views with NLP processing and API endpoint" && echo "✅ A2SL/views.py committed"
git add A2SL/wsgi.py && git commit -m "config: Add WSGI configuration" && echo "✅ A2SL/wsgi.py committed"
git add A2SL/asgi.py && git commit -m "config: Add ASGI configuration" && echo "✅ A2SL/asgi.py committed"

# Commit shell scripts
git add start_server.sh && git commit -m "script: Add Django server start script with port cleanup" && echo "✅ start_server.sh committed"
git add restart.sh && git commit -m "script: Add server restart script" && echo "✅ restart.sh committed"
git add start_all.sh && git commit -m "script: Add script to start both Django and Next.js servers" && echo "✅ start_all.sh committed"
git add start.sh && git commit -m "script: Add generic start script" && echo "✅ start.sh committed"

# Commit Next.js files
git add voice_to_isl/.gitignore && git commit -m "config: Add Next.js .gitignore" && echo "✅ voice_to_isl/.gitignore committed"
git add voice_to_isl/package.json && git commit -m "build: Add Next.js dependencies with Lenis smooth scroll" && echo "✅ voice_to_isl/package.json committed"
git add voice_to_isl/tsconfig.json && git commit -m "config: Add TypeScript configuration" && echo "✅ voice_to_isl/tsconfig.json committed"
git add voice_to_isl/next.config.ts && git commit -m "config: Add Next.js configuration" && echo "✅ voice_to_isl/next.config.ts committed"
git add voice_to_isl/postcss.config.mjs && git commit -m "config: Add PostCSS configuration" && echo "✅ voice_to_isl/postcss.config.mjs committed"
git add voice_to_isl/tailwind.config.ts && git commit -m "config: Add Tailwind CSS configuration" && echo "✅ voice_to_isl/tailwind.config.ts committed"

# Commit Next.js app files
git add voice_to_isl/app/globals.css && git commit -m "style: Add premium global styles with smooth scrolling and animations" && echo "✅ voice_to_isl/app/globals.css committed"
git add voice_to_isl/app/layout.tsx && git commit -m "feat: Add root layout with SEO metadata and Sanketavani branding" && echo "✅ voice_to_isl/app/layout.tsx committed"
git add voice_to_isl/app/page.tsx && git commit -m "feat: Add premium home page with hero section and features" && echo "✅ voice_to_isl/app/page.tsx committed"
git add voice_to_isl/app/icon.svg && git commit -m "assets: Add custom favicon with wave pattern design" && echo "✅ voice_to_isl/app/icon.svg committed"
git add voice_to_isl/app/apple-touch-icon.png && git commit -m "assets: Add Apple touch icon" && echo "✅ voice_to_isl/app/apple-touch-icon.png committed"

# Commit Next.js pages
git add voice_to_isl/app/converter/page.tsx && git commit -m "feat: Add converter page with dual video crossfade transitions" && echo "✅ voice_to_isl/app/converter/page.tsx committed"
git add voice_to_isl/app/about/page.tsx && git commit -m "feat: Add about page with team information" && echo "✅ voice_to_isl/app/about/page.tsx committed"
git add voice_to_isl/app/contact/page.tsx && git commit -m "feat: Add contact page" && echo "✅ voice_to_isl/app/contact/page.tsx committed"

# Commit components
git add voice_to_isl/components/Navbar.tsx && git commit -m "feat: Add responsive navbar with mobile menu" && echo "✅ voice_to_isl/components/Navbar.tsx committed"
git add voice_to_isl/components/Footer.tsx && git commit -m "feat: Add footer component" && echo "✅ voice_to_isl/components/Footer.tsx committed"
git add voice_to_isl/components/SmoothScroll.tsx && git commit -m "feat: Add Lenis smooth scroll component" && echo "✅ voice_to_isl/components/SmoothScroll.tsx committed"

# Commit public assets
git add voice_to_isl/public/favicon.svg && git commit -m "assets: Add favicon SVG" && echo "✅ voice_to_isl/public/favicon.svg committed"
git add voice_to_isl/public/manifest.json && git commit -m "config: Add PWA manifest" && echo "✅ voice_to_isl/public/manifest.json committed"
git add voice_to_isl/public/robots.txt && git commit -m "seo: Add robots.txt" && echo "✅ voice_to_isl/public/robots.txt committed"
git add voice_to_isl/public/sitemap.xml && git commit -m "seo: Add sitemap.xml" && echo "✅ voice_to_isl/public/sitemap.xml committed"

# Commit documentation
git add voice_to_isl/README.md && git commit -m "docs: Add Next.js app README" && echo "✅ voice_to_isl/README.md committed"
git add voice_to_isl/UPGRADE_SUMMARY.md && git commit -m "docs: Add upgrade summary documentation" && echo "✅ voice_to_isl/UPGRADE_SUMMARY.md committed"

# Commit NLTK data and assets (as directories)
git add nltk_data/ && git commit -m "data: Add NLTK tokenizer data" && echo "✅ nltk_data/ committed"
git add assets/ && git commit -m "assets: Add ISL video animations" && echo "✅ assets/ committed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ All files committed successfully!"
echo ""
echo "📊 Commit summary:"
git log --oneline -20
echo ""
echo "🚀 Ready to push to remote!"
echo "Run: git push origin main"
