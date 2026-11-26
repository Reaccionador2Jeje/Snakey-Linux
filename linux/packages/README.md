# Snakey Slackware packages

Snakey's native package layer is built with Slackware's own makepkg and
installed through Slackware pkgtools. Packages are ordinary Slackware .txz
archives; no Debian package manager or foreign package format is used.

## snakey-base

snakey-base provides /etc/snakey-release and /usr/bin/snakey-info.
Build it on a Slackware 15.0 x86_64 host:

    sudo linux/packages/build-snakey-base.sh

## snakey-theme

`snakey-theme` installs the official GTK2/GTK3 theme at
`/usr/share/themes/Snakey-Dark`. Build it with:

    sudo linux/packages/build-snakey-theme.sh

## snakey-control-center

`snakey-control-center` provides the main text-mode system panel, launched
from the XFCE desktop. It uses Python's standard library.

    sudo linux/packages/build-snakey-control-center.sh

## snakey-browser

`snakey-browser` adds Snakey Web to the XFCE application menu and registers
HTTP/HTTPS URL handling. It validates web addresses and launches a real
installed browser engine (Firefox, Chromium, Falkon or SeaMonkey). It does not
ship a fake HTML renderer or claim to implement TLS and modern web standards
itself. The actual browser engine must be present in the Slackware image.

    sudo linux/packages/build-snakey-browser.sh

The live-image build installs this package alongside the other Snakey
packages. At runtime, Snakey Web selects the first supported browser found;
set `SNAKEY_BROWSER` to an executable name to override the preference.
