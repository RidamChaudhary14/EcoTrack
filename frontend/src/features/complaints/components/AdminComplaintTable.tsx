import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { complaintService } from '../services/complaint.service';
import { AlertCircle, Clock, CheckCircle2, Loader2, PlayCircle, UserPlus } from 'lucide-react';
import type { ComplaintStatus } from '../types/complaint.types';
import { AssignStaffModal } from './AssignStaffModal';

const statusIcons: Record<ComplaintStatus, React.ReactNode> = {
  PENDING: <Clock className="h-4 w-4 text-yellow-500" />,
  ASSIGNED: <AlertCircle className="h-4 w-4 text-blue-500" />,
  IN_PROGRESS: <PlayCircle className="h-4 w-4 text-purple-500" />,
  COMPLETED: <CheckCircle2 className="h-4 w-4 text-green-500" />,
  CANCELLED: <AlertCircle className="h-4 w-4 text-red-500" />
};

export const AdminComplaintTable: React.FC = () => {
  const [page, setPage] = useState(1);
  const [selectedStatus, setSelectedStatus] = useState<string>('');
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedComplaint, setSelectedComplaint] = useState<{id: string, title: string} | null>(null);

  const { data, isLoading, isError } = useQuery({
    queryKey: ['admin-complaints', page, selectedStatus],
    queryFn: () => complaintService.getAllComplaintsAdmin(page, 15, selectedStatus || undefined),
  });

  const handleAssignClick = (id: string, title: string) => {
    setSelectedComplaint({ id, title });
    setModalOpen(true);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loader2 className="animate-spin h-8 w-8 text-primary" />
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="text-center py-12 text-destructive">
        Failed to load system complaints. Please try again.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-foreground">Manage Complaints</h2>
        
        <select
          value={selectedStatus}
          onChange={(e) => {
            setSelectedStatus(e.target.value);
            setPage(1);
          }}
          className="bg-background border border-border text-foreground text-sm rounded-md focus:ring-primary focus:border-primary block p-2"
        >
          <option value="">All Statuses</option>
          <option value="PENDING">Pending</option>
          <option value="ASSIGNED">Assigned</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="COMPLETED">Completed</option>
        </select>
      </div>

      <div className="overflow-x-auto rounded-lg border border-border shadow-sm">
        <table className="w-full text-left text-sm text-muted-foreground bg-card">
          <thead className="bg-muted text-foreground border-b border-border">
            <tr>
              <th className="px-4 py-3 font-medium">Title</th>
              <th className="px-4 py-3 font-medium">Reported By</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Priority</th>
              <th className="px-4 py-3 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {data.items.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-muted-foreground">
                  No complaints match the current filters.
                </td>
              </tr>
            ) : (
              data.items.map((complaint) => (
                <tr key={complaint.id} className="hover:bg-muted/50 transition-colors">
                  <td className="px-4 py-3 font-medium text-foreground">{complaint.title}</td>
                  <td className="px-4 py-3 text-xs">{complaint.reported_by}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      {statusIcons[complaint.status]}
                      <span className="capitalize">{complaint.status.replace('_', ' ').toLowerCase()}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <span className="capitalize">{complaint.priority.toLowerCase()}</span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    {complaint.status === 'PENDING' ? (
                      <button 
                        onClick={() => handleAssignClick(complaint.id, complaint.title)}
                        className="inline-flex items-center gap-1 bg-primary text-primary-foreground px-3 py-1.5 rounded-md text-xs font-medium hover:opacity-90 transition-opacity"
                      >
                        <UserPlus className="h-3 w-3" />
                        Assign
                      </button>
                    ) : (
                      <span className="text-xs text-muted-foreground">Assigned to: {complaint.assigned_to || 'N/A'}</span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {data.total_pages > 1 && (
        <div className="flex items-center justify-between pt-4 border-t border-border">
          <span className="text-sm text-muted-foreground">
            Page {data.page} of {data.total_pages}
          </span>
          <div className="flex gap-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={!data.has_previous}
              className="px-3 py-1 bg-card border border-border text-foreground rounded-md text-sm disabled:opacity-50 hover:bg-muted"
            >
              Previous
            </button>
            <button
              onClick={() => setPage(p => p + 1)}
              disabled={!data.has_next}
              className="px-3 py-1 bg-card border border-border text-foreground rounded-md text-sm disabled:opacity-50 hover:bg-muted"
            >
              Next
            </button>
          </div>
        </div>
      )}

      {selectedComplaint && (
        <AssignStaffModal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          complaintId={selectedComplaint.id}
          complaintTitle={selectedComplaint.title}
        />
      )}
    </div>
  );
};
