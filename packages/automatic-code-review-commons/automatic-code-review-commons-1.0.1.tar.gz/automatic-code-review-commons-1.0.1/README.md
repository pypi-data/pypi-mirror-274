# automatic-code-review-commons

Biblioteca com funções genéricas para revisões automáticas de código da ferramenta ACR.

- [DOCS](https://github.com/automatic-code-review/docs/wiki)
- [VERSIONS](https://pypi.org/project/automatic-code-review-commons)

## Install

```sh
pip install automatic-code-review-commons
```

## Publish

```sh
rm -rf dist
rm -rf build
rm -rf automatic_code_review_commons.egg-info
pip install setuptools wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*
```