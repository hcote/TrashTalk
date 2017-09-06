from trashtalk import app

if __name__ == '__main__':
    # Setup to override configuration. config_file is a path to config set in env var. Ex:
    # config_file = 'trashtalk/config/dev.py
    # app.config.from_envvar(config_file)
    app.run()

