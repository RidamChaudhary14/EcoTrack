import { apiClient } from '@/shared/api/axios';
import type { Building } from '../types/building.types';

export const buildingService = {
  async getAllBuildings(): Promise<Building[]> {
    const response = await apiClient.get<Building[]>('/buildings/');
    return response.data;
  },
};
