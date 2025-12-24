export type PlayStatus = 'ok' | 'changed' | 'failed';

export interface TaskSummary {
  ok: number;
  changed: number;
  failed: number;
}

export interface Play {
  id: string;
  name: string;
  date: string;
  status: PlayStatus;
  tasks: TaskSummary;
}

export interface Host {
  hostname: string;
  plays: Play[];
}
