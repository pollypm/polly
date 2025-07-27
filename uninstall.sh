#!/bin/bash

INSTALL_DIR="/opt/polly"
LAUNCHER_SCRIPT="/usr/local/bin/polly"

echo "Starting Polly uninstallation..."

# Remove the launcher script if it exists
if [ -f "$LAUNCHER_SCRIPT" ]; then
  echo "Removing Polly launcher script: $LAUNCHER_SCRIPT"
  sudo rm -f "$LAUNCHER_SCRIPT" >/dev/null 2>&1
fi

# Remove the installation directory if it exists
if [ -d "$INSTALL_DIR" ]; then
  echo "Removing Polly installation directory: $INSTALL_DIR"
  sudo rm -rf "$INSTALL_DIR" >/dev/null 2>&1
fi

echo "Removing git safe directory configuration..."
git config --global --unset safe.directory /opt/polly >/dev/null 2>&1

echo "Polly uninstallation complete."
