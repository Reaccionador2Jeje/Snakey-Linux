# Snakey Slackware packages

Snakey's native package layer is built with Slackware's own makepkg and
installed through Slackware pkgtools. Packages are ordinary Slackware .txz
archives; no Debian package manager or foreign package format is used.

## snakey-base

snakey-base provides /etc/snakey-release and /usr/bin/snakey-info.
Build it on a Slackware 15.0 x86_64 host:

    sudo linux/packages/build-snakey-base.sh

The liveslak builder places the resulting package in its local64/snakey-base
module directory, then includes it through SEQ_CUSTOM.
