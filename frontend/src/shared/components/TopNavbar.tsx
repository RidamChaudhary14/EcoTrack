import React from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { User as UserIcon } from 'lucide-react';

export const TopNavbar: React.FC = () => {
  const { user } = useAuth();

  return (
    <header className="h-16 bg-card border-b border-border flex items-center justify-between px-6 shadow-sm">
      <div className="flex items-center">
        {/* Mobile menu toggle button could go here */}
      </div>

      <div className="flex items-center gap-4">
        {/* Theme toggle could go here */}
        
        <div className="flex items-center gap-3 pl-4 border-l border-border">
          <div className="text-right">
            <p className="text-sm font-medium text-foreground">{user?.full_name}</p>
            <p className="text-xs text-muted-foreground">{user?.role}</p>
          </div>
          <div className="h-9 w-9 rounded-full bg-primary/10 flex items-center justify-center text-primary">
            <UserIcon className="h-5 w-5" />
          </div>
        </div>
      </div>
    </header>
  );
};
