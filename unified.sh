#!/bin/bash

detect_os() {
    if [[ "$(uname)" == "Darwin" ]]; then
        echo "macos"
    elif [[ -f "/data/data/com.termux/files/usr/bin/pkg" ]]; then
        echo "termux"
    else
        echo "linux"
    fi
}

install_dependencies() {
    case $1 in
        macos)
            if ! command -v brew &> /dev/null; then
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew update
            if ! command -v python3 &> /dev/null; then
                brew install python
            fi
            ;;
        termux)
            pkg update -y
            pkg install -y python
            ;;
        linux)
            if ! command -v sudo &> /dev/null; then
                exit 1
            fi
            sudo apt update -y
            sudo apt install -y python3 python3-venv python3-pip
            ;;
    esac
}

setup_venv() {
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
}

install_python_packages() {
    if [ -f requirements-cli.txt ]; then
        pip install --upgrade pip
        pip install -r requirements-cli.txt
    fi
}

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
            ;;
    esac
}

OS=$(detect_os)
install_dependencies $OS
setup_venv
install_python_packages
run_script $1
deactivate
