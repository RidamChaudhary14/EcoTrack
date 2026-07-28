import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { StatCard } from '@/shared/components/StatCard';
import { ComplaintTable } from '@/features/complaints/components/ComplaintTable';
import { complaintService } from '@/features/complaints/services/complaint.service';
import { FileText, CheckCircle2, Clock, Loader2 } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export const StudentDashboard: React.FC = () => {
  const { user } = useAuth();
  
  const { data: complaints, isLoading } = useQuery({
    queryKey: ['my-complaints-summary'],
    queryFn: () => complaintService.getMyComplaints(1, 100), // Get a larger batch for summary
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="animate-spin h-8 w-8 text-primary" />
      </div>
    );
  }

  const items = complaints?.items || [];
  const total = items.length;
  const pending = items.filter(c => c.status === 'PENDING').length;
  const completed = items.filter(c => c.status === 'COMPLETED').length;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-foreground">Welcome back, {user?.full_name?.split(' ')[0] || 'Student'}!</h2>
        <p className="text-muted-foreground mt-1">Here is the status of your reported campus waste issues.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Total Reports"
          value={total}
          icon={FileText}
          description="All time issues reported by you"
        />
        <StatCard
          title="Pending Issues"
          value={pending}
          icon={Clock}
          description="Issues waiting for assignment"
        />
        <StatCard
          title="Resolved Issues"
          value={completed}
          icon={CheckCircle2}
          description="Issues successfully resolved"
        />
      </div>

      <div className="mt-8">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-foreground">Recent Complaints</h3>
          <button className="text-sm font-medium text-primary hover:underline">
            View All
          </button>
        </div>
        <ComplaintTable />
      </div>
    </div>
  );
};
