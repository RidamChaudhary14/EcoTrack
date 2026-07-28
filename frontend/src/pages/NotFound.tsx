import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FileQuestion, ArrowLeft } from 'lucide-react';

export const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full text-center space-y-6">
        <div className="mx-auto bg-muted text-muted-foreground rounded-full h-24 w-24 flex items-center justify-center mb-2">
          <FileQuestion className="h-12 w-12" />
        </div>
        <h1 className="text-4xl font-bold text-foreground tracking-tight">404 Not Found</h1>
        <p className="text-muted-foreground text-lg">
          The page you are looking for does not exist or has been moved.
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
