#!/bin/bash
# Sophia Consciousness System - Unix/WSL Launcher

echo ""
echo "🌟 Sophia Consciousness System - WSL/Linux"
echo "=========================================="
echo ""

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python 3.8 or higher."
    echo "   Run: sudo apt update && sudo apt install python3 python3-pip"
    exit 1
fi

# Run the launcher
python3 sophia_launcher.py "$@"