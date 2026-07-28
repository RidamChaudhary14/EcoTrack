import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Modal } from '@/shared/components/Modal';
import { userService } from '@/features/users/services/user.service';
import { complaintService } from '@/features/complaints/services/complaint.service';
import { Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';

interface AssignStaffModalProps {
  isOpen: boolean;
  onClose: () => void;
  complaintId: string;
  complaintTitle: string;
}

export const AssignStaffModal: React.FC<AssignStaffModalProps> = ({ isOpen, onClose, complaintId, complaintTitle }) => {
  const [selectedStaffId, setSelectedStaffId] = useState<string>('');
  const queryClient = useQueryClient();

  const { data: staffMembers, isLoading } = useQuery({
    queryKey: ['staff-users'],
    queryFn: () => userService.getUsers('STAFF'),
    enabled: isOpen,
  });

  const assignMutation = useMutation({
    mutationFn: (staffId: string) => complaintService.assignComplaint(complaintId, staffId),
    onSuccess: () => {
      toast.success('Complaint successfully assigned!');
      queryClient.invalidateQueries({ queryKey: ['admin-complaints'] });
      queryClient.invalidateQueries({ queryKey: ['admin-dashboard-stats'] });
      onClose();
      setSelectedStaffId('');
    },
    onError: () => {
      toast.error('Failed to assign complaint. Please try again.');
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedStaffId) {
      assignMutation.mutate(selectedStaffId);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Assign Complaint">
      <div className="mb-4">
        <p className="text-sm text-muted-foreground">
          Assigning: <span className="font-semibold text-foreground">{complaintTitle}</span>
        </p>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-6">
          <Loader2 className="animate-spin h-6 w-6 text-primary" />
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Select Staff Member</label>
              <select
                value={selectedStaffId}
                onChange={(e) => setSelectedStaffId(e.target.value)}
                className="w-full bg-background border border-border text-foreground rounded-md p-2 text-sm focus:ring-primary focus:border-primary"
                required
              >
                <option value="" disabled>Choose a staff member...</option>
                {staffMembers?.map(staff => (
                  <option key={staff.id} value={staff.id}>
                    {staff.full_name} ({staff.email})
                  </option>
                ))}
              </select>
            </div>
            
            <div className="flex justify-end gap-3 pt-4 border-t border-border mt-6">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-sm font-medium text-foreground bg-muted hover:bg-muted/80 rounded-md transition-colors"
                disabled={assignMutation.isPending}
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={!selectedStaffId || assignMutation.isPending}
                className="px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:opacity-90 rounded-md transition-opacity disabled:opacity-50 flex items-center gap-2"
              >
                {assignMutation.isPending && <Loader2 className="h-4 w-4 animate-spin" />}
                Confirm Assignment
              </button>
            </div>
          </div>
        </form>
      )}
    </Modal>
  );
};
