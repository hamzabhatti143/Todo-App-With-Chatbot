# Todo Frontend

Next.js frontend application for the Todo full-stack web application.

## Tech Stack

- **Next.js 15.1.0** - React framework with App Router
- **React 19.0.0** - UI library
- **TypeScript 5.7.2** - Type-safe JavaScript
- **Tailwind CSS 4.0.0** - Utility-first CSS framework
- **Better Auth 1.0.7** - Authentication library with JWT plugin
- **Axios 1.7.9** - HTTP client for API requests
- **Zod 3.24.1** - Schema validation

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn package manager

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Update `.env.local` with your configuration:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
```

### Development

Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

Create a production build:
```bash
npm run build
```

### Start Production Server

```bash
npm run start
```

### Type Checking

Run TypeScript type checking:
```bash
npm run type-check
```

### Linting

Run ESLint:
```bash
npm run lint
```

## Project Structure

```
frontend/
├── app/              # Next.js App Router pages
├── components/       # React components
│   ├── ui/          # Reusable UI components
│   └── features/    # Feature-specific components
├── lib/             # Utility functions and API clients
├── types/           # TypeScript type definitions
├── hooks/           # Custom React hooks
└── validation/      # Zod schemas for validation
```

## Features

- Task management (CRUD operations)
- User authentication with Better Auth
- Responsive design with Tailwind CSS
- Type-safe development with TypeScript
- Server-side rendering with Next.js

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000/api/`.

Main API endpoints:
- `GET /api/{user_id}/tasks` - Get all tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `BETTER_AUTH_SECRET` | Secret key for authentication | - |
| `BETTER_AUTH_URL` | Frontend URL for auth callbacks | `http://localhost:3000` |

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Better Auth Documentation](https://better-auth.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
