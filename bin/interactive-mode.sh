# Interactive installation mode
# This file is sourced by install.sh when running in interactive mode

source "${REPO_DIR}/bin/interactive.sh"

CONFIG_FILE="$HOME/.config/orchis-installer.conf"

# Save configuration to file
save_config() {
  mkdir -p "$(dirname "$CONFIG_FILE")"
  
  cat > "$CONFIG_FILE" << EOF
# Orchis Theme Installer Configuration
selected_themes="${selected_themes[*]}"
selected_colors="${selected_colors[*]}"
selected_sizes="${selected_sizes[*]}"
selected_icon="${selected_icon}"
selected_tweaks="${selected_tweaks[*]}"
install_autoswitch="${install_autoswitch}"
install_libadwaita="${install_libadwaita}"
install_fixed="${install_fixed}"
install_tela="${install_tela}"
corner_radius="${corner_radius}"
EOF
}

# Load configuration from file
load_config() {
  if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
    
    # Convert string arrays back to arrays
    IFS=' ' read -r -a selected_themes <<< "$selected_themes"
    IFS=' ' read -r -a selected_colors <<< "$selected_colors"
    IFS=' ' read -r -a selected_sizes <<< "$selected_sizes"
    IFS=' ' read -r -a selected_tweaks <<< "$selected_tweaks"
    
    return 0
  fi
  return 1
}

