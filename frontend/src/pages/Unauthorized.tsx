 import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, ArrowLeft } from 'lucide-react';

export const Unauthorized: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full text-center space-y-6">
        <div className="mx-auto bg-yellow-500/10 text-yellow-600 rounded-full h-24 w-24 flex items-center justify-center mb-2">
          <ShieldAlert className="h-12 w-12" />
        </div>
        <h1 className="text-4xl font-bold text-foreground tracking-tight">403 Forbidden</h1>
        <p className="text-muted-foreground text-lg">
          You don't have the required administrative permissions to access this module.
        </p>
        <button
          onClick={() => navigate('/', { replace: true })}
          className="inline-flex items-center justify-center gap-2 bg-primary text-primary-foreground font-medium rounded-md px-6 py-3 hover:opacity-90 transition-opacity"
        >
          <ArrowLeft className="h-4 w-4" />
          Return to Dashboard
        </button>
      </div>
    </div>
  );
};
