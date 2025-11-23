#!/usr/bin/env python3
"""
Orchis Theme Automatic Switcher
Monitors GNOME's color-scheme and accent-color preferences and automatically
switches between Orchis theme variants (light/dark and color variants).
"""

import sys
import subprocess
import os
from pathlib import Path
from gi.repository import Gio, GLib


# Accent color mapping: GNOME accent-color -> Orchis variant suffix
ACCENT_MAP = {
    'blue': '',           # Default, no variant suffix
    'teal': '-Teal',
    'green': '-Green',
    'yellow': '-Yellow',
    'orange': '-Orange',
    'red': '-Red',
    'pink': '-Pink',
    'purple': '-Purple',
    'slate': '-Grey',     # Map slate to Grey variant
    'brown': '',          # Orchis doesn't have brown variant, use default
}

# Tela icon theme color mapping: GNOME accent-color -> Tela variant
TELA_ICON_MAP = {
    'blue': '',           # Default/standard, no color suffix
    'teal': '',           # Use blue (default) for teal since no teal variant
    'green': '-green',
    'yellow': '-yellow',
    'orange': '-orange',
    'red': '-red',
    'pink': '-pink',
    'purple': '-purple',
    'slate': '-grey',
    'brown': '-brown',    # Tela has brown variant
}

# GSettings schemas and keys
INTERFACE_SCHEMA = 'org.gnome.desktop.interface'
COLOR_SCHEME_KEY = 'color-scheme'
ACCENT_COLOR_KEY = 'accent-color'
GTK_THEME_KEY = 'gtk-theme'
ICON_THEME_KEY = 'icon-theme'

SHELL_THEME_SCHEMA = 'org.gnome.shell.extensions.user-theme'
SHELL_THEME_KEY = 'name'

# Libadwaita GTK4 config directory
GTK4_CONFIG_DIR = Path.home() / '.config' / 'gtk-4.0'
THEMES_DIR = Path.home() / '.themes'


