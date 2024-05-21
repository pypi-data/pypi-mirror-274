import inspect
import json
import os


def run(fn_review):
    stack = inspect.stack()
    caller_frame = stack[1]
    caller_file = caller_frame.filename
    path_config = os.path.dirname(os.path.abspath(caller_file)) + "/config.json"

    with open(path_config, 'r') as arquivo:
        config = json.load(arquivo)

    comments = fn_review(config)
    path_output = config['path_output']

    with open(path_output, 'w') as arquivo:
        json.dump(comments, arquivo, indent=True)
