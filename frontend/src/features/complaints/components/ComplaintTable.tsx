import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { complaintService } from '../services/complaint.service';
import { AlertCircle, Clock, CheckCircle2, Loader2, PlayCircle } from 'lucide-react';
import type { ComplaintStatus } from '../types/complaint.types';

const statusIcons: Record<ComplaintStatus, React.ReactNode> = {
  PENDING: <Clock className="h-4 w-4 text-yellow-500" />,
  ASSIGNED: <AlertCircle className="h-4 w-4 text-blue-500" />,
  IN_PROGRESS: <PlayCircle className="h-4 w-4 text-purple-500" />,
  COMPLETED: <CheckCircle2 className="h-4 w-4 text-green-500" />,
  CANCELLED: <AlertCircle className="h-4 w-4 text-red-500" />
};

export const ComplaintTable: React.FC = () => {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['my-complaints'],
    queryFn: () => complaintService.getMyComplaints(1, 10),
  });

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
        Failed to load complaints. Please try again.
      </div>
    );
  }

  if (data.items.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground border border-dashed border-border rounded-lg bg-card">
        No complaints reported yet.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-border shadow-sm">
      <table className="w-full text-left text-sm text-muted-foreground bg-card">
        <thead className="bg-muted text-foreground border-b border-border">
          <tr>
            <th className="px-4 py-3 font-medium">Title</th>
            <th className="px-4 py-3 font-medium">Status</th>
            <th className="px-4 py-3 font-medium">Priority</th>
            <th className="px-4 py-3 font-medium">Date Reported</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {data.items.map((complaint) => (
            <tr key={complaint.id} className="hover:bg-muted/50 transition-colors">
              <td className="px-4 py-3 font-medium text-foreground">{complaint.title}</td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-2">
                  {statusIcons[complaint.status]}
                  <span className="capitalize">{complaint.status.replace('_', ' ').toLowerCase()}</span>
                </div>
              </td>
              <td className="px-4 py-3">
                <span className="capitalize">{complaint.priority.toLowerCase()}</span>
              </td>
              <td className="px-4 py-3">
                {new Date(complaint.created_at).toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
