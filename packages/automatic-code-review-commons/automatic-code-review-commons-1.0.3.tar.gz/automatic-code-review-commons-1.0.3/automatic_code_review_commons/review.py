import json
import os


def run(fn_review):
    path_config = os.path.dirname(os.path.abspath(__file__)) + "/config.json"

    with open(path_config, 'r') as arquivo:
        config = json.load(arquivo)

    comments = fn_review(config)
    path_output = config['path_output']

    with open(path_output, 'w') as arquivo:
        json.dump(comments, arquivo, indent=True)
