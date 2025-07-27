#!/bin/bash

INSTALL_DIR="/opt/polly"

# Fix git thing
git config --global --add safe.directory /opt/polly

# Clone files from the Polly repository.
sudo git clone https://github.com/pollypm/polly.git "$INSTALL_DIR"

# Creates a file with the latest commit version of Polly.
latest_commit=$(git -C "$INSTALL_DIR" rev-parse HEAD)
echo "$latest_commit" | sudo tee "$INSTALL_DIR/latest" >/dev/null

# Create a simple script that is run with the command `polly` that
# launches the Polly CLI.
sudo tee /usr/local/bin/polly > /dev/null << EOF
#!/bin/bash
cd "$INSTALL_DIR" || exit 1
python3 "polly/main.py" "\$@"
EOF
sudo chmod +x /usr/local/bin/polly