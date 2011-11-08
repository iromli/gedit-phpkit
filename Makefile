GEDIT_PLUGIN_DIR = ~/.local/share/gedit/plugins

install:
	@if [ ! -d $(GEDIT_PLUGIN_DIR) ]; then \
		mkdir -p $(GEDIT_PLUGIN_DIR);\
	fi
	@echo "installing phpkit plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/phpkit*;
	@cp -R phpkit* $(GEDIT_PLUGIN_DIR);
	@rm -rf $(GEDIT_PLUGIN_DIR)/phpkit/*.py[co];

uninstall:
	@echo "uninstalling phpkit plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/phpkit*;
