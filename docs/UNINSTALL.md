# Uninstall Orchis & Tela Themes

[uninstall.sh](file:///home/aldinn/Downloads/Orchis-theme-master/uninstall.sh) - Complete uninstaller for Orchis and Tela themes

## What It Removes

1. **All Orchis Theme Variants**
   - All color variants (Purple, Pink, Red, Orange, Yellow, Green, Teal, Grey)
   - All modes (Light, Dark)
   - All sizes (Standard, Compact)
   - All special variants (Nord, Dracula)

2. **All Tela Icon Theme Variants**
   - All color variants (blue, purple, pink, red, orange, yellow, green, grey, brown, etc.)
   - All brightness variants (standard, light, dark)

3. **Orchis Theme Switcher**
   - Stops and disables the systemd service
   - Removes the Python switcher script from `~/.local/bin/`
   - Removes the service file from `~/.config/systemd/user/`

4. **libadwaita Symlinks**
   - Removes GTK4 theme symlinks from `~/.config/gtk-4.0/`

5. **Resets to Defaults**
   - Sets GTK theme to `Adwaita`
   - Sets icon theme to `Adwaita`
   - Resets GNOME Shell theme to default

## Usage

```bash
cd ~/Downloads/Orchis-theme-master
./uninstall.sh
```

The script will:
- Show you what will be removed
- Ask for confirmation before proceeding
- Display progress for each step
- Provide a summary at the end

## Features

- ✅ Interactive confirmation prompt
- ✅ Safe - only removes Orchis and Tela themes
- ✅ Colored, easy-to-read output
- ✅ Comprehensive removal of all related components
- ✅ Automatic theme reset to GNOME defaults
- ✅ Progress indicators for each step

## After Uninstall

You may need to:
- Log out and log back in for all changes to take effect
- Restart running GTK applications to see the default theme

Your system will be using the default GNOME Adwaita theme.

## Reinstalling

To reinstall after uninstalling:
```bash
cd ~/Downloads/Orchis-theme-master
./install.sh
```
