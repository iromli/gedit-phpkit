#!/usr/bin/env bash

PHPKIT=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
GEDIT_PLUGIN_DIR=~/.gnome2/gedit/plugins

echo "installing phpkit plugin"
mkdir -p $GEDIT_PLUGIN_DIR
cp -R $PHPKIT/plugin/phpkit* $GEDIT_PLUGIN_DIR
rm -rf $GEDIT_PLUGIN_DIR/phpkit/*.py[co]
