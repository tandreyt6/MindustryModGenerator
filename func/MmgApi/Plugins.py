class PluginLoader:
    def __init__(self, plugins: dict):
        for i in plugins:
            setattr(self, i, plugins[i])

Plugins = None