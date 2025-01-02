#!/bin/bash

# Update the package lists
sudo apt-get update -y

# Install Python and pip
sudo apt-get install -y python3 python3-pip

# Install the required Python packages
pip3 install -r requirements-cli.txt

# Function to run the Python scripts
run_script() {
    case $1 in
        driveid)
            python3 gdrive_scripts/driveid.py
            ;;
        add_to_team_drive)
            python3 gdrive_scripts/add_to_team_drive.py
            ;;
        gen_sa_accounts)
            python3 gdrive_scripts/gen_sa_accounts.py
            ;;
        *)
            echo "Invalid script name"
            ;;
    esac
}

# Run the script based on the user input
run_script $1
