#!/usr/bin/env zsh

# Function to change directory to the project
function tomcd() {
    # Configurable base directory for projects
    local PROJECTS_DIR="${TOM_HOME:-.}/projects"
    
    local project_name=$1

    if [ -z "$project_name" ]; then
	echo "tomcd - quickly cd into a project directory"
	echo "author: João Iacillo"
        echo "usage: tomcd <project_name>"
        return 1
    fi

    local project_path="$PROJECTS_DIR/$project_name"

    if [ -d "$project_path" ]; then
        cd "$project_path" || echo "failed to change directory to '$project_path'"
    else
        echo "project '$project_name' does not exist"
    fi
}