class OrchisThemeSwitcher:
    """Monitors color-scheme and accent-color changes and switches themes accordingly."""
    
    def __init__(self):
        """Initialize the theme switcher."""
        self.interface_settings = None
        self.shell_settings = None
        self.current_accent = 'blue'  # Default accent color
        
        # Initialize GSettings for interface
        try:
            self.interface_settings = Gio.Settings.new(INTERFACE_SCHEMA)
        except Exception as e:
            print(f"Error: Could not access {INTERFACE_SCHEMA} schema: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Try to initialize shell theme settings (optional)
        try:
            # First try to load from extension's schema directory
            extension_dir = Path.home() / '.local/share/gnome-shell/extensions/user-theme@gnome-shell-extensions.gcampax.github.com'
            schema_dir = extension_dir / 'schemas'
            
            if schema_dir.exists():
                schema_source = Gio.SettingsSchemaSource.new_from_directory(
                    str(schema_dir),
                    Gio.SettingsSchemaSource.get_default(),
                    False
                )
                schema = schema_source.lookup(SHELL_THEME_SCHEMA, False)
                if schema:
                    self.shell_settings = Gio.Settings.new_full(schema, None, None)
                    print("✓ Shell theme extension found")
                else:
                    raise Exception("Schema not found in extension directory")
            else:
                raise Exception("Extension schema directory not found")
        except Exception as e:
            print(f"Warning: Shell theme extension not available: {e}")
            print("Shell theme switching will be disabled.")
    
    def get_theme_name(self, color_scheme, accent_color):
        """Build theme name from color scheme and accent color."""
        # Determine light or dark suffix
        if color_scheme in ['prefer-dark', 'dark']:
            mode_suffix = '-Dark'
        else:
            mode_suffix = '-Light'
        
        # Get accent variant (empty string for default blue)
        accent_variant = ACCENT_MAP.get(accent_color, '')
        
        # Build theme name: Orchis + accent-variant + mode-suffix
        # Examples: "Orchis-Purple-dark", "Orchis-light" (default blue)
        theme_name = f"Orchis{accent_variant}{mode_suffix}"
        
        return theme_name
    
    def get_icon_theme_name(self, color_scheme, accent_color):
        """Build Tela icon theme name from color scheme and accent color."""
        # Determine light or dark suffix
        if color_scheme in ['prefer-dark', 'dark']:
            mode_suffix = '-dark'
        else:
            mode_suffix = '-light'
        
        # Get Tela color variant
        color_variant = TELA_ICON_MAP.get(accent_color, '')
        
        # Build icon theme name: Tela + color-variant + mode-suffix
        # Examples: "Tela-purple-dark", "Tela-light" (standard blue)
        # Special case: standard color with just brightness
        if not color_variant:
            # Standard color: Tela-dark or Tela-light
            icon_theme_name = f"Tela{mode_suffix}"
        else:
            # Colored variant: Tela-purple-dark
            icon_theme_name = f"Tela{color_variant}{mode_suffix}"
        
        return icon_theme_name
    
    def apply_gtk_theme(self, theme_name):
        """Apply GTK theme using GSettings."""
        try:
            current_theme = self.interface_settings.get_string(GTK_THEME_KEY)
            if current_theme != theme_name:
                self.interface_settings.set_string(GTK_THEME_KEY, theme_name)
                print(f"✓ Applied GTK theme: {theme_name}")
                return True
            return False
        except Exception as e:
            print(f"Error: Could not set GTK theme: {e}", file=sys.stderr)
            return False
    
    def apply_icon_theme(self, icon_theme_name):
        """Apply icon theme using GSettings."""
        try:
            current_icon_theme = self.interface_settings.get_string(ICON_THEME_KEY)
            if current_icon_theme != icon_theme_name:
                # Check if theme exists (check in user's icons directory)
                icon_path = Path.home() / '.local/share/icons' / icon_theme_name
                print(f"[ICON] Checking icon path: {icon_path}", flush=True)
                if not icon_path.exists():
                    print(f"Warning: Icon theme {icon_theme_name} not installed at {icon_path}", flush=True)
                    return False
                
                self.interface_settings.set_string(ICON_THEME_KEY, icon_theme_name)
                print(f"✓ Applied icon theme: {icon_theme_name}", flush=True)
                return True
            print(f"[ICON] No change needed, already using: {icon_theme_name}", flush=True)
            return False
        except Exception as e:
            print(f"Warning: Could not set icon theme: {e}", flush=True)
            return False
    
    def apply_shell_theme(self, theme_name):
        """Apply GNOME Shell theme using GSettings."""
        if not self.shell_settings:
            return False
        
        try:
            current_theme = self.shell_settings.get_string(SHELL_THEME_KEY)
            if current_theme != theme_name:
                self.shell_settings.set_string(SHELL_THEME_KEY, theme_name)
                print(f"✓ Applied Shell theme: {theme_name}")
                return True
            return False
        except Exception as e:
            print(f"Warning: Could not set Shell theme: {e}")
            return False
    
    def apply_libadwaita_theme(self, theme_name):
        """Update libadwaita (GTK4) theme symlinks."""
        try:
            # Check if theme exists
            theme_path = THEMES_DIR / theme_name / 'gtk-4.0'
            if not theme_path.exists():
                return False
            
            # Ensure GTK4 config directory exists
            GTK4_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
            # Update symlinks
            gtk_css = GTK4_CONFIG_DIR / 'gtk.css'
            gtk_dark_css = GTK4_CONFIG_DIR / 'gtk-dark.css'
            assets = GTK4_CONFIG_DIR / 'assets'
            
            # Remove old symlinks
            for link in [gtk_css, gtk_dark_css, assets]:
                if link.exists() or link.is_symlink():
                    link.unlink()
            
            # Create new symlinks
            gtk_css.symlink_to(theme_path / 'gtk.css')
            gtk_dark_css.symlink_to(theme_path / 'gtk-dark.css')
            assets.symlink_to(theme_path / 'assets')
            
            print(f"✓ Applied libadwaita theme: {theme_name}")
            return True
            
        except Exception as e:
            print(f"Warning: Could not set libadwaita theme: {e}")
            return False
    
    def on_color_scheme_changed(self, settings, key):
        """Handle dark/light mode changes."""
        print(f"\n[EVENT] on_color_scheme_changed triggered", flush=True)
        try:
            color_scheme = settings.get_string(COLOR_SCHEME_KEY)
            accent_color = self.current_accent
            print(f"[EVENT] Color scheme: {color_scheme}, Accent: {accent_color}", flush=True)
            
            # Try to read current accent color
            try:
                accent_color = settings.get_string(ACCENT_COLOR_KEY)
                self.current_accent = accent_color
            except:
                pass  # Accent color not available (older GNOME)
            
            theme_name = self.get_theme_name(color_scheme, accent_color)
            
            print(f"[CHANGE] Color scheme changed to: {color_scheme}", flush=True)
            print(f"[CHANGE] Will apply theme: {theme_name}", flush=True)
            
            # Apply both GTK and Shell themes
            gtk_changed = self.apply_gtk_theme(theme_name)
            shell_changed = self.apply_shell_theme(theme_name)
            libadwaita_changed = self.apply_libadwaita_theme(theme_name)
            icon_changed = self.apply_icon_theme(self.get_icon_theme_name(color_scheme, accent_color))
            
            if not gtk_changed and not shell_changed and not libadwaita_changed and not icon_changed:
                print("No theme changes needed.")
                
        except Exception as e:
            print(f"Error handling color scheme change: {e}", file=sys.stderr)
            # Fall back to default light theme
            self.apply_gtk_theme("Orchis-Light")
            self.apply_shell_theme("Orchis-Light")
    
    def on_accent_color_changed(self, settings, key):
        """Handle accent color changes (GNOME 47+)."""
        print(f"\n[EVENT] on_accent_color_changed triggered", flush=True)
        try:
            accent_color = settings.get_string(ACCENT_COLOR_KEY)
            self.current_accent = accent_color
            print(f"[EVENT] Accent color: {accent_color}", flush=True)
            
            # Get current color scheme
            color_scheme = settings.get_string(COLOR_SCHEME_KEY)
            theme_name = self.get_theme_name(color_scheme, accent_color)
            
            print(f"[CHANGE] Accent color changed to: {accent_color}", flush=True)
            print(f"[CHANGE] Will apply theme: {theme_name}", flush=True)
            
            # Apply both GTK and Shell themes
            gtk_changed = self.apply_gtk_theme(theme_name)
            shell_changed = self.apply_shell_theme(theme_name)
            libadwaita_changed = self.apply_libadwaita_theme(theme_name)
            icon_changed = self.apply_icon_theme(self.get_icon_theme_name(color_scheme, accent_color))
            
            if not gtk_changed and not shell_changed and not libadwaita_changed and not icon_changed:
                print("No theme changes needed.")
                
        except Exception as e:
            print(f"Error handling accent color change: {e}", file=sys.stderr)
    
    def sync_initial_theme(self):
        """Sync theme on startup based on current color-scheme and accent-color."""
        try:
            color_scheme = self.interface_settings.get_string(COLOR_SCHEME_KEY)
            accent_color = 'blue'  # Default
            
            # Try to read accent color (may not exist on older GNOME)
            try:
                accent_color = self.interface_settings.get_string(ACCENT_COLOR_KEY)
            except:
                print("Note: Accent color setting not available (GNOME < 47)")
            
            self.current_accent = accent_color
            theme_name = self.get_theme_name(color_scheme, accent_color)
            
            print(f"Initial color scheme: {color_scheme}")
            print(f"Initial accent color: {accent_color}")
            print(f"[SYNC] Applying all themes for {color_scheme} + {accent_color}", flush=True)
            self.apply_gtk_theme(theme_name)
            self.apply_shell_theme(theme_name)
            self.apply_libadwaita_theme(theme_name)
            icon_theme_name = self.get_icon_theme_name(color_scheme, accent_color)
            print(f"[SYNC] Icon theme to apply: {icon_theme_name}", flush=True)
            self.apply_icon_theme(icon_theme_name)
            
        except Exception as e:
            print(f"Error syncing initial theme: {e}", file=sys.stderr)
            # Fall back to default light theme
            self.apply_gtk_theme("Orchis-Light")
            self.apply_shell_theme("Orchis-Light")
    
    def run(self):
        """Run the theme switcher."""
        print("[START] Monitoring both color-scheme and accent-color changes", flush=True)
        print("[START] Orchis theme switcher is running...", flush=True)
        print("[START] Press Ctrl+C to stop", flush=True)
        sys.stdout.flush()
        
        # Sync theme on startup
        self.sync_initial_theme()
        
        # Connect to color-scheme change signal
        self.interface_settings.connect(
            f'changed::{COLOR_SCHEME_KEY}',
            self.on_color_scheme_changed
        )
        
        # Connect to accent-color change signal (gracefully handle if not available)
        try:
            self.interface_settings.connect(
                f'changed::{ACCENT_COLOR_KEY}',
                self.on_accent_color_changed
            )
            print("Monitoring both color-scheme and accent-color changes")
        except:
            print("Monitoring color-scheme changes only (accent-color not available)")
        
        # Run GLib main loop
        try:
            print("[LOOP] Starting GLib main loop...", flush=True)
            GLib.MainLoop().run()
        except KeyboardInterrupt:
            print("\n[STOP] Theme switcher stopped.", flush=True)
            sys.exit(0)


def main():
    """Main entry point."""
    try:
        switcher = OrchisThemeSwitcher()
        switcher.run()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
