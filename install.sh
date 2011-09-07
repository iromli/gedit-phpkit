#!/usr/bin/env bash

PHPKIT=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
GEDIT_PLUGIN_DIR=~/.gnome2/gedit/plugins
MIME_DIR=~/.local/share/mime

echo "installing phpkit plugin"
if [[ ! -d $GEDIT_PLUGIN_DIR ]]; then
    mkdir -p $GEDIT_PLUGIN_DIR
fi
cp -R $PHPKIT/plugin/phpkit* $GEDIT_PLUGIN_DIR

echo "installing cakephp mime"
if [[ ! -d $MIME_DIR/packages ]]; then
    mkdir -p $MIME_DIR/packages
fi
cp $PHPKIT/mime/cakephp.xml $MIME_DIR/packages
update-mime-database $MIME_DIR
