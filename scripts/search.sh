#!/usr/bin/env bash
#===============================================================================
# TuCarro Search Wrapper
#===============================================================================
# Wrapper script for searching vehicles on TuCarro.com.co
#
# Usage:
#   ./search.sh "Jeep Wrangler" Medellin 50000000
#   ./search.sh "BMW 335i" --hp-min 200
#
# Requirements:
#   - Python 3.6+
#   - requests library: pip install requests
#===============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#-------------------------------------------------------------------------------
# Helper functions
#-------------------------------------------------------------------------------

usage() {
    cat << EOF
${GREEN}TuCarro Search Wrapper${NC}

${YELLOW}Usage:${NC}
    $0 <query> [location] [max_price] [options]

${YELLOW}Examples:${NC}
    $0 "Jeep Wrangler" Medellin 50000000
    $0 "BMW 335i" --hp-min 200
    $0 "Audi A6" --year-min 2012

${YELLOW}Arguments:${NC}
    query         Search query (e.g., "Jeep Wrangler", "BMW 335i")
    location      Optional location filter (e.g., Medellin, Bogota)
    max_price     Optional maximum price in COP (e.g., 50000000)

${YELLOW}Options:${NC}
    --hp-min N    Minimum horsepower
    --year-min N  Minimum year
    --brand NAME  Brand filter (jeep, bmw, audi, ford, toyota, etc.)
    --output FILE Save results to JSON file
    --debug       Debug mode
    -h, --help   Show this help message

${YELLOW}Direct Python Usage:${NC}
    python3 $SCRIPT_DIR/scrape_tucarro.py "Jeep Wrangler" Medellin --max-price 50000000

EOF
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

#-------------------------------------------------------------------------------
# Check dependencies
#-------------------------------------------------------------------------------

check_dependencies() {
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed."
        exit 1
    fi
    
    # Check requests library
    if ! python3 -c "import requests" 2>/dev/null; then
        log_info "Installing requests library..."
        pip install requests --quiet
    fi
}

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

main() {
    # Parse arguments
    if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        usage
        exit 0
    fi
    
    # Check dependencies first
    check_dependencies
    
    # Build command
    PYTHON_SCRIPT="$SCRIPT_DIR/scrape_tucarro.py"
    
    if [[ ! -f "$PYTHON_SCRIPT" ]]; then
        log_error "Python script not found: $PYTHON_SCRIPT"
        exit 1
    fi
    
    # Run with all arguments
    log_info "Running TuCarro scraper..."
    python3 "$PYTHON_SCRIPT" "$@"
}

main "$@"
