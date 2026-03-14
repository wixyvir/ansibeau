# Ansibeau

A modern web application for visualizing Ansible playbook execution results with a clean, professional interface.

## Demo

<video src="doc/demo.mp4" controls width="100%"></video>

## Overview

Ansibeau provides DevOps teams and system administrators with an intuitive way to monitor and understand Ansible playbook execution results. Instead of parsing through terminal logs, users can see hosts, plays, and task summaries in a beautifully designed dark-mode interface.

## Features

- **Visual Host Overview**: Display all hosts with their associated plays
- **Play Status Tracking**: Color-coded status indicators (OK, Changed, Failed)
- **Task Summaries**: Detailed task counts for each play execution
- **Task Details**: Expandable task lists with failure messages and JSON syntax highlighting
- **Log Submission**: Upload logs via paste or file upload with title input
- **Token Authentication**: Secure API access with Bearer token authentication
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark Mode UI**: Terminal-friendly aesthetic with excellent contrast
- **Docker Deployment**: Production-ready multi-stage Docker builds with CI/CD

## Technology Stack

### Frontend
- React 18.3 with TypeScript
- Vite for fast development and builds
- Tailwind CSS for styling
- Lucide React for icons

### Backend
- Django 5.0 with Django REST Framework
- Python 3.11+
- SQLite (development) / PostgreSQL (production)
- Poetry for dependency management

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Poetry (install via `curl -sSL https://install.python-poetry.org | python3 -`)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

### Backend Setup

```bash
cd backend
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Backend runs at: `http://localhost:8000`

## Project Structure

```
ansibeau/
├── .github/workflows/     # CI/CD pipelines
│   ├── docker-build.yml   # Docker build & push to GHCR
│   └── python-lint.yml    # Python linting
│
├── doc/                   # Documentation assets
│   └── demo.mp4           # Demo screencast
│
├── frontend/              # React + TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components (LogPage, SubmitPage)
│   │   ├── services/      # API client
│   │   ├── types/         # TypeScript definitions
│   │   └── App.tsx        # Main app component
│   └── package.json
│
├── backend/               # Django REST API backend
│   ├── ansibeau/        # Django project config
│   ├── api/               # REST API app
│   │   ├── models.py      # Database models
│   │   ├── serializers.py # DRF serializers
│   │   ├── views.py       # API views
│   │   └── services/      # Business logic (log parser)
│   └── pyproject.toml
│
├── docker/                # Docker configuration
│   ├── entrypoint.api.sh  # API startup script
│   ├── entrypoint.web.sh  # Web startup script (generates runtime config)
│   └── nginx.conf         # nginx config
│
├── Dockerfile             # Multi-stage build
├── docker-compose.yml     # Service orchestration
├── CLAUDE.md              # Detailed documentation
└── README.md              # This file
```

## Data Model

The application uses a hierarchical structure:

```
Log (uploaded Ansible log file)
 └── Host (servers in the log)
      └── Play (play executions)
           ├── TaskSummary (ok/changed/failed counts)
           └── Task (individual task executions)
```

### Key Models

**Log**: Represents an uploaded Ansible log file
- Title, upload timestamp, raw content
- One-to-many relationship with hosts

**Host**: Represents a server in a log
- Hostname, unique per log
- One-to-many relationship with plays

**Play**: Represents an Ansible play execution
- Name, date, status (ok/changed/failed)
- Task counts (ok, changed, failed)

**Task**: Represents an individual task execution
- Name, order, status, failure message
- Supports all Ansible statuses (ok, changed, failed, fatal, skipping, etc.)

**Token**: API authentication tokens
- Value, status (active/inactive), optional expiration, comment
- Managed via Django admin

## Current Status

**Version 0.6.0** - Token Authentication

✅ Implemented:
- Complete frontend UI with responsive design
- Django backend with REST Framework
- Database models (Log, Host, Play, Task, Token)
- Ansible log parsing (raw stdout and timestamped formats)
- Task-level details with failure messages and JSON syntax highlighting
- Frontend log submission page (paste or file upload)
- Token-based API authentication (Bearer tokens)
- Django admin interface with custom filters
- Docker multi-stage builds (api, web containers)
- Docker Compose orchestration with PostgreSQL
- GitHub Actions CI/CD with GHCR
- Environment variable configuration (python-decouple)

📋 Planned:
- Log list page with pagination
- Search and filtering
- Enhanced API endpoints
- Real-time updates

## Documentation

For detailed documentation including:
- Component architecture
- API design
- Development workflow
- Design decisions
- Troubleshooting guide

See [CLAUDE.md](CLAUDE.md)

## Development

### Running Both Servers

Terminal 1 (Frontend):
```bash
cd frontend && npm run dev
```

Terminal 2 (Backend):
```bash
cd backend && poetry run python manage.py runserver
```

### Available Scripts

**Frontend**:
- `npm run dev` - Start dev server
- `npm run build` - Production build
- `npm run lint` - Run ESLint

**Backend**:
- `poetry run python manage.py runserver` - Start dev server
- `poetry run python manage.py migrate` - Apply migrations
- `poetry run python manage.py makemigrations` - Create migrations
- `poetry run python manage.py createsuperuser` - Create admin user

## Deployment

### Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose build
cp .env.production .env  # Edit with your values
docker-compose up -d

# Create admin user (migrations run automatically on startup)
docker-compose exec api django-admin createsuperuser
```

Access at: `http://localhost:8000`

**Frontend Backend URI**: By default, the frontend uses relative URLs (via nginx proxy) which works out of the box with Docker. To point the frontend at a different backend, set `BACKEND_URI` in your `.env`:
```bash
BACKEND_URI=https://api.example.com
```

### Using Pre-built Images from GHCR

Docker images are automatically built and pushed to GitHub Container Registry on every push.

```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull and run latest images
docker-compose pull
docker-compose up -d
```

**Available images:**
- `ghcr.io/wixyvir/ansibeau/api:latest`
- `ghcr.io/wixyvir/ansibeau/web:latest`

**Branch tags:** Use `DOCKER_TAG=branch-name` to pull specific branch builds.

## Database

The application uses SQLite for development. To reset the database:

```bash
cd backend
rm db.sqlite3
poetry run python manage.py migrate
```

## Contributing

1. Follow TypeScript types defined in `frontend/src/types/`
2. Use Tailwind utilities instead of custom CSS
3. Maintain dark mode aesthetic
4. Write backend models that mirror frontend types
5. Run `npm run lint` before committing frontend changes

## Future Roadmap

### v0.7.0 - Enhanced API
- List all logs with pagination
- Search and filter capabilities
- Export functionality (JSON, CSV)

### v0.8.0+ - Advanced Features
- User authentication and authorization
- Real-time updates via WebSockets
- Email/Slack notifications
- Analytics dashboard

## License

Internal use project.

## Support

For issues, questions, or contributions, please refer to the comprehensive documentation in [CLAUDE.md](CLAUDE.md).
