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
