import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { StatCard } from '@/shared/components/StatCard';
import { complaintService } from '@/features/complaints/services/complaint.service';
import { AlertCircle, Clock, CheckCircle2, Loader2, PlayCircle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import type { ComplaintStatus } from '@/features/complaints/types/complaint.types';
import toast from 'react-hot-toast';

export const StaffDashboard: React.FC = () => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  
  const { data: complaints, isLoading } = useQuery({
    queryKey: ['assigned-complaints'],
    queryFn: () => complaintService.getAssignedComplaints(1, 100),
  });

  const updateStatusMutation = useMutation({
    mutationFn: ({ id, status }: { id: string, status: ComplaintStatus }) => 
      complaintService.updateComplaintStatus(id, status, 'Status updated by staff'),
    onSuccess: () => {
      toast.success('Complaint status updated successfully!');
      queryClient.invalidateQueries({ queryKey: ['assigned-complaints'] });
    },
    onError: () => {
      toast.error('Failed to update complaint status.');
    }
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="animate-spin h-8 w-8 text-primary" />
      </div>
    );
  }

  const items = complaints?.items || [];
  const assigned = items.filter(c => c.status === 'ASSIGNED').length;
  const inProgress = items.filter(c => c.status === 'IN_PROGRESS').length;
  const completed = items.filter(c => c.status === 'COMPLETED').length;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-foreground">Staff Dashboard</h2>
        <p className="text-muted-foreground mt-1">Hello, {user?.full_name}. Manage and resolve issues assigned to you.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Newly Assigned"
          value={assigned}
          icon={AlertCircle}
          description="Awaiting your attention"
        />
        <StatCard
          title="In Progress"
          value={inProgress}
          icon={Clock}
          description="Currently being worked on"
        />
        <StatCard
          title="Resolved"
          value={completed}
          icon={CheckCircle2}
          description="Successfully completed tasks"
        />
      </div>

      <div className="mt-8">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-foreground">Your Active Assignments</h3>
        </div>
        
        {items.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground border border-dashed border-border rounded-lg bg-card">
            You currently have no assigned complaints.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {items.map((complaint) => (
              <div key={complaint.id} className="bg-card border border-border p-5 rounded-lg shadow-sm flex flex-col">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-semibold text-foreground line-clamp-1">{complaint.title}</h4>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    complaint.priority === 'CRITICAL' ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' :
                    complaint.priority === 'HIGH' ? 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400' :
                    'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                  }`}>
                    {complaint.priority}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground line-clamp-2 mb-4 flex-1">
                  {complaint.description}
                </p>
                <div className="pt-4 border-t border-border flex justify-between items-center">
                  <span className="text-xs font-medium text-muted-foreground capitalize">
                    Status: {complaint.status.replace('_', ' ').toLowerCase()}
                  </span>
                  
                  {complaint.status === 'ASSIGNED' && (
                    <button 
                      onClick={() => updateStatusMutation.mutate({ id: complaint.id, status: 'IN_PROGRESS' })}
                      className="text-xs bg-primary text-primary-foreground px-3 py-1.5 rounded-md hover:bg-primary/90 flex items-center gap-1 transition-colors"
                    >
                      <PlayCircle className="h-3 w-3" /> Start Work
                    </button>
                  )}
                  {complaint.status === 'IN_PROGRESS' && (
                    <button 
                      onClick={() => updateStatusMutation.mutate({ id: complaint.id, status: 'COMPLETED' })}
                      className="text-xs bg-green-600 text-white px-3 py-1.5 rounded-md hover:bg-green-700 flex items-center gap-1 transition-colors"
                    >
                      <CheckCircle2 className="h-3 w-3" /> Mark Resolved
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
