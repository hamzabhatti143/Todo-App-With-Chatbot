# How to Restart the Development Server

The backend URL has been updated to use your Hugging Face Space. To apply these changes:

## Steps:

1. **Stop the current dev server**:
   - Press `Ctrl + C` in the terminal where `npm run dev` is running

2. **Restart the dev server**:
   ```bash
   npm run dev
   ```

3. **Verify the API URL**:
   - Open your browser's DevTools (F12)
   - Go to the Console tab
   - You should see API requests going to: `https://hamzabhatti-todo-ai-chatbot.hf.space`
   - NOT to `http://localhost:8000`

## Quick Test:

After restarting, the environment variable will be loaded. You can verify by checking the Network tab:
- Try to sign in or register
- Check the Network tab for the POST request
- The URL should be: `https://hamzabhatti-todo-ai-chatbot.hf.space/api/auth/login`

## If Still Seeing localhost:8000:

If you still see `localhost:8000` after restarting, try:

1. **Clear browser cache** (Ctrl + Shift + R or hard refresh)
2. **Check Next.js build cache**:
   ```bash
   rm -rf .next
   npm run dev
   ```

## Current Configuration:

- **API URL**: `https://hamzabhatti-todo-ai-chatbot.hf.space`
- **Frontend URL**: `http://localhost:3000`

---

**Note**: Environment variables in Next.js are only loaded when the server starts. Any changes to `.env.local` require a server restart to take effect.
