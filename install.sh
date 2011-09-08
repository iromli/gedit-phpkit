#!/usr/bin/env bash

PHPKIT=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
GEDIT_PLUGIN_DIR=~/.gnome2/gedit/plugins

echo "installing phpkit plugin"
if [[ ! -d $GEDIT_PLUGIN_DIR ]]; then
    mkdir -p $GEDIT_PLUGIN_DIR
fi
cp -R $PHPKIT/plugin/phpkit* $GEDIT_PLUGIN_DIR
