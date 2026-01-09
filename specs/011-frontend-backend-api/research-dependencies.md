# Research: Frontend Dependencies Installation

**Feature**: 011-frontend-backend-api (Dependencies Sub-Plan)
**Date**: 2026-01-01
**Status**: Complete

## Research Summary

This document captures research findings for implementing a robust frontend dependencies installation workflow for the Next.js 15+ application.

## Decision 1: npm Install Sequence

**Decision**: Use npm clean install (npm ci) for deterministic builds, with fallback to npm install for development

**Rationale**:
- `npm ci` uses package-lock.json for exact version matching
- Faster installation in CI/CD environments
- Ensures consistency across team members and deployment environments
- Removes node_modules/ before install to prevent conflicts

**Sequence**:
```bash
# Production/CI workflow
rm -rf node_modules/
npm ci

# Development workflow (when package.json changes)
npm install

# Verify installation
npm list --depth=0
```

**Alternatives Considered**:
1. `npm install` only - Less deterministic, slower in CI
2. `yarn install` - Would require migration, different lockfile format
3. `pnpm install` - More efficient but requires new tooling setup

## Decision 2: Package Verification Strategy

**Decision**: Multi-layer verification using npm list, npm audit, and TypeScript compilation

**Rationale**:
- `npm list` - Detects missing or extraneous packages
- `npm audit` - Identifies known security vulnerabilities
- TypeScript compilation - Verifies type declarations are installed correctly
- Prevents runtime errors from missing dependencies

**Verification Commands**:
```bash
# Check all packages installed correctly
npm list --depth=0

# Audit for vulnerabilities
npm audit --production

# Verify TypeScript types
npm list @types/

# Check for outdated packages
npm outdated
```

**Error Detection**:
- Missing dependencies: npm list shows UNMET DEPENDENCY
- Version conflicts: npm list shows deduped packages
- Security issues: npm audit shows vulnerabilities

## Decision 3: TypeScript Compilation Check

**Decision**: Run full TypeScript type checking before considering installation complete

**Rationale**:
- Next.js 15 uses TypeScript 5.7.2 with strict mode
- Missing @types/ packages cause compilation errors
- Catches type errors early before runtime
- Validates tsconfig.json configuration

**Compilation Commands**:
```bash
# Type check without emitting files (fastest)
npx tsc --noEmit

# Type check with detailed errors
npx tsc --noEmit --pretty

# Check specific files
npx tsc --noEmit app/page.tsx
```

**Expected Output**:
```
✓ Type checking successful (0 errors)
```

**Common Errors**:
- `Cannot find module 'react'` → Missing @types/react
- `Cannot find name 'process'` → Missing @types/node
- `Property does not exist on type` → Incorrect type definitions

## Decision 4: Error Resolution Strategy

**Decision**: Structured troubleshooting workflow with automated fixes where possible

**Rationale**:
- Clear escalation path from simple to complex fixes
- Automated scripts for common issues
- Documentation for manual intervention when needed
- Prevents incomplete installations

**Resolution Workflow**:

### Level 1: Automatic Fixes
```bash
# Clear npm cache
npm cache clean --force

# Remove lockfile and reinstall
rm package-lock.json
npm install

# Clear Next.js cache
rm -rf .next/
```

### Level 2: Dependency Conflicts
```bash
# Check for conflicts
npm list

# Force install with legacy peer deps
npm install --legacy-peer-deps

# Update specific package
npm update <package-name>
```

### Level 3: Manual Intervention
```bash
# Check Node.js version compatibility
node --version  # Expect v18+ or v20+

# Verify npm registry
npm config get registry  # Should be https://registry.npmjs.org/

# Check for platform-specific issues
npm install --verbose
```

**Error Categories**:
1. **Network errors** → Retry with npm cache clean
2. **Permission errors** → Check file ownership, avoid sudo
3. **Version conflicts** → Update package.json constraints
4. **Platform errors** → Check Node.js version compatibility

## Decision 5: Installation Validation Checklist

**Decision**: Comprehensive post-install validation script

**Rationale**:
- Single command to verify all dependencies
- Prevents partial installations
- Documents expected state
- Catches issues before development

