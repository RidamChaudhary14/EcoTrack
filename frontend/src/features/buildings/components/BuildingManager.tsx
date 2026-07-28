import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { buildingService } from '../services/building.service';
import { Loader2, Building as BuildingIcon, MapPin, Activity } from 'lucide-react';

export const BuildingManager: React.FC = () => {
  const { data: buildings, isLoading, isError } = useQuery({
    queryKey: ['buildings'],
    queryFn: () => buildingService.getAllBuildings(),
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loader2 className="animate-spin h-8 w-8 text-primary" />
      </div>
    );
  }

  if (isError || !buildings) {
    return (
      <div className="text-center py-12 text-destructive">
        Failed to load buildings. Please try again.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Campus Buildings</h2>
          <p className="text-muted-foreground mt-1">Manage active campus infrastructure.</p>
        </div>
        <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md font-medium text-sm hover:opacity-90 transition-opacity flex items-center gap-2">
          <BuildingIcon className="h-4 w-4" /> Add Building
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {buildings.map(building => (
          <div key={building.id} className="bg-card border border-border p-6 rounded-lg shadow-sm">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="font-semibold text-lg text-foreground">{building.name}</h3>
                <p className="text-sm font-medium text-muted-foreground">Code: {building.code}</p>
              </div>
              <div className={`p-1.5 rounded-full ${building.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                <Activity className="h-4 w-4" />
              </div>
            </div>
            
            <div className="flex items-center gap-2 text-sm text-muted-foreground border-t border-border pt-4">
              <MapPin className="h-4 w-4" />
              <span>{building.latitude.toFixed(4)}, {building.longitude.toFixed(4)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
