# Ansible UI - Project Documentation

## Overview

Ansible UI is a modern web application designed to display comprehensive views of Ansible Play execution results in a clean, professional, and visually appealing interface. The application focuses on presenting hosts and their associated plays with detailed task summaries.

## Project Purpose

The primary goal is to provide DevOps teams and system administrators with an intuitive way to monitor and understand Ansible playbook execution results at a glance. Instead of parsing through terminal logs, users can see:

- Which hosts were targeted by Ansible executions
- Multiple plays executed on each host
- The overall status of each play (OK, Changed, Failed)
- Detailed task counts for each play
- Execution timestamps for each play

## Technology Stack

### Frontend Framework
- **React 18.3.1**: Modern UI library with hooks and functional components
- **TypeScript 5.6**: Type-safe development with enhanced IDE support
- **Vite 6**: Lightning-fast build tool and dev server

### Styling
- **Tailwind CSS 3.4**: Utility-first CSS framework
- **Dark Mode Design**: Optimized for terminal-friendly aesthetics with slate color palette

### Icons
- **Lucide React 0.460**: Clean, consistent icon library for server and calendar icons

### Development Tools
- **ESLint**: Code linting and quality enforcement
- **PostCSS**: CSS processing with Autoprefixer

## Architecture

### Component Structure

```
src/
├── components/
│   ├── PlayCard.tsx        # Displays individual play with task summaries
│   ├── PlayHeader.tsx      # (Legacy) Displays play title and execution date
│   ├── ServerCard.tsx      # Host card displaying multiple plays
│   └── StatusBadge.tsx     # Reusable status indicator badge
├── types/
│   └── ansible.ts          # TypeScript type definitions
├── App.tsx                 # Main application component
├── main.tsx                # React app entry point
└── index.css               # Global styles and Tailwind directives
```

### Data Model

#### Host
Represents a single server with its associated plays:
```typescript
interface Host {
  hostname: string;     // Server hostname/FQDN
  plays: Play[];        // Array of plays executed on this host
}
```

#### Play
Represents a single Ansible play execution:
```typescript
interface Play {
  id: string;           // Unique identifier
  name: string;         // Play name (e.g., "Setup Web Server")
  date: string;         // Execution timestamp
  status: PlayStatus;   // Play status (ok/changed/failed)
  tasks: TaskSummary;   // Task execution counts for this play
}
```

#### TaskSummary
Aggregated task results for a play:
```typescript
interface TaskSummary {
  ok: number;           // Successfully completed tasks
  changed: number;      // Tasks that made changes
  failed: number;       // Failed tasks
}
```

#### PlayStatus
```typescript
type PlayStatus = 'ok' | 'changed' | 'failed';
```

### Component Design

#### ServerCard
- Card-based design with dark slate background
- Server icon with color-coded status based on plays (red if any play failed, blue if any changed, green if all OK)
- Hostname prominently displayed
- Contains multiple PlayCard components
- Rounded corners with subtle shadow for depth

#### PlayCard
- Nested card design with lighter slate background
- Displays play name prominently with color-coded status
- Shows execution timestamp with calendar icon
- Three StatusBadge components showing task counts (OK/Changed/Failed)
- Compact design suitable for multiple plays per host

#### StatusBadge
- Reusable component for displaying status counts
- Color-coded backgrounds with semi-transparent overlays
- Border styling for definition
- Flex layout with label and count

#### PlayHeader (Legacy)
- Legacy component no longer used in main app
- Previously displayed play title and execution date
- Kept for potential future use

### Styling System

#### Color Palette (Dark Mode)
- **Background**: `bg-slate-900` - Deep dark slate
- **Host Cards**: `bg-slate-800` with `border-slate-700` - Medium dark slate
- **Play Cards**: `bg-slate-700` with `border-slate-600` - Lighter slate (nested)
- **Text Primary**: `text-slate-100` - Light gray
- **Text Secondary**: `text-slate-300` - Medium gray
- **Text Muted**: `text-slate-400` - Darker gray

#### Status Colors
- **OK**: Green theme (`bg-green-900/50`, `text-green-400`, `border-green-700`)
- **Changed**: Blue theme (`bg-blue-900/50`, `text-blue-400`, `border-blue-700`)
- **Failed**: Red theme (`bg-red-900/50`, `text-red-400`, `border-red-700`)

#### Responsive Layout
- **Mobile**: Single column grid
- **Tablet (md)**: 2-column grid
- **Desktop (lg)**: 3-column grid
- Consistent gap spacing and padding

## Development

### Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Run Linting**
   ```bash
   npm run lint
   ```
   Checks code quality with ESLint

3. **Start Development Server**
   ```bash
   npm run dev
   ```
   Server starts at `http://localhost:5173`

4. **Build for Production**
   ```bash
   npm run build
   ```
   Outputs to `dist/` directory

5. **Preview Production Build**
   ```bash
   npm run preview
   ```

### Project Scripts

- `npm run dev` - Start Vite dev server with hot reload
- `npm run build` - TypeScript compilation + production build
- `npm run lint` - Run ESLint on codebase
- `npm run preview` - Preview production build locally

### Mock Data

The first iteration uses hardcoded mock data in [src/App.tsx](src/App.tsx):
- 5 example hosts with realistic hostnames (web-01, web-02, db-01, lb-01, cache-01)
- Each host has 1-3 plays with descriptive names
- Mix of OK, Changed, and Failed play statuses
- Varied task counts per play (5-18 tasks)
- Execution timestamps showing relative times for each play

## Current Implementation (v0.1.0)

