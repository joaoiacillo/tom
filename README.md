# Tom

Tom is a lightweight CLI tool for managing Docker-based development projects. It simplifies the process of creating, organizing, and controlling multiple Docker projects by providing an intuitive command-line interface with automatic docker-compose.yml generation, port conflict detection, and quick project navigation.

## Features

- 🚀 **Quick Project Creation**: Generate new Docker projects with pre-configured docker-compose.yml files
- 🔍 **Project Management**: List, navigate, and organize your Docker projects efficiently  
- 🐳 **Docker Integration**: Seamless docker-compose operations (up, down, ps) with project context
- 🔌 **Port Conflict Detection**: Automatically detects and warns about port conflicts between projects
- 📝 **Editor Integration**: Opens docker-compose.yml files in your preferred editor
- 🗂️ **Quick Navigation**: Use `tomcd` to instantly change to any project directory
- 🧹 **Container Cleanup**: Built-in commands for cleaning up stopped containers
- 📊 **Port Overview**: View all ports used across your projects at a glance

## Prerequisites

- **Docker** and **Docker Compose** installed and running
- **Python 3.6+** 
- **Git** (optional, for project initialization)
- A shell that supports sourcing (bash, zsh, etc.)

## Installation

```bash
# Set up Tom home directory
export TOM_HOME="$HOME/.tom"

# Clone the repository
git clone https://github.com/joaoiacillo/tom
mv tom "$TOM_HOME"

# Add to your shell configuration (bash/zsh)
echo -e "\n\n# Tom CLI\nexport TOM_HOME=\"$TOM_HOME\"\nsource \"$TOM_HOME/tomcd.sh\"\nalias tom=\"python3 \$TOM_HOME/tom.py\"" >> ~/.bashrc

# For zsh users, use ~/.zshrc instead:
# echo -e "\n\n# Tom CLI\nexport TOM_HOME=\"$TOM_HOME\"\nsource \"$TOM_HOME/tomcd.sh\"\nalias tom=\"python3 \$TOM_HOME/tom.py\"" >> ~/.zshrc

# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc
```

## Quick Start

```bash
# Create a new project
tom new my-web-app -p 3000:80 -i nginx:alpine

# List all projects
tom ls

# Navigate to a project
tomcd my-web-app

# Start the project
tom up my-web-app

# View running containers
tom ps my-web-app

# Stop the project
tom down my-web-app
```

## Commands

### Project Management

#### `tom new <project-name> [options]`
Create a new Docker project with automatic docker-compose.yml generation.

**Options:**
- `-p, --port PORT`: Port mapping (default: `8080:80`)
- `-i, --image IMAGE`: Base Docker image (default: `hello-world:latest`)
- `--no-git`: Skip git repository initialization
- `--editor EDITOR`: Editor to open docker-compose.yml (default: `vim`)

**Examples:**
```bash
# Create a basic project
tom new my-app

# Create a Node.js project with custom port
tom new node-api -p 3000:3000 -i node:18-alpine

# Create without git and open in VS Code
tom new frontend --no-git --editor code
```

#### `tom ls [filter...]`
List all projects. Optionally filter by name patterns.

**Examples:**
```bash
# List all projects
tom ls

# Filter projects containing "api"
tom ls api

# Multiple filters
tom ls web api
```

#### `tom rm <project-name> [options]`
Remove a project and its files.

**Options:**
- `-f, --force`: Skip confirmation prompt

**Examples:**
```bash
# Remove with confirmation
tom rm old-project

# Force remove without confirmation
tom rm old-project -f
```

### Docker Operations

#### `tom up <project-name> [docker-compose-args...]`
Start containers for a project (or current directory if no project specified).

**Examples:**
```bash
# Start a specific project
tom up my-web-app

# Start in detached mode
tom up my-web-app -d

# Start current directory project
tom up
```

#### `tom down <project-name> [docker-compose-args...]`
Stop containers for a project.

**Options:**
- `-a, --all`: Stop all running Docker containers (not just project containers)

**Examples:**
```bash
# Stop a specific project
tom down my-web-app

# Stop and remove volumes
tom down my-web-app -v

# Stop all containers
tom down -a
```

#### `tom ps <project-name> [docker-compose-args...]`
Show container status for a project.

**Options:**
- `-d, --docker`: Show global Docker containers instead of project-specific

**Examples:**
```bash
# Show project containers
tom ps my-web-app

# Show all Docker containers
tom ps -d
```

### Utilities

#### `tom path <project-name>`
Print the absolute path to a project directory.

```bash
tom path my-web-app
# Output: /home/user/.tom/projects/my-web-app
```

#### `tom ports`
Display all ports used by projects, grouped by project.

```bash
tom ports
# Output:
# my-web-app: 3000:3000
# api-server: 8080:80 5432:5432
```

#### `tom edit <project-name> [options]`
Open the docker-compose.yml file for editing.

**Options:**
- `--editor EDITOR`: Specify editor (default: `vim`)

**Examples:**
```bash
# Edit with default editor
tom edit my-web-app

# Edit with specific editor
tom edit my-web-app --editor code
```

#### `tom wash`
Clean up stopped Docker containers (equivalent to `docker container prune -f`).

```bash
tom wash
```

### Navigation

#### `tomcd <project-name>`
Quickly change to a project directory. This function is sourced from `tomcd.sh`.

```bash
tomcd my-web-app
# Changes current directory to the project folder
```

## Typical Workflows

### Starting a New Web Project
```bash
# Create a new React development project
tom new my-react-app -p 3000:3000 -i node:18-alpine --editor code

# Navigate to the project
tomcd my-react-app

# Edit the docker-compose.yml as needed, then start
tom up my-react-app -d

# Check status
tom ps my-react-app
```

### Managing Multiple Projects
```bash
# List all projects
tom ls

# Check which ports are in use
tom ports

# Start multiple projects
tom up frontend -d
tom up backend -d
tom up database -d

# View all running containers
tom ps -d

# Stop everything when done
tom down -a
```

### Project Cleanup
```bash
# Remove old project
tom rm old-project

# Clean up stopped containers
tom wash

# Check remaining projects
tom ls
```

## Configuration

Tom uses the `TOM_HOME` environment variable to determine where to store projects. By default, projects are stored in `$TOM_HOME/projects/`.

You can customize:
- **Project storage location**: Set `TOM_HOME` to your preferred directory
- **Default editor**: Use `--editor` flag or modify the default in commands
- **Default image**: Customize the default Docker image for new projects

## Troubleshooting

### Port Conflicts
If you see a port conflict warning when creating a project, Tom has detected that another project is already using that port. You can:
- Choose a different port with `-p`
- Check which project is using the port with `tom ports`
- Stop the conflicting project if needed

### Projects Not Found
If `tomcd` can't find a project:
- Verify the project exists with `tom ls`
- Check that `TOM_HOME` is correctly set
- Ensure you've sourced `tomcd.sh` in your shell configuration

### Permission Issues
If you encounter permission errors:
- Ensure Docker is running and you have permission to use it
- Check that `TOM_HOME` directory is writable
- Verify Python 3 is accessible

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Development Setup
```bash
git clone https://github.com/joaoiacillo/tom
cd tom
# Make your changes and test
python3 tom.py --help
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
