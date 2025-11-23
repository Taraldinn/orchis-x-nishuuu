#!/bin/bash
# One-line installer for Orchis x Nishuuu Theme
# Usage: curl -sL https://raw.githubusercontent.com/Taraldinn/orchis-x-nishuuu/master/setup.sh | bash

set -e

REPO_URL="https://github.com/Taraldinn/orchis-x-nishuuu.git"
INSTALL_DIR="/tmp/orchis-x-nishuuu"
BRANCH="master"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                   ║${NC}"
echo -e "${BLUE}║  🌸 Orchis x Nishuuu Theme Installer             ║${NC}"
echo -e "${BLUE}║                                                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# Check dependencies
echo -e "${BLUE}Checking dependencies...${NC}"
deps_missing=false

if ! command -v git >/dev/null 2>&1; then
    echo -e "${RED}Error: git is not installed.${NC}"
    deps_missing=true
fi

if ! command -v sassc >/dev/null 2>&1; then
    echo -e "${YELLOW}Warning: sassc is not installed (needed for theme compilation).${NC}"
    echo -e "Attempting to install sassc..."
    
    if command -v apt >/dev/null 2>&1; then
        sudo apt update && sudo apt install -y sassc
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y sassc
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -S --noconfirm sassc
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install -y sassc
    else
        echo -e "${RED}Could not install sassc automatically. Please install it manually.${NC}"
        deps_missing=true
    fi
fi

if [ "$deps_missing" = true ]; then
    echo -e "${RED}Missing dependencies. Please install them and try again.${NC}"
    exit 1
fi

# Clone repository
echo -e "\n${BLUE}Downloading theme files...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
fi

git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$INSTALL_DIR"

# Run installer
echo -e "\n${BLUE}Starting installer...${NC}"
cd "$INSTALL_DIR"
chmod +x install.sh

# Pass any arguments to the installer
./install.sh "$@"

# Cleanup
echo -e "\n${BLUE}Cleaning up...${NC}"
cd ~
rm -rf "$INSTALL_DIR"

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "To uninstall in the future, clone the repo and run uninstall.sh"
