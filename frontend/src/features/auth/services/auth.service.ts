import { apiClient } from '@/shared/api/axios';
import type { AuthResponse, LoginFormData } from '../schemas/auth.schema';
import type { User } from '@/shared/types/user';

export const authService = {
  async login(credentials: LoginFormData): Promise<AuthResponse> {
    // FastAPI OAuth2 expects form-data
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await apiClient.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/users/me');
    return response.data;
  },
};
