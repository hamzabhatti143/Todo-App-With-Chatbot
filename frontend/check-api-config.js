#!/usr/bin/env node
/**
 * Quick diagnostic script to verify API configuration
 * Run with: node check-api-config.js
 */

const fs = require('fs');
const path = require('path');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('🔍 API Configuration Check');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('');

// Read .env.local file
const envPath = path.join(__dirname, '.env.local');
let apiUrl = null;

try {
  const envContent = fs.readFileSync(envPath, 'utf8');
  const match = envContent.match(/NEXT_PUBLIC_API_URL=(.+)/);
  if (match) {
    apiUrl = match[1].trim();
  }
} catch (err) {
  console.log('⚠️  .env.local file not found!');
}

const fallbackUrl = 'https://hamzabhatti-todo-fullstack-web.hf.space';

console.log('.env.local file:');
console.log(`  NEXT_PUBLIC_API_URL = ${apiUrl || '(not set)'}`);
console.log('');

console.log('Fallback URL (in code):');
console.log(`  ${fallbackUrl}`);
console.log('');

console.log('Effective API URL:');
console.log(`  ${apiUrl || fallbackUrl}`);
console.log('');

if (apiUrl === 'http://localhost:8000') {
  console.log('❌ ERROR: Still using localhost:8000!');
  console.log('');
  console.log('This file needs to be updated:');
  console.log(`  ${envPath}`);
  console.log('');
  console.log('Should contain:');
  console.log('  NEXT_PUBLIC_API_URL=https://hamzabhatti-todo-fullstack-web.hf.space');
} else if (apiUrl && apiUrl.includes('hamzabhatti-todo-fullstack-web.hf.space')) {
  console.log('✅ Configuration is correct!');
  console.log('');
  console.log('If API calls still go to localhost:8000:');
  console.log('');
  console.log('1. RESTART the development server:');
  console.log('   - Stop: Ctrl+C');
  console.log('   - Start: npm run dev');
  console.log('');
  console.log('2. HARD REFRESH your browser:');
  console.log('   - Windows/Linux: Ctrl+Shift+R');
  console.log('   - Mac: Cmd+Shift+R');
  console.log('');
  console.log('3. If still not working, clear Next.js cache:');
  console.log('   rm -rf .next');
  console.log('   npm run dev');
} else {
  console.log('ℹ️  No Hugging Face Space URL detected');
  console.log('');
  console.log('Expected: https://hamzabhatti-todo-fullstack-web.hf.space');
  console.log(`Found: ${apiUrl || '(not set)'}`);
}

console.log('');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
