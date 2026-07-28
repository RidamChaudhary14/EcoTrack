export const UserRole = {
  STUDENT: 'STUDENT',
  STAFF: 'STAFF',
  ADMIN: 'ADMIN',
} as const;

export type UserRole = (typeof UserRole)[keyof typeof UserRole];

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  department?: string;
  phone_number?: string;
  created_at: string;
}

/**
 * Normalizes a role string from the backend (e.g. "Admin", "Staff", "Student")
 * to the uppercase enum value used throughout the frontend ("ADMIN", "STAFF", "STUDENT").
 */
export function normalizeRole(role: string): UserRole {
  const upper = role.toUpperCase();
  if (upper === UserRole.ADMIN) return UserRole.ADMIN;
  if (upper === UserRole.STAFF) return UserRole.STAFF;
  return UserRole.STUDENT;
}
