# Quickstart: Frontend Dependencies Installation

**Feature**: 011-frontend-backend-api (Dependencies Sub-Plan)
**Prerequisites**: Node.js 18+ and npm 9+ installed

## 🚀 Quick Install (60 seconds)

### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 2: Clean Install Dependencies

**For Production/CI**:
```bash
npm ci
```

**For Development** (when package.json changes):
```bash
npm install
```

### Step 3: Validate Installation

```bash
bash scripts/validate-installation.sh
```

**Expected Output**:
```
=== Frontend Dependencies Validation ===
✓ Running in frontend directory
✓ node_modules/ directory exists
✓ next installed
✓ react installed
✓ TypeScript compilation passed (0 errors)
✓ No critical vulnerabilities found
✓ All checks passed! Dependencies are correctly installed.
```

---

## 📋 What Gets Installed

### Production Dependencies (6 packages)

| Package | Version | Purpose |
|---------|---------|---------|
| next | ^15.1.0 | Next.js framework |
| react | ^19.0.0 | React library |
| react-dom | ^19.0.0 | React DOM rendering |
| better-auth | ^1.0.7 | Authentication library |
| axios | ^1.7.9 | HTTP client |
| zod | ^3.24.1 | Schema validation |

### Development Dependencies (17 packages)

| Package | Version | Purpose |
|---------|---------|---------|
| typescript | ^5.7.2 | TypeScript compiler |
| @types/node | ^22.10.2 | Node.js type definitions |
| @types/react | ^19.0.1 | React type definitions |
| @types/react-dom | ^19.0.2 | React DOM type definitions |
| tailwindcss | ^4.0.0 | Utility-first CSS framework |
| postcss | ^8.4.49 | CSS transformation tool |
| autoprefixer | ^10.4.20 | CSS vendor prefixing |
| eslint | ^9.17.0 | JavaScript linter |
| eslint-config-next | ^15.1.0 | Next.js ESLint config |
| prettier | ^3.4.2 | Code formatter |
| jest | ^29.7.0 | Testing framework |
| @testing-library/react | ^16.1.0 | React testing utilities |
| @testing-library/jest-dom | ^6.6.3 | Jest DOM matchers |
| playwright | ^1.49.1 | E2E testing framework |
| @playwright/test | ^1.49.1 | Playwright test runner |

**Total**: 23 packages + dependencies (~350-400 packages total with transitive dependencies)

---

## 🔍 Verification Steps

### 1. Package Verification

```bash
# List all top-level dependencies
npm list --depth=0
```

**Expected Output**:
```
todo-frontend@0.1.0
├── next@15.1.0
├── react@19.0.0
├── react-dom@19.0.0
├── better-auth@1.0.7
├── axios@1.7.9
├── zod@3.24.1
└── ... (17 devDependencies)
```

### 2. TypeScript Compilation

```bash
# Type check all files
npx tsc --noEmit
```

**Expected Output**:
```
✓ Type checking successful (0 errors)
```

### 3. Security Audit

```bash
# Check for vulnerabilities
npm audit --production
```

**Expected Output**:
```
found 0 vulnerabilities
```

### 4. Package Scripts

```bash
# Verify all scripts work
npm run dev --help       # Development server
npm run build --help     # Production build
npm run type-check       # TypeScript check
npm run lint             # ESLint check
```

---

## ⚠️ Common Issues & Fixes

### Issue 1: "npm: command not found"

**Symptoms**: Shell cannot find npm command

**Cause**: Node.js not installed or not in PATH

**Fix**:
```bash
# Install Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should show v20.x.x
npm --version   # Should show v10.x.x
```

---

### Issue 2: "EACCES: permission denied"

**Symptoms**: Permission errors during npm install

**Cause**: npm trying to write to system directories

**Fix**:
```bash
# Option 1: Use user-local npm directory (recommended)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# Option 2: Fix permissions on current directory
sudo chown -R $(whoami) node_modules/
sudo chown -R $(whoami) ~/.npm

# DO NOT USE SUDO WITH NPM INSTALL
```

---

### Issue 3: "Cannot find module 'react'"

**Symptoms**: TypeScript or Next.js cannot find installed modules

**Cause**: Incomplete installation or missing dependencies

**Fix**:
```bash
# Clean reinstall
rm -rf node_modules/ package-lock.json
npm cache clean --force
npm install

# Verify React is installed
ls node_modules/react  # Should show package files
```

---

### Issue 4: "lockfileVersion mismatch"

**Symptoms**: package-lock.json version incompatible with npm version

**Cause**: Older npm version (< 7) trying to read newer lockfile

**Fix**:
```bash
# Upgrade npm to latest
npm install -g npm@latest

# Regenerate lockfile
rm package-lock.json
npm install
```

