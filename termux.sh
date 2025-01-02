#!/bin/bash

# Update the package lists
pkg update -y

# Install Python and pip
pkg install -y python python-pip

# Install the required Python packages
pip install -r requirements-cli.txt

# Function to run the Python scripts
run_script() {
    case $1 in
        driveid)
            python gdrive_scripts/driveid.py
            ;;
        add_to_team_drive)
            python gdrive_scripts/add_to_team_drive.py
            ;;
        gen_sa_accounts)
            python gdrive_scripts/gen_sa_accounts.py
            ;;
        *)
            echo "Invalid script name"
            ;;
    esac
}

# Run the script based on the user input
run_script $1
