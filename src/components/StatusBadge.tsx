import { type PlayStatus } from '../types/ansible';

interface StatusBadgeProps {
  status: PlayStatus;
  count: number;
  label: string;
}

const statusStyles: Record<PlayStatus, string> = {
  ok: 'bg-green-900/50 text-green-400 border-green-700',
  changed: 'bg-yellow-900/50 text-yellow-400 border-yellow-700',
  failed: 'bg-red-900/50 text-red-400 border-red-700',
};

export function StatusBadge({ status, count, label }: StatusBadgeProps) {
  return (
    <div
      className={`flex items-center justify-between px-3 py-2 rounded-lg border ${statusStyles[status]}`}
    >
      <span className="text-sm font-medium">{label}</span>
      <span className="text-lg font-bold ml-2">{count}</span>
    </div>
  );
}
