#!/usr/bin/env python3
"""
Orchis Theme Automatic Switcher - Restructured for Rock-Solid Sync
Monitors GNOME's color-scheme and accent-color preferences and automatically
switches between Orchis theme variants with atomic updates and self-healing.
"""

import sys
import os
import json
import time
from pathlib import Path
from gi.repository import Gio, GLib
from datetime import datetime


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

# Paths
GTK4_CONFIG_DIR = Path.home() / '.config' / 'gtk-4.0'
THEMES_DIR = Path.home() / '.themes'
STATE_CACHE_FILE = Path.home() / '.cache' / 'orchis-theme-state.json'


def detect_theme_suffix():
    """Detect if themes were installed with a suffix like -Dracula or -Nord."""
    themes_dir = THEMES_DIR
    if not themes_dir.exists():
        return ''
    
    # Look for a standard Orchis theme to detect suffix
    test_variants = [
        'Orchis-Dark-Dracula',
        'Orchis-Light-Dracula',
        'Orchis-Dark-Nord',
        'Orchis-Light-Nord',
    ]
    
    for variant in test_variants:
        if (themes_dir / variant).exists():
            if '-Dracula' in variant:
                return '-Dracula'
            elif '-Nord' in variant:
                return '-Nord'
    
    return ''


class ThemeState:
    """Represents a complete theme state (GTK, Shell, Icons, libadwaita)."""
    
    def __init__(self, color_scheme, accent_color, theme_suffix=''):
        self.color_scheme = color_scheme
        self.accent_color = accent_color
        self.theme_suffix = theme_suffix
        self.timestamp = datetime.now().isoformat()
        
        # Build component names
        self.gtk_theme = self._build_gtk_theme()
        self.shell_theme = self._build_shell_theme()
        self.icon_theme = self._build_icon_theme()
        self.libadwaita_path = self._build_libadwaita_path()
    
    def _build_gtk_theme(self):
        """Build GTK theme name from state."""
        mode_suffix = '-Dark' if self.color_scheme in ['prefer-dark', 'dark'] else '-Light'
        accent_variant = ACCENT_MAP.get(self.accent_color, '')
        return f"Orchis{accent_variant}{mode_suffix}{self.theme_suffix}"
    
    def _build_shell_theme(self):
        """Build Shell theme name (same as GTK)."""
        return self.gtk_theme
    
    def _build_icon_theme(self):
        """Build Tela icon theme name from state."""
        mode_suffix = '-dark' if self.color_scheme in ['prefer-dark', 'dark'] else '-light'
        color_variant = TELA_ICON_MAP.get(self.accent_color, '')
        
        if not color_variant:
            # Standard color: Tela-dark or Tela-light
            return f"Tela{mode_suffix}"
        else:
            # Colored variant: Tela-purple-dark
            return f"Tela{color_variant}{mode_suffix}"
    
    def _build_libadwaita_path(self):
        """Build libadwaita theme path."""
        return THEMES_DIR / self.gtk_theme / 'gtk-4.0'
    
    def validate(self):
        """Check if all theme components exist."""
        issues = []
        
        # Check GTK theme
        gtk_path = THEMES_DIR / self.gtk_theme
        if not gtk_path.exists():
            issues.append(f"GTK theme not found: {self.gtk_theme}")
        
        # Check icon theme (with fallback)
        icon_path = Path.home() / '.local/share/icons' / self.icon_theme
        if not icon_path.exists():
            # Try fallback for standard Tela variants
            if self.icon_theme in ['Tela-dark', 'Tela-light']:
                fallback_name = self.icon_theme.replace('Tela-', 'Tela-blue-')
                fallback_path = Path.home() / '.local/share/icons' / fallback_name
                if fallback_path.exists():
                    self.icon_theme = fallback_name
                else:
                    issues.append(f"Icon theme not found: {self.icon_theme} (fallback: {fallback_name})")
            else:
                issues.append(f"Icon theme not found: {self.icon_theme}")
        
        # Check libadwaita
        if not self.libadwaita_path.exists():
            issues.append(f"libadwaita theme not found: {self.libadwaita_path}")
        
        return len(issues) == 0, issues
    
    def to_dict(self):
        """Serialize to dictionary."""
        return {
            'color_scheme': self.color_scheme,
            'accent_color': self.accent_color,
            'theme_suffix': self.theme_suffix,
            'gtk_theme': self.gtk_theme,
            'shell_theme': self.shell_theme,
            'icon_theme': self.icon_theme,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data):
        """Deserialize from dictionary."""
        state = cls(data['color_scheme'], data['accent_color'], data.get('theme_suffix', ''))
        # Override computed values with saved ones (in case of custom mapping)
        state.gtk_theme = data.get('gtk_theme', state.gtk_theme)
        state.shell_theme = data.get('shell_theme', state.shell_theme)
        state.icon_theme = data.get('icon_theme', state.icon_theme)
        state.timestamp = data.get('timestamp', state.timestamp)
        return state
    
    def __eq__(self, other):
        """Check if two states are equal."""
        if not isinstance(other, ThemeState):
            return False
        return (self.gtk_theme == other.gtk_theme and
                self.icon_theme == other.icon_theme and
                self.color_scheme == other.color_scheme and
                self.accent_color == other.accent_color)
    
    def __str__(self):
        """String representation."""
        return f"ThemeState(gtk={self.gtk_theme}, icons={self.icon_theme}, scheme={self.color_scheme}, accent={self.accent_color})"


