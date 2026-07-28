import React from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { StudentDashboard } from './StudentDashboard';
import { StaffDashboard } from './StaffDashboard';
import { AdminDashboard } from './AdminDashboard';
import { Navigate } from 'react-router-dom';
import { UserRole } from '@/shared/types/user';

export const DashboardRouter: React.FC = () => {
  const { user } = useAuth();

  if (!user) return <Navigate to="/auth/login" replace />;

  switch (user.role) {
    case UserRole.STUDENT:
      return <StudentDashboard />;
    case UserRole.STAFF:
      return <StaffDashboard />;
    case UserRole.ADMIN:
      return <AdminDashboard />;
    default:
      return <div>Unknown Role</div>;
  }
};
