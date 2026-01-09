#!/bin/bash
# validate-installation.sh - Frontend Dependencies Validation Script
#
# Purpose: Comprehensive post-install validation for frontend dependencies
# Usage: cd frontend && bash scripts/validate-installation.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0

# Helper functions
check_pass() {
  echo -e "${GREEN}✓${NC} $1"
  ((CHECKS_PASSED++))
}

check_fail() {
  echo -e "${RED}❌${NC} $1"
  ((CHECKS_FAILED++))
}

check_warn() {
  echo -e "${YELLOW}⚠️${NC}  $1"
}

echo "=== Frontend Dependencies Validation ==="
echo ""

# Check 1: Verify we're in frontend directory
if [ ! -f "package.json" ]; then
  check_fail "Not in frontend directory (package.json not found)"
  exit 1
fi
check_pass "Running in frontend directory"

# Check 2: Verify node_modules exists
if [ ! -d "node_modules" ]; then
  check_fail "node_modules/ directory not found"
  echo "Run: npm install"
  exit 1
fi
check_pass "node_modules/ directory exists"

# Check 3: Verify critical production dependencies
echo ""
echo "Checking production dependencies..."
CRITICAL_DEPS=("next" "react" "react-dom" "axios" "better-auth" "zod")

for pkg in "${CRITICAL_DEPS[@]}"; do
  if [ -d "node_modules/$pkg" ]; then
    check_pass "$pkg installed"
  else
    check_fail "$pkg missing"
  fi
done

# Check 4: Verify TypeScript types
echo ""
echo "Checking TypeScript type definitions..."
TYPE_DEPS=("@types/node" "@types/react" "@types/react-dom")

for pkg in "${TYPE_DEPS[@]}"; do
  if [ -d "node_modules/$pkg" ]; then
    check_pass "$pkg installed"
  else
    check_fail "$pkg missing"
  fi
done

# Check 5: Verify development tools
echo ""
echo "Checking development dependencies..."
DEV_DEPS=("typescript" "tailwindcss" "eslint" "prettier")

for pkg in "${DEV_DEPS[@]}"; do
  if [ -d "node_modules/$pkg" ]; then
    check_pass "$pkg installed"
  else
    check_fail "$pkg missing"
  fi
done

# Check 6: Verify package.json scripts exist
echo ""
echo "Checking package.json scripts..."
REQUIRED_SCRIPTS=("dev" "build" "start" "lint" "type-check")

for script in "${REQUIRED_SCRIPTS[@]}"; do
  if grep -q "\"$script\":" package.json; then
    check_pass "Script '$script' defined"
  else
    check_fail "Script '$script' missing"
  fi
done

# Check 7: Run TypeScript compilation check
echo ""
echo "Running TypeScript compilation check..."
if command -v npx &> /dev/null; then
  if npx tsc --noEmit --pretty 2>&1 | tee /tmp/tsc-output.log; then
    check_pass "TypeScript compilation passed (0 errors)"
  else
    check_fail "TypeScript compilation failed"
    echo "See errors above or in /tmp/tsc-output.log"
  fi
else
  check_warn "npx not found, skipping TypeScript check"
fi

# Check 8: Verify package-lock.json exists
echo ""
echo "Checking lockfile..."
if [ -f "package-lock.json" ]; then
  check_pass "package-lock.json exists"

  # Verify lockfile version
  LOCKFILE_VERSION=$(grep -m1 "lockfileVersion" package-lock.json | grep -oP '\d+' || echo "0")
  if [ "$LOCKFILE_VERSION" -ge "3" ]; then
    check_pass "lockfileVersion: $LOCKFILE_VERSION (npm 7+)"
  else
    check_warn "lockfileVersion: $LOCKFILE_VERSION (consider upgrading npm)"
  fi
else
  check_fail "package-lock.json missing"
  echo "Run: npm install"
fi

# Check 9: Run npm audit (production only)
echo ""
echo "Running security audit..."
if npm audit --production --audit-level=critical 2>&1 | tee /tmp/npm-audit.log | grep -q "found 0 vulnerabilities"; then
  check_pass "No critical vulnerabilities found"
elif npm audit --production --audit-level=high 2>&1 | grep -q "found 0 vulnerabilities"; then
  check_pass "No high/critical vulnerabilities found"
else
  check_warn "Vulnerabilities found - review /tmp/npm-audit.log"
  echo "Run: npm audit fix"
fi

# Check 10: Verify Node.js version
echo ""
echo "Checking environment..."
NODE_VERSION=$(node --version | grep -oP '\d+' | head -1)
if [ "$NODE_VERSION" -ge "18" ]; then
  check_pass "Node.js version: v$NODE_VERSION (>= 18)"
else
  check_fail "Node.js version: v$NODE_VERSION (upgrade to v18+)"
fi

# Check 11: Verify npm version
NPM_VERSION=$(npm --version | grep -oP '\d+' | head -1)
if [ "$NPM_VERSION" -ge "9" ]; then
  check_pass "npm version: v$NPM_VERSION (>= 9)"
else
  check_warn "npm version: v$NPM_VERSION (consider upgrading to v9+)"
fi

# Check 12: Verify disk space for node_modules
echo ""
echo "Checking disk usage..."
if command -v du &> /dev/null; then
  NODE_MODULES_SIZE=$(du -sh node_modules 2>/dev/null | awk '{print $1}')
  check_pass "node_modules/ size: $NODE_MODULES_SIZE"
else
  check_warn "du command not available, skipping size check"
fi

# Check 13: Verify critical configuration files
echo ""
echo "Checking configuration files..."
CONFIG_FILES=("tsconfig.json" "next.config.js" "tailwind.config.js" ".eslintrc.json")

for file in "${CONFIG_FILES[@]}"; do
  if [ -f "$file" ]; then
    check_pass "$file exists"
  else
    check_warn "$file missing (may be optional)"
  fi
done

# Check 14: Verify environment file
if [ -f ".env.local" ]; then
  check_pass ".env.local exists"

  # Check for required environment variables
  REQUIRED_ENV_VARS=("NEXT_PUBLIC_API_URL" "BETTER_AUTH_SECRET")
  for var in "${REQUIRED_ENV_VARS[@]}"; do
    if grep -q "^$var=" .env.local; then
      check_pass "Environment variable $var defined"
    else
      check_fail "Environment variable $var missing in .env.local"
    fi
  done
else
  check_fail ".env.local missing"
  echo "Create .env.local with required variables"
fi

# Summary
echo ""
echo "=========================================="
echo "Validation Summary:"
echo -e "${GREEN}Passed:${NC} $CHECKS_PASSED"
if [ $CHECKS_FAILED -gt 0 ]; then
  echo -e "${RED}Failed:${NC} $CHECKS_FAILED"
fi
echo "=========================================="

if [ $CHECKS_FAILED -eq 0 ]; then
  echo -e "${GREEN}✓ All checks passed! Dependencies are correctly installed.${NC}"
  exit 0
else
  echo -e "${RED}❌ Some checks failed. Review errors above.${NC}"
  exit 1
fi