### Features
- Single-page display of Ansible execution results by host
- Host cards with status indicators based on play outcomes
- Multiple plays displayed per host with individual task summaries
- Color-coded badges for OK/Changed/Failed tasks per play
- Play names and execution timestamps
- Responsive grid layout
- Dark mode design with nested card hierarchy

### Limitations
- Static mock data (no backend integration)
- No historical play logs
- No filtering or search capabilities
- No authentication or user management
- No real-time updates

## Future Iterations

### Backend Integration (v0.2.0)
- REST API for fetching play results
- Persistent storage (PostgreSQL or MongoDB)
- API endpoints for CRUD operations
- WebSocket support for real-time updates

### Enhanced Features (v0.3.0)
- Historical play logs with pagination
- Search and filter capabilities
- Detailed task-level information
- Expandable server cards with task details
- Export functionality (JSON, CSV)

### Advanced Features (v0.4.0+)
- User authentication and authorization
- Multi-user support with role-based access
- Play scheduling and triggering
- Email/Slack notifications for failures
- Dashboard with analytics and trends
- Dark/Light mode toggle
- Customizable views and preferences

## File Organization

### Configuration Files
- [package.json](package.json) - Dependencies and scripts
- [vite.config.ts](vite.config.ts) - Vite build configuration
- [eslint.config.js](eslint.config.js) - ESLint configuration with TypeScript support
- [tsconfig.json](tsconfig.json) - TypeScript project references
- [tsconfig.app.json](tsconfig.app.json) - App TypeScript config
- [tsconfig.node.json](tsconfig.node.json) - Node scripts TypeScript config
- [tailwind.config.js](tailwind.config.js) - Tailwind CSS configuration
- [postcss.config.js](postcss.config.js) - PostCSS plugins
- [.gitignore](.gitignore) - Git ignore patterns

### Source Files
- [src/main.tsx](src/main.tsx) - React application entry point
- [src/App.tsx](src/App.tsx) - Main application component with mock host data
- [src/index.css](src/index.css) - Global styles and Tailwind directives
- [src/vite-env.d.ts](src/vite-env.d.ts) - Vite environment type declarations
- [src/types/ansible.ts](src/types/ansible.ts) - TypeScript type definitions (Host, Play, TaskSummary)
- [src/components/PlayCard.tsx](src/components/PlayCard.tsx) - Individual play card with task summaries
- [src/components/PlayHeader.tsx](src/components/PlayHeader.tsx) - (Legacy) Play title and date component
- [src/components/ServerCard.tsx](src/components/ServerCard.tsx) - Host card displaying multiple plays
- [src/components/StatusBadge.tsx](src/components/StatusBadge.tsx) - Status indicator badge

## Design Decisions

### Why Vite over Create React App?
- Significantly faster dev server startup
- Hot Module Replacement (HMR) is more responsive
- Smaller bundle sizes with better tree-shaking
- Native ESM support
- Better TypeScript integration

### Why Dark Mode First?
- Terminal-friendly aesthetic aligns with DevOps workflows
- Reduces eye strain for users monitoring systems
- Modern, professional appearance
- Better contrast for status colors

### Why Tailwind CSS?
- Rapid prototyping with utility classes
- Consistent design system
- Smaller CSS bundle (only used classes)
- No CSS naming conflicts
- Easy responsive design

### Why Lucide React?
- Lightweight icon library
- Consistent design language
- Tree-shakeable (only import icons you use)
- Active maintenance and updates
- Better than Font Awesome for React projects

### ESLint Configuration
The project uses modern ESLint flat config (eslint.config.js) with:
- **TypeScript ESLint**: Type-aware linting rules
- **React Hooks Plugin**: Ensures hooks are used correctly
- **React Refresh Plugin**: Validates Fast Refresh compatibility
- **Recommended Rulesets**: Industry-standard best practices

ESLint helps maintain code quality by:
- Catching potential bugs before runtime
- Enforcing consistent code style
- Identifying unused variables and imports
- Validating React patterns and TypeScript types

Run `npm run lint` before committing to ensure code quality.

## Quality Assurance

### Code Quality Checks
The project includes comprehensive code quality tooling:

**ESLint Configuration**
- Modern flat config format (eslint.config.js)
- TypeScript-aware linting with typescript-eslint
- React Hooks rules enforcement
- React Refresh compatibility checks

**TypeScript Strict Mode**
- Strict type checking enabled
- No unused locals or parameters allowed
- No fallthrough cases in switch statements
- No unchecked side effect imports

**Running Quality Checks**
```bash
# Run ESLint
npm run lint

# Run TypeScript compiler check (without emitting files)
npx tsc -b --noEmit

# Run both checks in CI/CD
npm run lint && npx tsc -b --noEmit
```

**Current Status**: ✅ All checks passing
- Zero ESLint errors or warnings
- Zero TypeScript type errors
- Production-ready codebase

## Contributing

When extending this project, follow these guidelines:

1. **Maintain Type Safety**: Always use TypeScript types from `src/types/`
2. **Component Reusability**: Create small, focused components
3. **Consistent Styling**: Use Tailwind utilities, avoid custom CSS
4. **Dark Mode First**: Design for dark mode, then adapt if light mode is added
5. **Responsive Design**: Test on mobile, tablet, and desktop viewports
6. **Accessibility**: Use semantic HTML and ARIA labels where appropriate

## Troubleshooting

### Port Already in Use
If port 5173 is occupied:
```bash
npm run dev -- --port 3000
```

### TypeScript Errors
Ensure all dependencies are installed:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Tailwind Styles Not Applying
Check that [src/index.css](src/index.css) is imported in [src/main.tsx](src/main.tsx) and contains the Tailwind directives.

## License

This project is for internal use. Backend integration and production deployment details will be added in future iterations.
