import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { StatCard } from '@/shared/components/StatCard';
import { adminService } from '../services/admin.service';
import { FileText, Clock, CheckCircle2, PlayCircle, Building, Users, Loader2 } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export const AdminDashboard: React.FC = () => {
  const { user } = useAuth();
  
  const { data: stats, isLoading, isError } = useQuery({
    queryKey: ['admin-dashboard-stats'],
    queryFn: () => adminService.getDashboardStats(),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="animate-spin h-8 w-8 text-primary" />
      </div>
    );
  }

  if (isError || !stats) {
    return (
      <div className="text-center py-12 text-destructive">
        Failed to load system statistics.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-foreground">System Overview</h2>
        <p className="text-muted-foreground mt-1">Hello, {user?.full_name}. Here is the aggregated EcoTrack data.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard
          title="Total Complaints"
          value={stats.total_complaints || 0}
          icon={FileText}
          description="System-wide reports"
        />
        <StatCard
          title="Pending Assignment"
          value={stats.pending_complaints || 0}
          icon={Clock}
          description="Awaiting staff allocation"
        />
        <StatCard
          title="In Progress"
          value={stats.in_progress_complaints || 0}
          icon={PlayCircle}
          description="Currently being worked on"
        />
        <StatCard
          title="Resolved"
          value={stats.completed_complaints || 0}
          icon={CheckCircle2}
          description="Successfully completed tasks"
        />
        <StatCard
          title="Active Buildings"
          value={stats.total_buildings || 0}
          icon={Building}
          description="Monitored campus facilities"
        />
        <StatCard
          title="Registered Users"
          value={stats.total_users || 0}
          icon={Users}
          description="Students, Staff, and Admins"
        />
      </div>

      <div className="mt-8 bg-card border border-border p-6 rounded-lg shadow-sm">
        <h3 className="text-lg font-semibold text-foreground mb-2">Quick Actions</h3>
        <p className="text-sm text-muted-foreground mb-4">Navigate to administrative modules to manage the system.</p>
        <div className="flex gap-4">
           {/* These will be real links in Phase 12/13 */}
           <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md font-medium text-sm hover:opacity-90 transition-opacity">
             Manage Complaints
           </button>
           <button className="bg-secondary text-secondary-foreground border border-border px-4 py-2 rounded-md font-medium text-sm hover:bg-muted transition-colors">
             Manage Buildings
           </button>
        </div>
      </div>
    </div>
  );
};
