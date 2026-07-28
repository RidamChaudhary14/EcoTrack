import { apiClient } from '@/shared/api/axios';

export interface DashboardStats {
  total_complaints: number;
  pending_complaints: number;
  in_progress_complaints: number;
  completed_complaints: number;
  total_buildings: number;
  total_users: number;
}

export const adminService = {
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await apiClient.get<DashboardStats>('/dashboard/stats');
    return response.data;
  },
};
