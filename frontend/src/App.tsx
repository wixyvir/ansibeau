import { ServerCard } from './components/ServerCard';
import { type Host } from './types/ansible';

const mockHosts: Host[] = [
  {
    hostname: 'web-01.prod.example.com',
    plays: [
      {
        id: '1',
        name: 'Setup Web Server',
        date: new Date(Date.now() - 3600000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 15,
          changed: 0,
          failed: 0,
        },
      },
      {
        id: '2',
        name: 'Deploy Application',
        date: new Date(Date.now() - 1800000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 12,
          changed: 0,
          failed: 0,
        },
      },
    ],
  },
  {
    hostname: 'web-02.prod.example.com',
    plays: [
      {
        id: '3',
        name: 'Setup Web Server',
        date: new Date(Date.now() - 3600000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'changed',
        tasks: {
          ok: 10,
          changed: 5,
          failed: 0,
        },
      },
      {
        id: '4',
        name: 'Deploy Application',
        date: new Date(Date.now() - 1800000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 12,
          changed: 0,
          failed: 0,
        },
      },
    ],
  },
  {
    hostname: 'db-01.prod.example.com',
    plays: [
      {
        id: '5',
        name: 'Setup Database',
        date: new Date(Date.now() - 5400000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'changed',
        tasks: {
          ok: 18,
          changed: 3,
          failed: 0,
        },
      },
      {
        id: '6',
        name: 'Run Migrations',
        date: new Date(Date.now() - 3000000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 8,
          changed: 0,
          failed: 0,
        },
      },
      {
        id: '7',
        name: 'Optimize Database',
        date: new Date(Date.now() - 1200000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 5,
          changed: 0,
          failed: 0,
        },
      },
    ],
  },
  {
    hostname: 'lb-01.prod.example.com',
    plays: [
      {
        id: '8',
        name: 'Configure Load Balancer',
        date: new Date(Date.now() - 4200000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'failed',
        tasks: {
          ok: 8,
          changed: 2,
          failed: 1,
        },
      },
      {
        id: '9',
        name: 'Update SSL Certificates',
        date: new Date(Date.now() - 2400000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'changed',
        tasks: {
          ok: 6,
          changed: 2,
          failed: 0,
        },
      },
    ],
  },
  {
    hostname: 'cache-01.prod.example.com',
    plays: [
      {
        id: '10',
        name: 'Setup Redis Cache',
        date: new Date(Date.now() - 3900000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 10,
          changed: 0,
          failed: 0,
        },
      },
    ],
  },
  {
    hostname: 'api-01.prod.example.com',
    plays: [
      {
        id: '11',
        name: 'Setup API Server',
        date: new Date(Date.now() - 4800000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'changed',
        tasks: {
          ok: 14,
          changed: 4,
          failed: 0,
        },
      },
      {
        id: '12',
        name: 'Deploy API Services',
        date: new Date(Date.now() - 2700000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 9,
          changed: 0,
          failed: 0,
        },
      },
    ],
  },
  {
    hostname: 'queue-01.prod.example.com',
    plays: [
      {
        id: '13',
        name: 'Install RabbitMQ',
        date: new Date(Date.now() - 6000000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 16,
          changed: 0,
          failed: 0,
        },
      },
      {
        id: '14',
        name: 'Configure Message Queues',
        date: new Date(Date.now() - 4500000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'changed',
        tasks: {
          ok: 11,
          changed: 3,
          failed: 0,
        },
      },
    ],
  },
  {
    hostname: 'monitor-01.prod.example.com',
    plays: [
      {
        id: '15',
        name: 'Setup Prometheus',
        date: new Date(Date.now() - 5100000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'failed',
        tasks: {
          ok: 7,
          changed: 1,
          failed: 2,
        },
      },
    ],
  },
  {
    hostname: 'worker-01.prod.example.com',
    plays: [
      {
        id: '16',
        name: 'Setup Background Workers',
        date: new Date(Date.now() - 3300000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'changed',
        tasks: {
          ok: 13,
          changed: 5,
          failed: 0,
        },
      },
      {
        id: '17',
        name: 'Deploy Worker Services',
        date: new Date(Date.now() - 1500000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 8,
          changed: 0,
          failed: 0,
        },
      },
      {
        id: '18',
        name: 'Configure Job Scheduling',
        date: new Date(Date.now() - 900000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'changed',
        tasks: {
          ok: 6,
          changed: 2,
          failed: 0,
        },
      },
    ],
  },
  {
    hostname: 'storage-01.prod.example.com',
    plays: [
      {
        id: '19',
        name: 'Mount Network Storage',
        date: new Date(Date.now() - 4100000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'ok',
        tasks: {
          ok: 12,
          changed: 0,
          failed: 0,
        },
      },
      {
        id: '20',
        name: 'Configure Backup Jobs',
        date: new Date(Date.now() - 2100000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: 'changed',
        tasks: {
          ok: 9,
          changed: 4,
          failed: 0,
        },
      },
    ],
  },
];

function App() {
  const getHostStatus = (host: Host) => {
    const hasFailedPlays = host.plays.some(play => play.status === 'failed');
    const hasChangedPlays = host.plays.some(play => play.status === 'changed');

    if (hasFailedPlays) return 'failed';
    if (hasChangedPlays) return 'changed';
    return 'ok';
  };

  const statusOrder = { failed: 0, changed: 1, ok: 2 };
  const sortedHosts = [...mockHosts].sort(
    (a, b) => statusOrder[getHostStatus(a)] - statusOrder[getHostStatus(b)]
  );

  return (
    <div className="min-h-screen bg-slate-900 py-6 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-5">
          <h1 className="text-3xl font-bold text-slate-100 mb-1">Ansible Execution Results</h1>
          <p className="text-slate-400 text-base">
            {new Date().toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sortedHosts.map((host) => (
            <ServerCard key={host.hostname} host={host} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
