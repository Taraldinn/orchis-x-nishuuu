# Orchis × Nishuuu - Enhanced Theme with Auto-Switcher

A beautifully enhanced version of the Orchis GTK theme with comprehensive automatic theme switching for GNOME, including full Tela icon integration.

## ✨ Features

### 🎨 Complete Theme System
- **9 Accent Colors**: Blue, Purple, Pink, Red, Orange, Yellow, Green, Teal, Grey (+ Brown icon support)
- **Multiple Variants**: Light/Dark modes, Compact panels, Solid panels, Custom tweaks
- **Matching Icon Themes**: Tela icons automatically sync with accent colors
- **libadwaita Support**: Consistent theming for modern GTK4 applications

### 🔄 Automatic Theme Switching
- **Real-time Sync**: Instantly switches all themes when changing accent colors
- **Dark Mode Toggle**: Seamlessly transitions between light and dark variants
- **Four Components**: Syncs GTK, GNOME Shell, icons, and libadwaita simultaneously
- **Systemd Service**: Runs automatically at login, no manual intervention needed

### 🚀 Features Added by Nishuuu
1. **Tela Icon Integration**: Full automatic icon theme switching with accent colors
2. **Brown Accent Support**: Added mapping for GNOME 47's brown accent color
3. **Enhanced Auto-Switcher**: Improved Python script with comprehensive logging
4. **Interactive Installer**: User-friendly installation with guided prompts
5. **Complete Uninstaller**: Clean removal of all components
6. **Debug Logging**: Detailed service logs for troubleshooting

## 📦 Installation

### ⚡ One-Line Install (Recommended)
Copy and paste this command into your terminal:

```bash
curl -sL https://raw.githubusercontent.com/Taraldinn/orchis-x-nishuuu/master/setup.sh | bash
```

This will:
1. Install necessary dependencies (sassc)
2. Download the theme files
3. Launch the interactive installer
4. Clean up temporary files automatically

### Manual Install
If you prefer to clone the repository manually:

```bash
git clone https://github.com/Taraldinn/orchis-x-nishuuu.git
cd orchis-x-nishuuu
chmod +x install.sh
./install.sh
```

The interactive installer will guide you through selecting:
- Color variants (Purple, Pink, Red, Orange, Yellow, Green, Teal, Grey)
- Panel tweaks (Solid, Compact, Black, Nord, Dracula, etc.)
- Automatic theme switcher installation
- Tela icon theme installation

### Command Line Install
```bash
# Install specific variants
./install.sh -c purple -c pink -t all --auto-switch --tela-icons

# Install all colors with auto-switcher
./install.sh -c all --auto-switch --tela-icons
```

## 🎯 Usage

### Automatic Switching
Once installed with `--auto-switch`, themes automatically change when you:
1. **Change Accent Color**: Settings → Appearance → Accent Color
2. **Toggle Dark Mode**: Settings → Appearance → Style

All four components (GTK, Shell, Icons, libadwaita) sync instantly!

### Manual Theme Selection
Use GNOME Tweaks or Settings to manually select themes:
- GTK Theme: `Orchis-<Color>-<Mode>` (e.g., `Orchis-Purple-Dark`)
- Icon Theme: `Tela-<color>-<mode>` (e.g., `Tela-purple-dark`)

### Monitoring
View auto-switcher logs:
```bash
journalctl --user -u orchis-theme-switcher.service -f
```

Check service status:
```bash
systemctl --user status orchis-theme-switcher.service
```

## 🗑️ Uninstallation

```bash
./uninstall.sh
```

Removes all Orchis themes, Tela icons, auto-switcher service, and resets to default GNOME theme.

## 🎨 Accent Color Support

| Accent | Orchis Theme | Tela Icons | Notes |
|--------|--------------|------------|-------|
| Blue | `Orchis-Dark/Light` | `Tela-dark/light` | Default |
| Purple | `Orchis-Purple-*` | `Tela-purple-*` | ✅ |
| Pink | `Orchis-Pink-*` | `Tela-pink-*` | ✅ |
| Red | `Orchis-Red-*` | `Tela-red-*` | ✅ |
| Orange | `Orchis-Orange-*` | `Tela-orange-*` | ✅ |
| Yellow | `Orchis-Yellow-*` | `Tela-yellow-*` | ✅ |
| Green | `Orchis-Green-*` | `Tela-green-*` | ✅ |
| Teal | `Orchis-Teal-*` | `Tela-dark/light` | Uses blue icons |
| Slate | `Orchis-Grey-*` | `Tela-grey-*` | ✅ |
| Brown | `Orchis-Dark/Light` | `Tela-brown-*` | Icons only |

## 📋 Requirements

- GNOME Shell 42+ (Full support for 47+)
- GTK 3.24+
- `sassc` for theme compilation
- `git` for Tela icon installation (optional)
- Python 3 with `gi` (GObject Introspection) for auto-switcher

## 🛠️ Components

