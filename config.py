#!/usr/bin/env python3

import os
import os.path
import sys
import yaml

_CONFIG = 'message'

_DEFAULT_MESSAGE = 'Hello, the world'


def main():
    config_file = os.path.join(os.environ['SNAP_APP_DATA_PATH'], _CONFIG)

    config_yaml = yaml.load(sys.stdin)
    if config_yaml:
        set_config(config_file, config_yaml)

    yaml.dump(get_config(config_file), stream=sys.stdout,
              default_flow_style=False)


def set_config(config_file, config_yaml={}):
    with open(config_file, 'w') as f:
        yaml.dump(_config(config_yaml), stream=f, default_flow_style=False)

    return config_yaml


def get_config(config_file):
    try:
        with open(config_file) as f:
            return yaml.load(f)
    except FileNotFoundError:
        return _config()


def _config(config_yaml={}):
    try:
        msg_value = config_yaml['config'][
            os.environ['SNAP_NAME']]['msg']
        if not isinstance( msg_value, str):
            config_yaml['config'][
                os.environ['SNAP_NAME']]['msg'] = _DEFAULT_MESSAGE
    except KeyError:
        msg = {
            'config': {
                os.environ['SNAP_NAME']: {
                    'msg': _DEFAULT_MESSAGE
                }
            }
        }
        config_yaml.update(msg)

    return config_yaml


if __name__ == '__main__':
    main()
