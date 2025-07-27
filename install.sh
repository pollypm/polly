#!/bin/bash

INSTALL_DIR="/opt/polly"

# Clone files from the Polly repository
# and move them to the $INSTALL_DIR directory.
sudo git clone https://github.com/pollypm/polly.git "$INSTALL_DIR"
sudo mv "$INSTALL_DIR/polly/"* "$INSTALL_DIR/"
sudo mv "$INSTALL_DIR/polly/".* "$INSTALL_DIR/" 2>/dev/null || true
sudo rm -rf "$INSTALL_DIR/polly"

# Creates a file with the latest tag version of Polly.
latest_tag=$(git -C "$INSTALL_DIR" describe --tags $(git -C "$INSTALL_DIR" rev-list --tags --max-count=1))
echo "$latest_tag" | sudo tee "$INSTALL_DIR/latest" >/dev/null

# Create a simple script that is run with the command `polly` that
# launches the Polly CLI.
sudo tee /usr/local/bin/polly > /dev/null << EOF
#!/bin/bash
cd "$INSTALL_DIR" || exit 1
python3 "polly/main.py" "\$@"
EOF
sudo chmod +x /usr/local/bin/polly