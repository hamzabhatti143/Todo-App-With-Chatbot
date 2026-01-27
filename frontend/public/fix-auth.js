/**
 * Authentication Fix Script
 *
 * Run this in your browser console to clear old authentication tokens
 * and redirect to login page.
 *
 * Usage:
 * 1. Open browser at http://localhost:3000
 * 2. Press F12 to open Developer Tools
 * 3. Go to Console tab
 * 4. Copy and paste this entire script
 * 5. Press Enter
 */

(function() {
  console.log('🔧 Authentication Fix Script');
  console.log('─'.repeat(60));

  // Check if we have old tokens
  const oldToken = localStorage.getItem('auth_token');
  const oldUserId = localStorage.getItem('user_id');

  if (oldToken || oldUserId) {
    console.log('❌ Found old authentication tokens:');
    if (oldToken) console.log('   - auth_token:', oldToken.substring(0, 20) + '...');
    if (oldUserId) console.log('   - user_id:', oldUserId);

    console.log('\n🗑️  Clearing localStorage...');
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');

    console.log('✅ localStorage cleared');
    console.log('\n🔄 Redirecting to login page...');

    setTimeout(() => {
      window.location.href = '/signin?cleared=true';
    }, 1000);

  } else {
    console.log('✅ No old tokens found');
    console.log('📝 You can now login with:');
    console.log('   Email: test_chat_user@example.com');
    console.log('   Password: SecurePassword123!');
  }

  console.log('─'.repeat(60));
})();
