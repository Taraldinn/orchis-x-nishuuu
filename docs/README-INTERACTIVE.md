# Orchis Theme - Interactive Installation Mode

## Quick Start

Simply run the installer without any arguments:

```bash
./install.sh
```

You'll be guided through an interactive menu to select all installation options.

## Features

The interactive installation mode provides a modern, user-friendly CLI experience with:

- 🎨 **Color-coded interface** for better readability
- 📋 **Step-by-step prompts** for all options
- ✅ **Multi-select menus** for variants and tweaks
- 📊 **Installation summary** before proceeding
- 🔄 **Auto-switcher integration** with smart recommendations
- ⌨️ **Keyboard-driven** navigation

## Interactive Flow

### 1. Theme Color Variants

Select which color variants to install:
- Default (Blue)
- Purple, Pink, Red
- Orange, Yellow, Green
- Teal, Grey
- Or all variants

### 2. Color Modes

Choose light, dark, or both modes.

### 3. Size Variant

Select standard, compact, or both sizes.

### 4. Panel Icon

Choose the activities button icon style (ChromeOS default, Apple, GNOME, distro logos, etc.).

### 5. Theme Tweaks

Optional customizations:
- Solid panel (no transparency)
- Compact panel (no floating)
- Black variant
- Primary radio color
- macOS style buttons
- Themed submenus
- Nord/Dracula colorschemes
- Dash-to-dock fixes

### 6. Round Corners

Optionally customize corner radius (2-16px).

### 7. Advanced Options

- Libadwaita support for GTK4 apps
- Fixed accent color for GNOME 47+

### 8. Auto Theme Switcher

Install the automatic theme switcher that:
- Switches between light/dark based on GNOME preference
- Switches accent colors (GNOME 47+)
- Switches icon theme colors to match
- Runs automatically at login

**Smart recommendation**: If you enable the auto-switcher with only the default theme, you'll be prompted to install all color variants for full accent color support.

### 8.5. Tela Icon Theme

Optionally install Tela icon theme color variants that automatically match your accent color:
- Includes all matching colors (purple, pink, red, orange, yellow, green, grey, blue)
- Works seamlessly with the auto-switcher
- Approximately 200 MB disk space required

### 9. Installation Summary

Review all selected options with estimated disk space before confirming.

## Traditional CLI Mode

All traditional command-line flags still work:

```bash
# Install specific variants
./install.sh -t purple pink red -c dark --auto-switch

# Install all with tweaks
./install.sh -t all --tweaks solid macos dock --auto-switch
```

## Example Interactive Session

```
╔══════════════════════════════════════════════════╗
║                                                   ║
║     🎨 Orchis Theme Installer                    ║
║     Interactive Installation Mode                ║
║                                                   ║
╚══════════════════════════════════════════════════╝

Welcome to the Orchis theme interactive installer!
This guide will help you customize your installation.

Would you like to continue with interactive installation? [Y/n]: y

──────────────────────────────────────────────────
1. Theme Color Variants
──────────────────────────────────────────────────

Which color variants would you like?
Enter numbers separated by spaces (e.g., 1 3 5), or 'a' for all:

  1) default
  2) purple
  3) pink
  4) red
  5) orange
  6) yellow
  7) green
  8) teal
  9) grey
  a) All variants

Your selection: 2 3 4

✓ Selected: purple pink red

[... more prompts ...]

──────────────────────────────────────────────────
8. Automatic Theme Switcher
──────────────────────────────────────────────────

The auto-switcher automatically changes themes based on:
  • GNOME dark/light preference
  • Accent color (GNOME 47+)

Install automatic theme switcher? (Recommended) [Y/n]: y

✓ Auto-switcher will be installed

═══════════════════════════════════════════════════
📋 INSTALLATION SUMMARY
═══════════════════════════════════════════════════

Theme variants: purple pink red
Color modes:    light dark
Size:           standard
Tweaks:         macos dock
Auto-switcher:  Yes

ℹ Estimated size: ~50-200 MB (depending on variants)

Proceed with installation? [Y/n]: y

Installing Orchis theme...
```

## Benefits

✅ **No need to memorize flags** - All options are presented clearly  
✅ **Discoverable** - See all available options in one place  
✅ **Guided** - Helpful descriptions for each option  
✅ **Safe** - Confirmation before installation  
✅ **Modern UX** - Matches experience of tools like Vite, create-react-app  
✅ **Backward compatible** - Traditional CLI still works  

## Tips

- Press **Enter** without input to use defaults
- Use **space-separated numbers** for multi-select (e.g., `1 3 5`)
- Type **'a'** in multi-select menus to select all options
- Press **Ctrl+C** to cancel at any time
- Run `./install.sh --help` to see all traditional CLI options
