#!/bin/sh
# Keep the Snakey base package post-install hook intentionally minimal.
if [ -x /usr/bin/snakey-info ]; then
  chmod 0755 /usr/bin/snakey-info
fi
