/**
 * User Type Definitions
 *
 * TypeScript interfaces for user entities and authentication.
 * Matches backend SQLModel schema for type safety.
 */

/**
 * User entity from database
 */
export interface User {
  id: string;
  username: string;
  email: string;
  created_at: string;
}

/**
 * Input for creating a new user
 */
export interface UserCreate {
  username: string;
  email: string;
  password: string;
}

/**
 * Input for user login
 */
export interface UserLogin {
  username: string;
  password: string;
}

/**
 * Sign-in form input (alias for UserLogin)
 */
export type SignInInput = UserLogin;

/**
 * Sign-up form input (alias for UserCreate)
 */
export type SignUpInput = UserCreate;

/**
 * JWT token response from authentication
 */
export interface Token {
  access_token: string;
  token_type: string;
}

/**
 * Authentication state in the application
 */
export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}
