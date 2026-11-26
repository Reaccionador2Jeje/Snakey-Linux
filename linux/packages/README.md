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

## snakey-theme

`snakey-theme` installs the official GTK2/GTK3 theme at
`/usr/share/themes/Snakey-Dark`. The XFCE XSettings defaults select it.
Build it on a Slackware 15.0 x86_64 host:

    sudo linux/packages/build-snakey-theme.sh

The Live builder adds the package as `local:snakey-theme` in the custom
liveslak package sequence. It inherits Adwaita icons and window decorations
rather than shipping a partial or incompatible icon/window-manager theme.
