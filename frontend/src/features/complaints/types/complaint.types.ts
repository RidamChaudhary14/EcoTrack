export type ComplaintStatus = 'PENDING' | 'ASSIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
export type Priority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type WasteType = 'PLASTIC' | 'PAPER' | 'ORGANIC' | 'METAL' | 'GLASS' | 'ELECTRONIC' | 'HAZARDOUS' | 'MIXED' | 'OTHER';

export interface Complaint {
  id: string;
  title: string;
  description: string;
  status: ComplaintStatus;
  priority: Priority;
  waste_type: WasteType;
  building_id: string;
  location_details: string;
  image_url?: string;
  reported_by: string;
  assigned_to?: string;
  created_at: string;
  updated_at: string;
  resolved_at?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_previous: boolean;
}
