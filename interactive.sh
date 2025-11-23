# Interactive installation helper functions for Orchis theme

# Color codes for better UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print functions
print_header() {
  echo -e "\n${BOLD}${BLUE}╔══════════════════════════════════════════════════╗${NC}"
  echo -e "${BOLD}${BLUE}║                                                   ║${NC}"
  echo -e "${BOLD}${BLUE}║     🎨 Orchis Theme Installer                    ║${NC}"
  echo -e "${BOLD}${BLUE}║     Interactive Installation Mode                ║${NC}"
  echo -e "${BOLD}${BLUE}║                                                   ║${NC}"
  echo -e "${BOLD}${BLUE}╚══════════════════════════════════════════════════╝${NC}\n"
}

print_section() {
  echo -e "\n${BOLD}${CYAN}$1${NC}"
  echo -e "${CYAN}$(printf '─%.0s' {1..50})${NC}"
}

print_success() {
  echo -e "${GREEN}✓${NC} $1"
}

print_info() {
  echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}⚠${NC} $1"
}

# Multi-select menu (space-separated numbers)
# Usage: multi_select "Prompt" selected_array option1 option2 option3...
multi_select() {
  local prompt="$1"
  shift
  local result_var="$1"
  shift
  local options=("$@")
  local selections=()
  
  echo -e "\n${YELLOW}${prompt}${NC}"
  echo -e "${BLUE}Enter numbers separated by spaces (e.g., 1 3 5), or 'a' for all:${NC}\n"
  
  local i=1
  for option in "${options[@]}"; do
    echo "  $i) $option"
    ((i++))
  done
  echo "  a) All variants"
  echo ""
  
  read -p "$(echo -e ${YELLOW}Your selection: ${NC})" input
  
  # Handle 'all' option
  if [[ "$input" == "a" || "$input" == "A" ]]; then
    selections=("${options[@]}")
  else
    # Parse space-separated numbers
    for num in $input; do
      if [[ "$num" =~ ^[0-9]+$ ]] && [ "$num" -ge 1 ] && [ "$num" -le "${#options[@]}" ]; then
        selections+=("${options[$((num-1))]}")
      fi
    done
  fi
  
  if [ ${#selections[@]} -eq 0 ]; then
    echo -e "${YELLOW}No selection made, using defaults...${NC}"
    selections=("${options[@]}")
  fi
  
  # Return selections via global variable
  eval "$result_var=(\"\${selections[@]}\")"
  
  print_success "Selected: ${selections[*]}"
}

# Single select menu
# Usage: single_select "Prompt" result_var option1 option2 option3...
single_select() {
  local prompt="$1"
  shift
  local result_var="$1"
  shift
  local options=("$@")
  local selection=""
  
  echo -e "\n${YELLOW}${prompt}${NC}\n"
  
  select choice in "${options[@]}"; do
    if [[ -n "$choice" ]]; then
      selection="$choice"
      eval "$result_var=\"$selection\""
      print_success "Selected: $selection"
      break
    else
      echo -e "${RED}Invalid selection, please try again${NC}"
    fi
  done
}

# Yes/No prompt
# Usage: confirm "Question text" && do_something
confirm() {
  local prompt="$1"
  local default="${2:-n}"
  local response
  
  if [[ "$default" == "y" ]]; then
    read -p "$(echo -e ${YELLOW}${prompt} [Y/n]: ${NC})" response
    response=${response:-y}
  else
    read -p "$(echo -e ${YELLOW}${prompt} [y/N]: ${NC})" response
    response=${response:-n}
  fi
  
  [[ "$response" =~ ^[Yy]$ ]]
}

# Read input with default
# Usage: read_with_default "Prompt" "default_value" result_var
read_with_default() {
  local prompt="$1"
  local default="$2"
  local result_var="$3"
  local value
  
  read -p "$(echo -e ${YELLOW}${prompt} [${default}]: ${NC})" value
  value=${value:-$default}
  
  eval "$result_var=\"$value\""
}

# Print installation summary
print_summary() {
  echo -e "\n${BOLD}${CYAN}═══════════════════════════════════════════════════${NC}"
  echo -e "${BOLD}${CYAN}📋 INSTALLATION SUMMARY${NC}"
  echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════${NC}\n"
  
  [[ -n "${selected_themes[*]}" ]] && echo -e "${BOLD}Theme variants:${NC} ${selected_themes[*]}"
  [[ -n "${selected_colors[*]}" ]] && echo -e "${BOLD}Color modes:${NC}    ${selected_colors[*]}"
  [[ -n "${selected_sizes[*]}" ]] && echo -e "${BOLD}Size:${NC}           ${selected_sizes[*]}"
  [[ -n "${selected_icon}" ]] && echo -e "${BOLD}Icon:${NC}           ${selected_icon}"
  [[ -n "${selected_tweaks[*]}" ]] && echo -e "${BOLD}Tweaks:${NC}         ${selected_tweaks[*]}"
  [[ "$install_autoswitch" == "true" ]] && echo -e "${BOLD}Auto-switcher:${NC}  Yes"
  [[ "$install_libadwaita" == "true" ]] && echo -e "${BOLD}Libadwaita:${NC}     Yes"
  
  echo -e "\n${BLUE}ℹ Estimated size: ~50-200 MB (depending on variants)${NC}\n"
}
