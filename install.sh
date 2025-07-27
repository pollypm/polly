#!/bin/bash

INSTALL_DIR="/opt/polly"

echo "Starting Polly installation..."

# Remove the old installation directory if it exists.
if [ -d "$INSTALL_DIR" ]; then
  echo "Removing old installation directory: $INSTALL_DIR"
  sudo rm -rf "$INSTALL_DIR" >/dev/null 2>&1
fi

echo "Configuring git safe directory..."
git config --global --add safe.directory /opt/polly >/dev/null 2>&1

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