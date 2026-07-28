import { createBrowserRouter, Navigate } from 'react-router-dom';
import { PublicRoute } from './PublicRoute';
import { ProtectedRoute } from './ProtectedRoute';
import { RoleProtectedRoute } from './RoleProtectedRoute';

import { AuthLayout } from '@/layouts/AuthLayout';
import { LoginForm } from '@/features/auth/components/LoginForm';

import { DashboardLayout } from '@/layouts/DashboardLayout';
import { AdminComplaintTable } from '@/features/complaints/components/AdminComplaintTable';
import { BuildingManager } from '@/features/buildings/components/BuildingManager';
import { CampusMap } from '@/features/map/components/CampusMap';

import { DashboardRouter } from '@/features/dashboard/components/DashboardRouter';

import { NotFound } from '@/pages/NotFound';
import { Unauthorized } from '@/pages/Unauthorized';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/dashboard" replace />,
  },
  {
    path: '/auth',
    element: <PublicRoute />,
    children: [
      {
        path: '',
        element: <AuthLayout />,
        children: [
          {
            path: 'login',
            element: <LoginForm />,
          },
        ]
      }
    ],
  },
  {
    path: '/dashboard',
    element: <ProtectedRoute />,
    children: [
      {
        path: '',
        element: <DashboardLayout />,
        children: [
          {
            path: '',
            element: <DashboardRouter />,
          },
        ]
      },
    ],
  },
  {
    path: '/admin',
    element: <RoleProtectedRoute allowedRoles={['ADMIN']} />,
    children: [
      {
        path: '',
        element: <DashboardLayout />,
        children: [
          {
            path: 'complaints',
            element: <AdminComplaintTable />,
          },
          {
            path: 'buildings',
            element: <BuildingManager />,
          },
          {
            path: 'map',
            element: <CampusMap />,
          },
        ]
      },
    ],
  },
  {
    path: '/unauthorized',
    element: <Unauthorized />,
  },
  {
    path: '*',
    element: <NotFound />,
  }
]);
