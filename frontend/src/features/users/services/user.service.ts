import { apiClient } from '@/shared/api/axios';
import type { User, UserRole } from '@/shared/types/user';

export const userService = {
  async getUsers(role?: UserRole): Promise<User[]> {
    const params = role ? { role } : {};
    const response = await apiClient.get<User[]>('/users/', { params });
    return response.data;
  },
};