### Enhanced Files
- `interactive-mode.sh` - Full-featured interactive installer
- `scripts/orchis-theme-switcher.py` - Auto-switcher with icon support
- `core.sh` - Installation functions including Tela integration
- `uninstall.sh` - Complete cleanup script

### Documentation
- `README-INTERACTIVE.md` - Interactive mode guide
- `UNINSTALL.md` - Uninstallation instructions

## 🐛 Troubleshooting

### Running Apps Don't Update
GTK applications load themes at startup. To see changes:
- **Quick**: Restart the application
- **Complete**: Log out and back in

### Icons Not Switching
Make sure Tela icons are installed:
```bash
./install.sh --tela-icons
```

Or run the sync script manually:
```bash
~/.local/bin/sync-icon-theme.sh
```

## 🔧 Advanced Features

### Quick Installation

After your first installation, the installer remembers your preferences in `~/.config/orchis-installer.conf`.

The next time you run the installer, you'll see:
```
Quick Install (Load previous settings)? [Y/n]:
```

Select **Yes** to instantly reinstall with your exact same choices!

### Dracula & Nord Colorscheme Support

If you install with the **Dracula** or **Nord** tweak enabled, the auto-switcher automatically detects the suffix and applies themes correctly.

**Note**: Dracula uses a fixed color palette, so all accent colors will appear similar (bluish/slate) in the UI. This is intentional Dracula behavior. If you want distinct accent color variations, reinstall without the Dracula tweak.

### Ubuntu Dock Theme Integration

The installer automatically supports both Dash to Dock and Ubuntu Dock extensions:
- Backs up original dock stylesheet
- Removes it so the theme stylesheet applies
- Enables custom theme setting

**After installation**, reload GNOME Shell to see dock theming:
- Press **Alt + F2**, type `r`, press Enter
- Or log out and log back in

**To restore original dock styling**:
```bash
sudo mv /usr/share/gnome-shell/extensions/ubuntu-dock@ubuntu.com/stylesheet.css.bak \
       /usr/share/gnome-shell/extensions/ubuntu-dock@ubuntu.com/stylesheet.css
```

## 🐛 Troubleshooting

### Accent Colors All Look the Same

**Cause**: You installed with the Dracula or Nord colorscheme, which uses a fixed color palette.

**Solution**: Reinstall without the Dracula/Nord tweak:
1. Run the uninstaller: `curl -sL https://raw.githubusercontent.com/Taraldinn/orchis-x-nishuuu/master/uninstall.sh | bash`
2. Run the installer again
3. When selecting tweaks, skip Dracula and Nord (select only: compact, macos, submenu, dock)

### Ubuntu Dock Not Using Theme

**Symptoms**: The dock still looks default even after installation.

**Solution**:
1. Check if custom theme is enabled:
   ```bash
   dconf read /org/gnome/shell/extensions/ubuntu-dock/apply-custom-theme
   ```
   Should return `true`. If not:
   ```bash
   dconf write /org/gnome/shell/extensions/ubuntu-dock/apply-custom-theme true
   ```

2. Remove the original stylesheet (it's already backed up):
   ```bash
   sudo rm /usr/share/gnome-shell/extensions/ubuntu-dock@ubuntu.com/stylesheet.css
   ```

3. Reload GNOME Shell: **Alt + F2** → type `r` → Enter

### Icons Not Changing with Accent Colors

**Cause**: Standard Tela-dark/Tela-light icons are missing.

**Solution**: The auto-switcher automatically falls back to Tela-blue-dark/Tela-blue-light. This is normal and works correctly.

### Themes Not Switching Automatically

**Check service status**:
```bash
systemctl --user status orchis-theme-switcher
```

**View logs**:
```bash
journalctl --user -u orchis-theme-switcher -f
```

**Restart service**:
```bash
systemctl --user restart orchis-theme-switcher
```

### Snap Theme Notifications

When switching themes, you may see notifications about installing snap themes. These are harmless.

**To install snap theme support**:
```bash
sudo snap install gtk-common-themes
sudo snap install gnome-42-2204  # Or your GNOME version
```

**To check if you use snaps**:
```bash
snap list
```

If you don't use snap applications, you can safely ignore these notifications.

## 📚 Additional Documentation

- [Auto-Switcher Details](docs/README-AUTO-SWITCH.md) - Comprehensive auto-switcher documentation
- [Interactive Mode Guide](docs/README-INTERACTIVE.md) - Interactive installer usage

## 🙏 Credits

- **Original Theme**: [Orchis Theme](https://github.com/vinceliuice/Orchis-theme) by vinceliuice
- **Icon Theme**: [Tela Icon Theme](https://github.com/vinceliuice/Tela-icon-theme) by vinceliuice
- **Enhancements**: Nishuuu (Taraldinn)

## 📄 License

This project maintains the original GPL-3.0 license from Orchis theme. Enhancements are also licensed under GPL-3.0.

## 🌟 Star This Repo!

If you find this enhanced theme useful, please give it a star ⭐

---

**Made with ❤️ by Nishuuu** | Based on the amazing Orchis theme by vinceliuice
