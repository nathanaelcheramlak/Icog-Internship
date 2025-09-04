# Smart Task Scheduler

An intelligent task management application with dependency tracking and optimization using MeTTa (Meta Type Theory) for advanced scheduling algorithms.

## Features

- **Task Management**: Create, update, and delete tasks with priorities and deadlines
- **Dependency Tracking**: Define task dependencies to ensure proper execution order
- **Smart Scheduling**: MeTTa-powered scheduling using topological sorting and priority optimization
- **Visual Graph**: Interactive dependency graph visualization
- **Schedule Generation**: Generate optimal task execution schedules
- **Real-time Updates**: Live task completion tracking

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Lucide React** for icons

### Backend
- **Flask** Python web framework
- **MeTTa** (Meta Type Theory) for knowledge representation and logical reasoning


## Quick Start

### Prerequisites
- Node.js 18+ and pnpm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nathanaelcheramlak/Icog-Internship.git
   cd Smart-Scheduler
   ```

2. **Install frontend dependencies**
   ```bash
   cd client
   pnpm install
   ```

3. **Install backend dependencies**
   ```bash
   cd ../server
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd server
   python app.py
   ```
   The server will run on `http://localhost:5000`

2. **Start the frontend development server**
   ```bash
   cd client
   pnpm dev
   ```
   The application will be available at `http://localhost:5173`

## Usage

1. **Create Tasks**: Add new tasks with name, description, priority, and deadline
2. **Set Dependencies**: Define which tasks must be completed before others
3. **Generate Schedule**: Use the smart scheduler to get optimal task execution order
4. **View Graph**: Visualize task dependencies in an interactive graph
5. **Track Progress**: Mark tasks as complete and see real-time updates

## API Endpoints

- `GET /tasks` - Retrieve all tasks
- `POST /tasks` - Create a new task
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task
- `GET /schedule` - Generate optimal schedule
- `GET /graph` - Get task dependency graph

## Project Structure

```
Smart-Scheduler/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── lib/          # API utilities
│   │   ├── types/        # TypeScript type definitions
│   │   └── pages/        # Page components
│   └── package.json
├── server/                # Flask backend
│   ├── app.py            # Main Flask application
│   ├── utils.py          # Utility functions
│   └── pymetta.py        # MeTTa integration
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
