#!/bin/bash

# Default installation directory
DEFAULT_INSTALL_DIR="/opt/polly"

# Prompt user for installation directory
echo "Enter installation directory (press Enter for default: $DEFAULT_INSTALL_DIR):"
read -r INSTALL_DIR

# Use default if user input is empty
INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}

echo "Starting Polly installation to $INSTALL_DIR..."

# Remove the old installation directory if it exists
if [ -d "$INSTALL_DIR" ]; then
  echo "Removing old installation directory: $INSTALL_DIR"
  sudo rm -rf "$INSTALL_DIR" >/dev/null 2>&1
fi

echo "Configuring git safe directory..."
git config --global --add safe.directory "$INSTALL_DIR" >/dev/null 2>&1

echo "Cloning Polly repository..."
sudo git clone https://github.com/pollypm/polly.git "$INSTALL_DIR" >/dev/null 2>&1

echo "Saving latest commit hash..."
latest_commit=$(git -C "$INSTALL_DIR" rev-parse HEAD 2>/dev/null)
echo "$latest_commit" | sudo tee "$INSTALL_DIR/latest" >/dev/null

echo "Creating Polly launcher script..."
sudo tee /usr/local/bin/polly > /dev/null << EOF
#!/bin/bash
cd "$INSTALL_DIR" || exit 1
python3 "polly/main.py" "\$@"
EOF
sudo chmod +x /usr/local/bin/polly >/dev/null 2>&1

echo "Polly installation complete."