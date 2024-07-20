#!/bin/bash

# Update the system
sudo apt update -y

# Install Python and pip
sudo apt install -y python3 python3-pip

# Install the required Python packages
pip3 install -r requirements-cli.txt

# Function to run the Python scripts
run_script() {
    case $1 in
        driveid)
            python3 driveid.py
            ;;
        add_to_team_drive)
            python3 add_to_team_drive.py
            ;;
        gen_sa_accounts)
            python3 gen_sa_accounts.py
            ;;
        generate_drive_token)
            python3 generate_drive_token.py
            ;;
        generate_string_session)
            python3 generate_string_session.py
            ;;
        *)
            echo "Invalid option. Available options are: driveid, add_to_team_drive, gen_sa_accounts, generate_drive_token, generate_string_session."
            ;;
    esac
}

# Run the script based on the user input
run_script $1
