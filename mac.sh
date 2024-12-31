#!/bin/bash

# Check if Homebrew is installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Update Homebrew
brew update

# Install Python3 and pip
if ! command -v python3 &> /dev/null
then
    echo "Installing Python3..."
    brew install python
fi

if ! command -v pip3 &> /dev/null
then
    echo "Installing pip3..."
    python3 -m ensurepip --upgrade
fi

# Set up a Python virtual environment
if [ ! -d "venv" ]; then
    echo "Creating a Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating the virtual environment..."
source venv/bin/activate

# Install the required Python packages
if [ -f requirements-cli.txt ]; then
    echo "Installing Python packages from requirements-cli.txt..."
    pip install --upgrade pip
    pip install -r requirements-cli.txt
else
    echo "requirements-cli.txt not found. Skipping Python package installation."
fi

# Function to run the Python scripts
run_script() {
    case $1 in
        driveid)
            python driveid.py
            ;;
        add_to_team_drive)
            python add_to_team_drive.py
            ;;
        gen_sa_accounts)
            python gen_sa_accounts.py
            ;;
        generate_drive_token)
            python generate_drive_token.py
            ;;
        generate_string_session)
            python generate_string_session.py
            ;;
        *)
            echo "Invalid option. Available options are: driveid, add_to_team_drive, gen_sa_accounts, generate_drive_token, generate_string_session."
            ;;
    esac
}

# Run the script based on the user input
run_script $1

# Deactivate the virtual environment
deactivate
