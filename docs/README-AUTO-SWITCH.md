# Orchis Automatic Theme Switcher

This feature enables automatic switching between Orchis theme variants based on GNOME's appearance preferences:
- **Light/Dark mode** – Automatically switch between light and dark variants
- **Accent color** – Automatically switch between color variants (Purple, Pink, Red, Orange, Yellow, Green, Teal, Grey)

## Requirements

- Python 3
- `python3-gi` (GObject Introspection bindings for Python)
- GNOME Desktop Environment
- **For accent colors**: GNOME 47+ (falls back to default blue on older versions)
- **Optional**: User Themes extension (for shell theme switching)
- **Important**: Install the Orchis color variants you want to use

## Installation

### Automatic Installation

**For full accent color support**, install all Orchis color variants first, then add the auto-switcher:

```bash
# Install all color variants + auto-switcher
./install.sh -t all --auto-switch

# Or install specific variants you want + auto-switcher
./install.sh -t purple pink red --auto-switch
```

**For basic light/dark switching only** (no accent color variants):

```bash
./install.sh --auto-switch
```

This will:
1. Install the watcher script to `~/.local/bin/orchis-theme-switcher.py`
2. Install the systemd service to `~/.config/systemd/user/orchis-theme-switcher.service`
3. Enable and start the service automatically

### Manual Installation

If you prefer to install manually:

```bash
# Create directories
mkdir -p ~/.local/bin
mkdir -p ~/.config/systemd/user

# Copy and make script executable
cp scripts/orchis-theme-switcher.py ~/.local/bin/
chmod +x ~/.local/bin/orchis-theme-switcher.py

# Copy service file
cp scripts/orchis-theme-switcher.service ~/.config/systemd/user/

# Enable and start the service
systemctl --user daemon-reload
systemctl --user enable orchis-theme-switcher.service
systemctl --user start orchis-theme-switcher.service
```

## How It Works

The automatic theme switcher monitors two GNOME settings:

### 1. Dark/Light Mode

Monitors `org.gnome.desktop.interface color-scheme`:
- **Dark mode** (`prefer-dark` or `dark`) → Uses `-dark` suffix
- **Light mode** (`prefer-light`, `light`, or `default`) → Uses `-light` suffix

### 2. Accent Color (GNOME 47+)

Monitors `org.gnome.desktop.interface accent-color` and maps to Orchis variants:

| GNOME Accent | Orchis Variant | Example Themes |
|--------------|----------------|----------------|
| `blue` | *default* | `Orchis-light`, `Orchis-dark` |
| `purple` | `-Purple` | `Orchis-Purple-light`, `Orchis-Purple-dark` |
| `pink` | `-Pink` | `Orchis-Pink-light`, `Orchis-Pink-dark` |
| `red` | `-Red` | `Orchis-Red-light`, `Orchis-Red-dark` |
| `orange` | `-Orange` | `Orchis-Orange-light`, `Orchis-Orange-dark` |
| `yellow` | `-Yellow` | `Orchis-Yellow-light`, `Orchis-Yellow-dark` |
| `green` | `-Green` | `Orchis-Green-light`, `Orchis-Green-dark` |
| `teal` | `-Teal` | `Orchis-Teal-light`, `Orchis-Teal-dark` |
| `slate` | `-Grey` | `Orchis-Grey-light`, `Orchis-Grey-dark` |

### Combined Theme Switching

The switcher combines both settings to build the complete theme name:

**Formula**: `Orchis` + *accent-variant* + *mode-suffix*

**Examples**:
- Blue accent + Light mode = `Orchis-light`
- Purple accent + Dark mode = `Orchis-Purple-dark`
- Teal accent + Light mode = `Orchis-Teal-light`

The switcher updates both:
- GTK theme (`org.gnome.desktop.interface gtk-theme`)
- GNOME Shell theme (`org.gnome.shell.extensions.user-theme name`) - if User Themes extension is installed

## Usage

### Service Management

```bash
# Check service status
systemctl --user status orchis-theme-switcher

# View real-time logs
journalctl --user -u orchis-theme-switcher -f

# Stop the service
systemctl --user stop orchis-theme-switcher

# Start the service
systemctl --user start orchis-theme-switcher

# Disable automatic startup
systemctl --user disable orchis-theme-switcher

# Re-enable automatic startup
systemctl --user enable orchis-theme-switcher
```

### Testing the Switcher

To test the automatic theme switching:

**Test Dark/Light Mode**:
1. Open **Settings** → **Appearance**
2. Toggle between **Light** and **Dark** styles
3. The theme should change automatically within a second

