#!/usr/bin/env sh
set -eu

MINECRAFT_VERSION="1.20.1"
FORGE_VERSION="47.4.23"
FORGE_COORD="${MINECRAFT_VERSION}-${FORGE_VERSION}"
INSTALLER="forge-${FORGE_COORD}-installer.jar"
ARGS="libraries/net/minecraftforge/forge/${FORGE_COORD}/unix_args.txt"

if [ ! -f "$ARGS" ]; then
  echo "Installing Forge ${FORGE_COORD}..."
  java -jar "$INSTALLER" --installServer
fi

exec java @user_jvm_args.txt @"$ARGS" nogui