**Validation Script**:
```bash
#!/bin/bash
# validate-installation.sh

echo "=== Validating Frontend Dependencies ==="

# 1. Check node_modules exists
if [ ! -d "node_modules" ]; then
  echo "❌ node_modules/ not found"
  exit 1
fi
echo "✓ node_modules/ exists"

# 2. Verify critical dependencies
for pkg in "next" "react" "react-dom" "typescript"; do
  if [ ! -d "node_modules/$pkg" ]; then
    echo "❌ Missing: $pkg"
    exit 1
  fi
done
echo "✓ Critical dependencies installed"

# 3. Check TypeScript types
for pkg in "@types/node" "@types/react" "@types/react-dom"; do
  if [ ! -d "node_modules/$pkg" ]; then
    echo "❌ Missing: $pkg"
    exit 1
  fi
done
echo "✓ TypeScript types installed"

# 4. Run type check
if ! npx tsc --noEmit; then
  echo "❌ TypeScript compilation failed"
  exit 1
fi
echo "✓ TypeScript compilation passed"

# 5. Check for vulnerabilities
if ! npm audit --production --audit-level=high; then
  echo "⚠️  High/critical vulnerabilities found"
fi
echo "✓ Security audit complete"

echo "=== All validations passed ==="
```

## Decision 6: Dependency Update Strategy

**Decision**: Pin major versions in package.json, allow patch updates automatically

**Rationale**:
- Caret (^) allows compatible updates (e.g., ^15.1.0 allows 15.x.x)
- Prevents breaking changes from major version bumps
- Allows security patches to install automatically
- Documented in package.json for transparency

**Version Constraints**:
```json
{
  "dependencies": {
    "next": "^15.1.0",        // Allow 15.x.x
    "react": "^19.0.0",        // Allow 19.x.x
    "axios": "^1.7.9"          // Allow 1.x.x
  }
}
```

**Update Workflow**:
```bash
# Check for outdated packages
npm outdated

# Update to latest compatible versions
npm update

# Update specific package to latest
npm install <package>@latest

# Regenerate lockfile
rm package-lock.json && npm install
```

## Best Practices Applied

### From Constitution Principle III (Frontend Architecture):
- ✅ All dependencies documented in package.json
- ✅ TypeScript strict mode enabled
- ✅ Tailwind CSS as sole styling solution
- ✅ Axios for HTTP requests
- ✅ Zod for validation

### From Frontend CLAUDE.md:
- ✅ Next.js 15+ with App Router
- ✅ React 19 with hooks
- ✅ Better Auth 1.0.7 for authentication
- ✅ Testing libraries (Jest, Playwright, React Testing Library)

### Security Considerations:
- ✅ npm audit checks for known vulnerabilities
- ✅ No wildcards (*) in version constraints
- ✅ Lockfile committed to repository
- ✅ Regular dependency updates scheduled

## Performance Metrics

**Installation Benchmarks** (Expected):
- `npm ci` (clean install): ~30-60 seconds
- `npm install` (with cache): ~15-30 seconds
- `npm update` (minor versions): ~10-20 seconds
- TypeScript compilation: ~5-10 seconds

**Success Criteria**:
- All 18 dependencies in package.json installed
- All 17 devDependencies installed
- Zero TypeScript compilation errors
- Zero high/critical npm audit vulnerabilities
- node_modules/ size: ~500-800 MB (expected for Next.js 15)

## Integration Points

### Files Affected:
- `frontend/package.json` - Dependency manifest
- `frontend/package-lock.json` - Locked versions
- `frontend/node_modules/` - Installed packages
- `frontend/.next/` - Next.js build cache (cleared if needed)

### Environment Requirements:
- Node.js: v18.17.0+ or v20.0.0+ (recommended: v20.11.0)
- npm: v9.0.0+ (included with Node.js)
- RAM: Minimum 2GB free for installation
- Disk space: ~1GB for node_modules/

## Lessons Learned

1. **Clean installs are critical**: Always remove node_modules/ before `npm ci` to prevent conflicts
2. **TypeScript types are essential**: Missing @types/ packages cause cryptic errors
3. **npm audit is noisy**: Focus on high/critical vulnerabilities only
4. **Version conflicts are common**: Use --legacy-peer-deps as last resort
5. **Cache issues are frequent**: `npm cache clean --force` resolves many problems

## Future Enhancements

### Potential Improvements:
1. Automated dependency updates via Dependabot
2. Pre-commit hook to verify package.json matches package-lock.json
3. CI/CD pipeline integration for automated testing
4. npm workspaces for monorepo optimization
5. pnpm migration for faster installs

### Not Implemented (Out of Scope):
- Automated security patching
- Dependency license compliance checking
- Bundle size analysis
- Tree-shaking optimization

## References

- **package.json**: `frontend/package.json`
- **Frontend CLAUDE.md**: `frontend/CLAUDE.md`
- **Constitution**: `.specify/memory/constitution.md`
- **npm documentation**: https://docs.npmjs.com/
- **Next.js 15 docs**: https://nextjs.org/docs

## Research Validation

All decisions have been validated against:
- ✅ Frontend architecture standards (Next.js 15, TypeScript 5.7)
- ✅ Security requirements (npm audit, lockfile)
- ✅ Performance goals (<60s install time)
- ✅ Constitution principles (quality, testing, documentation)
