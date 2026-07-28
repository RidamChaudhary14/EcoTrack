import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { UserRole } from '@/shared/types/user';
import { LayoutDashboard, AlertCircle, FileText, Building, Users, Map as MapIcon, LogOut } from 'lucide-react';

const STUDENT_LINKS = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'My Complaints', path: '/dashboard/complaints', icon: FileText },
  { name: 'New Complaint', path: '/dashboard/complaints/new', icon: AlertCircle },
];

const STAFF_LINKS = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Assigned Issues', path: '/dashboard/assigned', icon: AlertCircle },
];

const ADMIN_LINKS = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Manage Complaints', path: '/admin/complaints', icon: FileText },
  { name: 'Manage Buildings', path: '/admin/buildings', icon: Building },
  { name: 'Manage Users', path: '/admin/users', icon: Users },
  { name: 'Campus Map', path: '/admin/map', icon: MapIcon },
];

const ROLE_LINKS = {
  [UserRole.STUDENT]: STUDENT_LINKS,
  [UserRole.STAFF]: STAFF_LINKS,
  [UserRole.ADMIN]: ADMIN_LINKS,
} as const;

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();
  
  const links = ROLE_LINKS[user?.role ?? UserRole.STUDENT] ?? STUDENT_LINKS;

  return (
    <div className="flex flex-col h-full bg-card border-r border-border w-64 shadow-sm">
      <div className="h-16 flex items-center px-6 border-b border-border">
        <h1 className="text-xl font-bold text-primary flex items-center gap-2">
          <AlertCircle className="h-6 w-6" />
          EcoTrack
        </h1>
      </div>

      <nav className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-3">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <li key={link.path}>
                <NavLink
                  to={link.path}
                  end={link.path === '/dashboard'}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                    }`
                  }
                >
                  <Icon className="h-5 w-5" />
                  {link.name}
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="p-4 border-t border-border">
        <button
          onClick={logout}
          className="flex items-center gap-3 px-3 py-2 w-full rounded-md text-sm font-medium text-destructive hover:bg-destructive/10 transition-colors"
        >
          <LogOut className="h-5 w-5" />
          Log out
        </button>
      </div>
    </div>
  );
};