---

### Issue 5: "Peer dependency conflicts"

**Symptoms**: npm warns about unmet peer dependencies

**Cause**: Version conflicts between packages

**Fix**:
```bash
# Option 1: Let npm auto-resolve (npm 7+)
npm install

# Option 2: Force install with legacy peer deps
npm install --legacy-peer-deps

# Option 3: Manually update conflicting package
npm install <package>@latest
```

---

### Issue 6: "Out of memory" errors

**Symptoms**: Installation crashes with "JavaScript heap out of memory"

**Cause**: Insufficient Node.js memory allocation

**Fix**:
```bash
# Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=4096"
npm install

# Or use ci with retry
npm ci --prefer-offline --no-audit
```

---

### Issue 7: Network timeouts

**Symptoms**: npm install hangs or times out

**Cause**: Slow/unstable network connection

**Fix**:
```bash
# Increase timeout
npm config set fetch-timeout 300000  # 5 minutes

# Use offline cache if available
npm install --prefer-offline

# Try different registry
npm config set registry https://registry.npmmirror.com/
npm install
npm config set registry https://registry.npmjs.org/  # Reset
```

---

## 📊 Success Criteria Checklist

### Before Installation
- [ ] Node.js v18+ installed (`node --version`)
- [ ] npm v9+ installed (`npm --version`)
- [ ] In frontend directory (`pwd` shows .../frontend)
- [ ] Internet connection available
- [ ] At least 1GB free disk space

### After Installation
- [ ] node_modules/ directory exists
- [ ] package-lock.json generated
- [ ] All 23 packages listed in `npm list --depth=0`
- [ ] TypeScript compilation passes (`npx tsc --noEmit`)
- [ ] No high/critical vulnerabilities (`npm audit --production`)
- [ ] .env.local file exists with required variables
- [ ] Validation script passes (`bash scripts/validate-installation.sh`)

### Testing Installation
- [ ] Development server starts (`npm run dev`)
- [ ] Build succeeds (`npm run build`)
- [ ] Type check passes (`npm run type-check`)
- [ ] Linter passes (`npm run lint`)
- [ ] No console errors when loading http://localhost:3000

---

## 🎯 Next Steps

### After Successful Installation

1. **Start Development Server**:
   ```bash
   npm run dev
   ```
   - Visit http://localhost:3000
   - Verify page loads without errors

2. **Run Type Check**:
   ```bash
   npm run type-check
   ```
   - Should show 0 errors

3. **Run Linter**:
   ```bash
   npm run lint
   ```
   - Should show 0 warnings/errors

4. **Test Build**:
   ```bash
   npm run build
   ```
   - Creates optimized production build in `.next/`

5. **Run Tests** (when available):
   ```bash
   npm test
   ```

---

## 🛠️ Development Workflow

### Daily Development

```bash
# Start development server
npm run dev

# In separate terminal: watch for type errors
npm run type-check -- --watch

# Format code
npx prettier --write .
```

### Adding New Dependencies

```bash
# Production dependency
npm install <package-name>

# Development dependency
npm install --save-dev <package-name>

# Verify it installs correctly
npm list <package-name>
bash scripts/validate-installation.sh
```

### Updating Dependencies

```bash
# Check for outdated packages
npm outdated

# Update specific package
npm update <package-name>

# Update all packages (within version constraints)
npm update

# Update to latest version (may be breaking)
npm install <package>@latest
```

### Troubleshooting Workflow

```bash
# Level 1: Clear caches
npm cache clean --force
rm -rf .next/

# Level 2: Reinstall dependencies
rm -rf node_modules/ package-lock.json
npm install

# Level 3: Validate installation
bash scripts/validate-installation.sh

# Level 4: Check logs
npm install --verbose > install.log 2>&1
cat install.log
```

---

## 📚 Related Documentation

- **Package Manifest**: `frontend/package.json`
- **Research Document**: `specs/011-frontend-backend-api/research-dependencies.md`
- **Validation Script**: `frontend/scripts/validate-installation.sh`
- **Frontend Guidelines**: `frontend/CLAUDE.md`
- **npm Documentation**: https://docs.npmjs.com/
- **Next.js Docs**: https://nextjs.org/docs

---

## ✅ Quick Validation Commands

Copy-paste these commands to verify installation:

```bash
# One-line validation
cd frontend && npm list --depth=0 && npx tsc --noEmit && npm audit --production

# Full validation
cd frontend && bash scripts/validate-installation.sh

# Environment check
node --version && npm --version && du -sh node_modules/

# Script check
npm run dev -- --help && npm run build -- --help
```

**All checks passing?** ✅ Dependencies installed successfully!
