import { apiClient } from '@/shared/api/axios';
import type { Complaint, PaginatedResponse } from '../types/complaint.types';

export const complaintService = {
  async getMyComplaints(page = 1, pageSize = 10): Promise<PaginatedResponse<Complaint>> {
    const response = await apiClient.get<PaginatedResponse<Complaint>>('/complaints/me', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  async getComplaint(id: string): Promise<Complaint> {
    const response = await apiClient.get<Complaint>(`/complaints/${id}`);
    return response.data;
  },

  async getAssignedComplaints(page = 1, pageSize = 10): Promise<PaginatedResponse<Complaint>> {
    const response = await apiClient.get<PaginatedResponse<Complaint>>('/staff/complaints', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  async updateComplaintStatus(id: string, status: string, remarks?: string): Promise<Complaint> {
    const response = await apiClient.patch<Complaint>(`/staff/complaints/${id}/status`, {
      status,
      remarks,
    });
    return response.data;
  },

  async getAllComplaintsAdmin(page = 1, pageSize = 10, status?: string): Promise<PaginatedResponse<Complaint>> {
    const params: Record<string, any> = { page, page_size: pageSize };
    if (status) params.status = status;
    
    const response = await apiClient.get<PaginatedResponse<Complaint>>('/admin/complaints', { params });
    return response.data;
  },

  async assignComplaint(complaintId: string, staffId: string): Promise<Complaint> {
    const response = await apiClient.patch<Complaint>(`/admin/complaints/${complaintId}/assign`, {
      assigned_to_id: staffId,
    });
    return response.data;
  }
};
