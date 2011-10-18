PHPKIT_DIR = $(dir $(CURDIR)/$(lastword $(MAKEFILE_LIST)))
GEDIT_PLUGIN_DIR = ~/.gnome2/gedit/plugins

install:
	@if [ ! -d $(GEDIT_PLUGIN_DIR) ]; then \
		mkdir -p $(GEDIT_PLUGIN_DIR);\
	fi
	@echo "installing phpkit plugin";
	@cp -R $(PHPKIT_DIR)/plugin/phpkit* $(GEDIT_PLUGIN_DIR);
	@rm -rf $(GEDIT_PLUGIN_DIR)/phpkit/*.py[co];

uninstall:
	@echo "uninstalling phpkit plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/phpkit*;

symlink:
	@echo "symlinking phpkit plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/phpkit*;
	@ln -s $(PHPKIT_DIR)/plugin/phpkit $(GEDIT_PLUGIN_DIR)/phpkit;
	@ln -s $(PHPKIT_DIR)/plugin/phpkit.gedit-plugin $(GEDIT_PLUGIN_DIR)/phpkit-gedit-plugin;
