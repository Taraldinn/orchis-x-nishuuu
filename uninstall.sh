#!/usr/bin/env bash
# Uninstall Orchis themes and Tela icon themes

# Don't exit on error - we want to complete all cleanup even if some steps fail
# set -e

echo "╔══════════════════════════════════════════════════╗"
echo "║                                                   ║"
echo "║  🗑️  Orchis & Tela Theme Uninstaller             ║"
echo "║                                                   ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Determine user
MY_USERNAME="${SUDO_USER:-$(logname 2>/dev/null || echo "${USER}")}"
MY_HOME=$(getent passwd "${MY_USERNAME}" | cut -d: -f6)

# Directories - check both possible theme locations
THEMES_DIRS=("${MY_HOME}/.themes" "${MY_HOME}/.local/share/themes")
ICONS_DIR="${MY_HOME}/.local/share/icons"
BIN_DIR="${MY_HOME}/.local/bin"
SYSTEMD_DIR="${MY_HOME}/.config/systemd/user"
GTK4_CONFIG_DIR="${MY_HOME}/.config/gtk-4.0"

echo "This will remove:"
echo "  • All Orchis theme variants"
echo "  • All Tela icon theme variants"
echo "  • Orchis theme switcher service"
echo "  • libadwaita (GTK4) symlinks"
echo ""

read -p "Continue with uninstall? [y/N]: " -n 1 -r < /dev/tty
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo " Uninstalling Orchis Themes"
echo "═══════════════════════════════════════════════════"
echo ""

# Find and remove all Orchis themes from both possible locations
removed_count=0
for themes_dir in "${THEMES_DIRS[@]}"; do
    if [[ -d "$themes_dir" ]]; then
        for theme in "$themes_dir"/Orchis*; do
            if [[ -d "$theme" ]]; then
                echo "  Removing: $(basename "$theme")"
                rm -rf "$theme" 2>/dev/null || echo "    Warning: Could not remove $theme"
                ((removed_count++))
            fi
        done
    fi
done

if [[ $removed_count -gt 0 ]]; then
    echo "✓ Removed $removed_count Orchis theme variants"
else
    echo "ℹ No Orchis themes found"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo " Uninstalling Tela Icon Themes"
echo "═══════════════════════════════════════════════════"
echo ""

# Find and remove all Tela icon themes
removed_count=0
if [[ -d "$ICONS_DIR" ]]; then
    for icon in "$ICONS_DIR"/Tela*; do
        if [[ -d "$icon" ]]; then
            echo "  Removing: $(basename "$icon")"
            rm -rf "$icon" 2>/dev/null || echo "    Warning: Could not remove $icon"
            ((removed_count++))
        fi
    done
    
    if [[ $removed_count -gt 0 ]]; then
        echo "✓ Removed $removed_count Tela icon theme variants"
    else
        echo "ℹ No Tela icon themes found"
    fi
else
    echo "ℹ Icons directory not found"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo " Removing Theme Switcher Service"
echo "═══════════════════════════════════════════════════"
echo ""

# Stop and disable service if running
if systemctl --user is-active orchis-theme-switcher.service &>/dev/null; then
    echo "  Stopping orchis-theme-switcher service..."
    systemctl --user stop orchis-theme-switcher.service
    echo "✓ Service stopped"
fi

if systemctl --user is-enabled orchis-theme-switcher.service &>/dev/null; then
    echo "  Disabling orchis-theme-switcher service..."
    systemctl --user disable orchis-theme-switcher.service
    echo "✓ Service disabled"
fi

# Remove service file
if [[ -f "${SYSTEMD_DIR}/orchis-theme-switcher.service" ]]; then
    echo "  Removing service file..."
    rm -f "${SYSTEMD_DIR}/orchis-theme-switcher.service"
    systemctl --user daemon-reload
    echo "✓ Service file removed"
fi

# Remove Python script
if [[ -f "${BIN_DIR}/orchis-theme-switcher.py" ]]; then
    echo "  Removing theme switcher script..."
    rm -f "${BIN_DIR}/orchis-theme-switcher.py"
    echo "✓ Script removed"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo " Removing libadwaita Symlinks"
echo "═══════════════════════════════════════════════════"
echo ""

# Remove GTK4/libadwaita symlinks
if [[ -d "$GTK4_CONFIG_DIR" ]]; then
    removed_links=false
    for link in "${GTK4_CONFIG_DIR}/"{assets,gtk.css,gtk-dark.css}; do
        if [[ -L "$link" ]]; then
            echo "  Removing: $(basename "$link")"
            rm -f "$link"
            removed_links=true
        fi
    done
    
    if [[ "$removed_links" == "true" ]]; then
        echo "✓ Removed GTK4 symlinks"
    else
        echo "ℹ No GTK4 symlinks found"
    fi
else
    echo "ℹ GTK4 config directory not found"
fi

echo ""
echo "══════════════════════════════════════════════════════"
echo " Reset to Default Themes"
echo "══════════════════════════════════════════════════════"
echo ""

# Reset to default GNOME themes
echo "  Setting default Adwaita theme..."
gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
gsettings set org.gnome.desktop.interface icon-theme 'Adwaita'

# Reset shell theme if user-theme extension exists
if [[ -d "${MY_HOME}/.local/share/gnome-shell/extensions/user-theme@gnome-shell-extensions.gcampax.github.com" ]]; then
    if gsettings --schemadir "${MY_HOME}/.local/share/gnome-shell/extensions/user-theme@gnome-shell-extensions.gcampax.github.com/schemas" \
        set org.gnome.shell.extensions.user-theme name '' 2>/dev/null; then
        echo "  Resetting GNOME Shell theme..."
    fi
fi

echo "✓ Reset to default themes"

echo ""
echo "══════════════════════════════════════════════════════"
echo " Summary"
echo "══════════════════════════════════════════════════════"
echo ""
echo "✓ Uninstall complete!"
echo ""
echo "All Orchis themes, Tela icons, and the auto-switcher have been removed."
echo "Your theme settings have been reset to Adwaita (GNOME default)."
echo ""
echo "You may need to log out and log back in for all changes to take effect."
echo ""