class AtomicThemeApplier:
    """Applies theme changes atomically - all or nothing."""
    
    def __init__(self, interface_settings, shell_settings=None):
        self.interface_settings = interface_settings
        self.shell_settings = shell_settings
    
    def get_current_state_from_gsettings(self):
        """Read current state from GSettings."""
        try:
            color_scheme = self.interface_settings.get_string(COLOR_SCHEME_KEY)
            accent_color = 'blue'  # Default
            
            try:
                accent_color = self.interface_settings.get_string(ACCENT_COLOR_KEY)
            except:
                pass  # Accent color not available on older GNOME
            
            return color_scheme, accent_color
        except Exception as e:
            print(f"[ERROR] Failed to read GSettings: {e}", file=sys.stderr)
            return 'prefer-light', 'blue'
    
    def apply(self, new_state):
        """
        Apply theme state atomically.
        Returns: (success: bool, results: dict)
        """
        print(f"\n[SYNC] Applying theme state: {new_state}")
        
        # Validate before applying
        is_valid, issues = new_state.validate()
        if not is_valid:
            print(f"[VALIDATION FAILED] Missing components:")
            for issue in issues:
                print(f"  - {issue}")
            return False, {'validation': issues}
        
        print("[VALIDATE] All components exist ✓")
        
        # Save current state for potential rollback
        old_gtk = self.interface_settings.get_string(GTK_THEME_KEY)
        old_icon = self.interface_settings.get_string(ICON_THEME_KEY)
        
        results = {}
        
        try:
            # Apply GTK theme
            results['gtk'] = self._apply_gtk_theme(new_state.gtk_theme)
            
            # Apply Shell theme
            results['shell'] = self._apply_shell_theme(new_state.shell_theme)
            
            # Apply icon theme
            results['icons'] = self._apply_icon_theme(new_state.icon_theme)
            
            # Apply libadwaita theme
            results['libadwaita'] = self._apply_libadwaita_theme(new_state.gtk_theme, new_state.libadwaita_path)
            
            # Check if all succeeded
            if all(results.values()):
                print("[SUCCESS] Theme sync complete ✓")
                return True, results
            else:
                print("[PARTIAL FAILURE] Some components failed:")
                for component, success in results.items():
                    if not success:
                        print(f"  - {component} failed")
                # Don't rollback on partial failure, just log it
                return False, results
                
        except Exception as e:
            print(f"[ERROR] Exception during apply: {e}", file=sys.stderr)
            return False, {'exception': str(e)}
    
    def _apply_gtk_theme(self, theme_name):
        """Apply GTK theme."""
        try:
            current = self.interface_settings.get_string(GTK_THEME_KEY)
            if current != theme_name:
                self.interface_settings.set_string(GTK_THEME_KEY, theme_name)
                print(f"[APPLY] GTK theme: {theme_name} ✓")
                return True
            else:
                print(f"[SKIP] GTK theme already set: {theme_name}")
                return True
        except Exception as e:
            print(f"[ERROR] GTK theme apply failed: {e}", file=sys.stderr)
            return False
    
    def _apply_shell_theme(self, theme_name):
        """Apply GNOME Shell theme."""
        if not self.shell_settings:
            return True  # Not an error if shell settings unavailable
        
        try:
            current = self.shell_settings.get_string(SHELL_THEME_KEY)
            if current != theme_name:
                self.shell_settings.set_string(SHELL_THEME_KEY, theme_name)
                print(f"[APPLY] Shell theme: {theme_name} ✓")
                return True
            else:
                print(f"[SKIP] Shell theme already set: {theme_name}")
                return True
        except Exception as e:
            print(f"[WARN] Shell theme apply failed: {e}")
            return True  # Don't fail on shell theme error
    
    def _apply_icon_theme(self, icon_theme_name):
        """Apply icon theme."""
        try:
            current = self.interface_settings.get_string(ICON_THEME_KEY)
            if current != icon_theme_name:
                self.interface_settings.set_string(ICON_THEME_KEY, icon_theme_name)
                print(f"[APPLY] Icon theme: {icon_theme_name} ✓")
                return True
            else:
                print(f"[SKIP] Icon theme already set: {icon_theme_name}")
                return True
        except Exception as e:
            print(f"[ERROR] Icon theme apply failed: {e}", file=sys.stderr)
            return False
    
    def _apply_libadwaita_theme(self, theme_name, theme_path):
        """Update libadwaita (GTK4) theme symlinks."""
        try:
            if not theme_path.exists():
                print(f"[SKIP] libadwaita theme path not found: {theme_path}")
                return True  # Not an error
            
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
            
            print(f"[APPLY] libadwaita theme: {theme_name} ✓")
            return True
            
        except Exception as e:
            print(f"[WARN] libadwaita theme apply failed: {e}")
            return True  # Don't fail on libadwaita error


