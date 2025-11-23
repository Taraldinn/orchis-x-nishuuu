#!/usr/bin/env bash
# Install all Tela icon theme color variants matching Orchis themes

SCRIPT_DIR="$(dirname "$(readlink -m "${0}")")"

echo "Installing Tela icon theme color variants..."
echo ""

# Tela color variants matching Orchis accent colors
COLORS=("blue" "purple" "pink" "red" "orange" "yellow" "green" "grey")

# Check if Tela repo is available
if [ ! -d "/tmp/tela-icon-theme" ]; then
    echo "Cloning Tela icon theme repository..."
    git clone --depth 1 https://github.com/vinceliuice/Tela-icon-theme.git /tmp/tela-icon-theme
fi

cd /tmp/tela-icon-theme

echo "Installing Tela color variants..."
for color in "${COLORS[@]}"; do
    echo "  Installing Tela-${color}..."
    ./install.sh "$color"
done

echo ""
echo "✓ All Tela color variants installed!"
echo ""
echo "Installed variants:"
ls ~/.local/share/icons/ | grep "^Tela-" | sort

echo ""
echo "Restart the theme switcher service to apply changes:"
echo "  systemctl --user restart orchis-theme-switcher.service"
