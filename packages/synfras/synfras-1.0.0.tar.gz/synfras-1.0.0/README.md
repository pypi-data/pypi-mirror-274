# Sample Configs

## `.env`

```
ROOT_PATH_FOR_DYNACONF=""  # base dir for settings
SETTINGS_FILE_FOR_DYNACONF="settings.toml;.secrets.toml;.secrets.dev.toml"
ENVIRONMENTS_FOR_DYNACONF=true  # multi environments supported
SF_NUM_THREADS = 50  # multi threading
SF_NUM_PROCESSORS = 8  # multi processing
```

## `settings.toml`

```
[default]
[default.database]
url = 'database_url'
[default.output]
path = 'output_dir'

[dev]
[default.database]
url = 'dev_database_url'
[default.output]
path = 'dev_output_dir'
```