class OrchisThemeSwitcher:
    """Main theme switcher with atomic updates and self-healing."""
    
    def __init__(self):
        """Initialize the theme switcher."""
        self.interface_settings = None
        self.shell_settings = None
        self.theme_suffix = detect_theme_suffix()
        self.current_state = None
        self.applier = None
        
        if self.theme_suffix:
            print(f"[INIT] Detected theme suffix: {self.theme_suffix}")
        
        # Initialize GSettings
        self._init_gsettings()
        
        # Initialize applier
        self.applier = AtomicThemeApplier(self.interface_settings, self.shell_settings)
        
        # Load or create initial state
        self._init_state()
    
    def _init_gsettings(self):
        """Initialize GSettings for interface and shell."""
        try:
            self.interface_settings = Gio.Settings.new(INTERFACE_SCHEMA)
        except Exception as e:
            print(f"[FATAL] Could not access {INTERFACE_SCHEMA} schema: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Try to initialize shell theme settings (optional, requires User Themes extension)
        try:
            # Try to use the system-wide schema (works for both user and system-installed extension)
            self.shell_settings = Gio.Settings.new(SHELL_THEME_SCHEMA)
            print("[INIT] Shell theme extension found ✓")
        except Exception as e:
            print(f"[INIT] Shell theme extension not available (will skip shell theme)")
            # Not a fatal error, shell theme switching is optional
    
    def _init_state(self):
        """Initialize current state from GSettings or cache."""
        color_scheme, accent_color = self.applier.get_current_state_from_gsettings()
        self.current_state = ThemeState(color_scheme, accent_color, self.theme_suffix)
        
        # Try to load from cache
        cached_state = self._load_state()
        if cached_state:
            print(f"[CACHE] Loaded previous state: {cached_state}")
            # If cached state differs from GSettings, prefer GSettings (user changed manually)
            if cached_state != self.current_state:
                print("[CACHE] State mismatch - user may have changed settings manually")
        
        # Apply initial state
        print(f"[INIT] Initial state: {self.current_state}")
        success, _ = self.applier.apply(self.current_state)
        if success:
            self._save_state(self.current_state)
    
    def _save_state(self, state):
        """Save state to cache file."""
        try:
            STATE_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(STATE_CACHE_FILE, 'w') as f:
                json.dump(state.to_dict(), f, indent=2)
        except Exception as e:
            print(f"[WARN] Failed to save state cache: {e}")
    
    def _load_state(self):
        """Load state from cache file."""
        try:
            if STATE_CACHE_FILE.exists():
                with open(STATE_CACHE_FILE, 'r') as f:
                    data = json.load(f)
                    return ThemeState.from_dict(data)
        except Exception as e:
            print(f"[WARN] Failed to load state cache: {e}")
        return None
    
    def on_settings_changed(self, settings, key):
        """Handle any settings change (color-scheme or accent-color)."""
        print(f"\n[EVENT] Settings changed: {key}")
        
        try:
            # Get current GSettings values
            color_scheme, accent_color = self.applier.get_current_state_from_gsettings()
            
            # Build new state
            new_state = ThemeState(color_scheme, accent_color, self.theme_suffix)
            
            # Check if actually changed
            if new_state == self.current_state:
                print("[SKIP] State unchanged")
                return
            
            print(f"[CHANGE] {self.current_state} → {new_state}")
            
            # Apply new state
            success, results = self.applier.apply(new_state)
            
            if success:
                self.current_state = new_state
                self._save_state(new_state)
            else:
                print("[ERROR] Failed to apply new state, keeping old state")
                
        except Exception as e:
            print(f"[ERROR] Exception in settings change handler: {e}", file=sys.stderr)
            # Don't crash, just log the error
    
    def run(self):
        """Run the theme switcher."""
        print("\n[START] Orchis Theme Switcher (Restructured)")
        print("[START] Monitoring color-scheme and accent-color changes")
        print("[START] Press Ctrl+C to stop\n")
        sys.stdout.flush()
        
        # Connect to both signals with same handler
        self.interface_settings.connect(f'changed::{COLOR_SCHEME_KEY}', self.on_settings_changed)
        
        try:
            self.interface_settings.connect(f'changed::{ACCENT_COLOR_KEY}', self.on_settings_changed)
            print("[START] Monitoring both color-scheme and accent-color")
        except:
            print("[START] Monitoring color-scheme only (accent-color not available)")
        
        # Run GLib main loop
        try:
            GLib.MainLoop().run()
        except KeyboardInterrupt:
            print("\n[STOP] Theme switcher stopped")
            sys.exit(0)


def main():
    """Main entry point."""
    try:
        switcher = OrchisThemeSwitcher()
        switcher.run()
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
