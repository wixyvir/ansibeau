import { Calendar } from 'lucide-react';

interface PlayHeaderProps {
  title: string;
  date: string;
}

export function PlayHeader({ title, date }: PlayHeaderProps) {
  return (
    <div className="mb-8">
      <h1 className="text-4xl font-bold text-slate-100 mb-3">{title}</h1>
      <div className="flex items-center gap-2 text-slate-400">
        <Calendar className="w-5 h-5" />
        <span className="text-lg">{date}</span>
      </div>
    </div>
  );
}