interactive_mode() {
  # Display welcome header
  print_header
  
  echo -e "${BLUE}Welcome to the Orchis theme interactive installer!${NC}"
  echo -e "${BLUE}This guide will help you customize your installation.${NC}\n"
  
  if ! confirm "Would you like to continue with interactive installation?" "y"; then
    echo -e "\n${YELLOW}Installation cancelled. Run with --help to see all options.${NC}"
    exit 0
  fi
  
  # Initialize selection variables
  selected_themes=()
  selected_colors=()
  selected_sizes=()
  selected_icon=""
  selected_tweaks=()
  install_autoswitch="false"
  install_libadwaita="false"
  install_fixed="false"
  install_tela="false"
  corner_radius=""

  # Check for previous configuration
  if [[ -f "$CONFIG_FILE" ]]; then
    echo -e "\n${BLUE}Previous installation settings found!${NC}"
    if confirm "Quick Install (Load previous settings)?" "y"; then
      load_config
      print_success "Settings loaded"
      print_summary
      
      if confirm "Proceed with installation?" "y"; then
        build_install_args
        return 0
      fi
    fi
  fi
  
  # 1. Theme Color Variants
  print_section "1. Theme Color Variants"
  echo -e "${BLUE}Select which color variants to install:${NC}"
  
  theme_options=("default" "purple" "pink" "red" "orange" "yellow" "green" "teal" "grey")
  multi_select "Which color variants would you like?" selected_themes "${theme_options[@]}"
  
  # 2. Color Modes (Light/Dark)
  print_section "2. Color Modes"
  echo -e "${BLUE}Select which color modes to install:${NC}"
  
  color_options=("light" "dark" "standard")
  multi_select "Which color modes would you like?" selected_colors "${color_options[@]}"
  
  # 3. Size Variant
  print_section "3. Size Variant"
  echo -e "${BLUE}Select the size variant:${NC}"
  
  size_options=("standard" "compact" "both")
  single_select "Which size variant?" selected_size "${size_options[@]}"
  
  if [[ "$selected_size" == "both" ]]; then
    selected_sizes=("standard" "compact")
  else
    selected_sizes=("$selected_size")
  fi
  
  # 4. Icon Variant
  print_section "4. Panel Icon"
  echo -e "${BLUE}Select the activities button icon style:${NC}"
  
  if confirm "Use default ChromeOS-style icon?" "y"; then
    selected_icon="default"
    print_success "Selected: ChromeOS default"
  else
    icon_options=("apple" "simple" "gnome" "ubuntu" "arch" "manjaro" "fedora" "debian" "void" "opensuse" "popos" "zorin" "nixos" "gentoo" "budgie" "solus" "kali")
    single_select "Which icon style?" selected_icon "${icon_options[@]}"
  fi
  
  # 5. Tweaks
  print_section "5. Theme Tweaks (Optional)"
  echo -e "${BLUE}Select optional tweaks to apply:${NC}"
  
  tweak_options=(
    "solid - No transparency panel"
    "compact - No floating panel"
    "black - Full black variant"
    "primary - Primary radio color"
    "macos - macOS style buttons"
    "submenu - Themed submenus"
    "nord - Nord colorscheme"
    "dracula - Dracula colorscheme"
    "dock - Dash-to-dock fix"
  )
  
  echo -e "\n${YELLOW}Select tweaks (space-separated numbers), or press ENTER to skip:${NC}\n"
  
  local i=1
  for tweak in "${tweak_options[@]}"; do
    echo "  $i) $tweak"
    ((i++))
  done
  echo ""
  
  read -p "$(echo -e ${YELLOW}Your selection: ${NC})" tweak_input
  
  if [[ -n "$tweak_input" ]]; then
    for num in $tweak_input; do
      if [[ "$num" =~ ^[0-9]+$ ]] && [ "$num" -ge 1 ] && [ "$num" -le "${#tweak_options[@]}" ]; then
        tweak_name=$(echo "${tweak_options[$((num-1))]}" | cut -d' ' -f1)
        selected_tweaks+=("$tweak_name")
      fi
    done
    print_success "Selected tweaks: ${selected_tweaks[*]}"
  else
    print_info "No tweaks selected"
  fi
  
  # 6. Round Corners
  print_section "6. Round Corners (Optional)"
  
  if confirm "Customize corner radius?" "n"; then
    read_with_default "Enter corner radius in pixels (2-16)" "12" corner_radius
    print_success "Corner radius: ${corner_radius}px"
  fi
  
  # 7. Advanced Options
  print_section "7. Advanced Options"
  
  if confirm "Enable libadwaita support? (GTK4 apps)" "n"; then
    install_libadwaita="true"
    print_success "Libadwaita support enabled"
  fi
  
  # Detect GNOME Shell version
  if command -v gnome-shell &> /dev/null; then
    SHELL_VER=$(gnome-shell --version | cut -d ' ' -f 3 | cut -d . -f 1)
    print_info "Detected GNOME Shell version: $SHELL_VER"
    
    if [[ "$SHELL_VER" -ge 47 ]]; then
      if confirm "Use fixed accent color for libadwaita?" "n"; then
        install_fixed="true"
      fi
    fi
  fi
  
  # 8. Auto Theme Switcher
  print_section "8. Automatic Theme Switcher"
  echo -e "${BLUE}The auto-switcher automatically changes themes based on:${NC}"
  echo -e "${BLUE}  • GNOME dark/light preference${NC}"
  echo -e "${BLUE}  • Accent color (GNOME 47+)${NC}\n"
  
  if confirm "Install automatic theme switcher? (Recommended)" "y"; then
    install_autoswitch="true"
    print_success "Auto-switcher will be installed"
    
    # Ensure all color variants are selected if auto-switcher is enabled
    if [[ "$install_autoswitch" == "true" ]] && [[ ${#selected_themes[@]} -eq 1 ]] && [[ "${selected_themes[0]}" == "default" ]]; then
      print_warning "Auto-switcher works best with multiple color variants"
      if confirm "Install all color variants for full accent color support?" "y"; then
        selected_themes=("default" "purple" "pink" "red" "orange" "yellow" "green" "teal" "grey")
        print_success "All color variants will be installed"
      fi
    fi
  fi
  
  # 8.5 Tela Icon Theme
  print_section "8.5. Tela Icon Theme (Optional)"
  echo -e "${BLUE}Install matching Tela icon theme colors:${NC}"
  echo -e "${BLUE}  • Automatically matches accent colors${NC}"
  echo -e "${BLUE}  • Works with the auto-switcher${NC}"
  echo -e "${BLUE}  • Requires ~200 MB disk space${NC}\n"
  
  if confirm "Install Tela icon theme color variants?" "n"; then
    install_tela="true"
    print_success "Tela icon themes will be installed"
  fi
  
  # 9. Installation Summary & Confirmation
  print_summary
  
  if ! confirm "Proceed with installation?" "y"; then
    echo -e "\n${YELLOW}Installation cancelled.${NC}"
    exit 0
  fi
  
  # Save configuration
  save_config
  
  # Build command-line arguments from selections
  build_install_args
  
  # Return to main install script
  return 0
}

# Build installation arguments from interactive selections
build_install_args() {
  # Theme variants
  if [[ ${#selected_themes[@]} -gt 0 ]]; then
    themes=()
    for t in "${selected_themes[@]}"; do
      case "$t" in
        default) themes+=("${THEME_VARIANTS[0]}") ;;
        purple) themes+=("${THEME_VARIANTS[1]}") ;;
        pink) themes+=("${THEME_VARIANTS[2]}") ;;
        red) themes+=("${THEME_VARIANTS[3]}") ;;
        orange) themes+=("${THEME_VARIANTS[4]}") ;;
        yellow) themes+=("${THEME_VARIANTS[5]}") ;;
        green) themes+=("${THEME_VARIANTS[6]}") ;;
        teal) themes+=("${THEME_VARIANTS[7]}") ;;
        grey) themes+=("${THEME_VARIANTS[8]}") ;;
      esac
    done
  fi
  
  # Color modes
  if [[ ${#selected_colors[@]} -gt 0 ]]; then
    colors=()
    for c in "${selected_colors[@]}"; do
      case "$c" in
        standard) colors+=("${COLOR_VARIANTS[0]}") ;;
        light) colors+=("${COLOR_VARIANTS[1]}") ;;
        dark) colors+=("${COLOR_VARIANTS[2]}") ;;
      esac
    done
  fi
  
  # Size variants
  if [[ ${#selected_sizes[@]} -gt 0 ]]; then
    sizes=()
    for s in "${selected_sizes[@]}"; do
      case "$s" in
        standard) sizes+=("${SIZE_VARIANTS[0]}") ;;
        compact) sizes+=("${SIZE_VARIANTS[1]}") ;;
      esac
    done
  fi
  
  # Icon
  if [[ -n "$selected_icon" ]] && [[ "$selected_icon" != "default" ]]; then
    icon="-${selected_icon}"
    activities='icon'
  fi
  
  # Tweaks
  for tweak in "${selected_tweaks[@]}"; do
    case "$tweak" in
      solid) opacity="solid" ;;
      compact) panel="compact" ;;
      black) blackness="true" ;;
      primary) primary="true" ;;
      macos) macstyle="true" ;;
      submenu) submenu="true" ;;
      nord) nord="true"; ctype="-Nord" ;;
      dracula) dracula="true"; ctype="-Dracula" ;;
      dock) dockfix="true" ;;
    esac
  done
  
  # Round corners
  if [[ -n "$corner_radius" ]]; then
    round="true"
    corner="$corner_radius"
  fi
  
  # Libadwaita
  if [[ "$install_libadwaita" == "true" ]]; then
    libadwaita="true"
  fi
  
  # Fixed accent
  if [[ "$install_fixed" == "true" ]]; then
    fixed="true"
  fi
  
  # Auto-switcher
  if [[ "$install_autoswitch" == "true" ]]; then
    autoswitch="true"
  fi
  
  # Tela icons
  if [[ "$install_tela" == "true" ]]; then
    tela_icons="true"
  fi
}