**Test Accent Colors** (GNOME 47+ only):
1. Open **Settings** → **Appearance**
2. Select different accent colors (Purple, Pink, Red, etc.)
3. The theme should change to the matching Orchis variant
4. Toggle dark/light mode to see combined changes

**Monitor in Real-time**:
```bash
journalctl --user -u orchis-theme-switcher -f
```

Expected output:
```
Initial color scheme: prefer-light
Initial accent color: blue
✓ Applied GTK theme: Orchis-light
Monitoring both color-scheme and accent-color changes
Accent color changed to: purple
✓ Applied GTK theme: Orchis-Purple-light
Color scheme changed to: prefer-dark
✓ Applied GTK theme: Orchis-Purple-dark
```

### Manual Execution

You can also run the script manually (without the systemd service):

```bash
~/.local/bin/orchis-theme-switcher.py
```

Press `Ctrl+C` to stop it.

## Troubleshooting

### Service not starting

Check the service status for errors:

```bash
systemctl --user status orchis-theme-switcher
```

### Python dependencies missing

Install the required Python GObject Introspection library:

```bash
# Debian/Ubuntu
sudo apt install python3-gi

# Fedora
sudo dnf install python3-gobject

# Arch Linux
sudo pacman -S python-gobject
```

### Shell theme not changing

The User Themes extension is required for GNOME Shell theme switching:

1. Install User Themes extension from [extensions.gnome.org](https://extensions.gnome.org/extension/19/user-themes/)
2. Enable it in Extensions app
3. Restart the switcher service:
   ```bash
   systemctl --user restart orchis-theme-switcher
   ```

### Theme names don't match

**For basic light/dark switching:**
The switcher uses theme names `Orchis-light` and `Orchis-dark` by default.

**For accent color variants:**
Make sure you've installed the Orchis color variants:
```bash
# Install all variants
./install.sh -t all

# Or specific variants
./install.sh -t purple pink red orange yellow green teal grey
```

If you installed Orchis with custom options (e.g., compact size, tweaks), the theme names may differ. Edit `~/.local/bin/orchis-theme-switcher.py` and modify the `ACCENT_MAP` or theme building logic.

### Dracula/Nord Variant Support

The auto-switcher **automatically detects** if you installed with Dracula or Nord tweaks and applies the correct suffix.

**How it works**:
1. On startup, the switcher checks `~/.themes/` for installed Orchis variants
2. If it finds themes with `-Dracula` or `-Nord` suffix, it automatically uses that suffix
3. Logs will show: `Detected theme suffix: -Dracula`

**Example**:
- Installed with Dracula tweak: `Orchis-Purple-Dark-Dracula`
- Installed with Nord tweak: `Orchis-Purple-Dark-Nord`
- Standard installation: `Orchis-Purple-Dark`

**Note**: Dracula colorscheme uses a fixed color palette, so all accent colors will appear visually similar (bluish/slate) in the UI. This is intentional Dracula behavior - the themes ARE switching (check logs), but they look similar due to Dracula's design.

To see distinct accent color variations, reinstall without the Dracula/Nord tweak.

### Accent colors not working

**Check GNOME version**:
```bash
gnome-shell --version
```
Accent color support requires GNOME 47+. On older versions, the switcher will still work but only for light/dark mode.

**Check if accent color setting is available**:
```bash
gsettings get org.gnome.desktop.interface accent-color
```
If this returns an error, your GNOME version doesn't support accent colors.

### Color variant not switching

If changing accent color doesn't switch the theme:
1. Verify the color variant is installed: `ls ~/.themes/ | grep Orchis`
2. Check logs: `journalctl --user -u orchis-theme-switcher -n 50`
3. The switcher may log warnings if a variant isn't found but will continue working

### Uninstallation

To completely remove the automatic theme switcher:

```bash
# Stop and disable the service
systemctl --user stop orchis-theme-switcher
systemctl --user disable orchis-theme-switcher

# Remove files
rm ~/.local/bin/orchis-theme-switcher.py
rm ~/.config/systemd/user/orchis-theme-switcher.service

# Reload systemd
systemctl --user daemon-reload
```

## Technical Details

The switcher is a lightweight Python daemon that:
- Uses GObject Introspection (`gi.repository`) to monitor GSettings
- Runs continuously with minimal resource usage
- Automatically restarts on failure (configured in systemd service)
- Handles errors gracefully and falls back to light theme on errors
- Supports both GTK and GNOME Shell theme switching

The systemd service ensures the switcher:
- Starts automatically with your user session
- Restarts if it crashes (with a 5-second delay)
- Runs in the background without user interaction
