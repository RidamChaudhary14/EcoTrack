import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { buildingService } from '@/features/buildings/services/building.service';
import { Loader2 } from 'lucide-react';
import L from 'leaflet';

// Fix Leaflet's default icon paths for React
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

export const CampusMap: React.FC = () => {
  const { data: buildings, isLoading } = useQuery({
    queryKey: ['buildings-map'],
    queryFn: () => buildingService.getAllBuildings(),
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loader2 className="animate-spin h-8 w-8 text-primary" />
      </div>
    );
  }

  // Fallback center point if no buildings exist
  const defaultCenter: [number, number] = buildings && buildings.length > 0 
    ? [buildings[0].latitude, buildings[0].longitude] 
    : [37.7749, -122.4194];

  return (
    <div className="space-y-4 h-full flex flex-col">
      <div>
        <h2 className="text-2xl font-bold text-foreground">Campus Map</h2>
        <p className="text-muted-foreground mt-1">Geographic overview of EcoTrack infrastructure.</p>
      </div>

      <div className="flex-1 min-h-[500px] border border-border rounded-lg overflow-hidden shadow-sm relative z-0">
        <MapContainer center={defaultCenter} zoom={15} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {buildings?.map((building) => (
            <Marker key={building.id} position={[building.latitude, building.longitude]}>
              <Popup>
                <div className="font-sans">
                  <h3 className="font-bold text-sm mb-1">{building.name}</h3>
                  <p className="text-xs text-gray-600 mb-0">Code: {building.code}</p>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};
