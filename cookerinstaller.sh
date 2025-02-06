#!/bin/bash

BINARY_URL="https://github.com/bluestar-b/bluestar-b/raw/refs/heads/main/cook"
BINARY_NAME="cook"
INSTALL_DIR="/usr/local/bin"
SERVICE_NAME="cook_service"

if systemctl is-active --quiet $SERVICE_NAME; then
    systemctl stop $SERVICE_NAME
fi

if [ -f "$INSTALL_DIR/$BINARY_NAME" ]; then
    rm -f "$INSTALL_DIR/$BINARY_NAME"
fi

curl -L $BINARY_URL -o "$INSTALL_DIR/$BINARY_NAME"
chmod +x "$INSTALL_DIR/$BINARY_NAME"

cat <<EOL > /etc/systemd/system/$SERVICE_NAME.service
[Unit]
Description=Cook Service
After=network.target

[Service]
ExecStart=$INSTALL_DIR/$BINARY_NAME
Restart=always
User=root
WorkingDirectory=$INSTALL_DIR

[Install]
WantedBy=multi-user.target
EOL

systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME
