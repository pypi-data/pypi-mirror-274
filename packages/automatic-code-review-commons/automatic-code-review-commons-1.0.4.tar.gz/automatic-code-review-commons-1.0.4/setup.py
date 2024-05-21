from setuptools import setup, find_packages

setup(
    name='automatic-code-review-commons',
    version='1.0.4',
    packages=find_packages(),
    description='Biblioteca com funções genéricas para revisões automáticas de código do projeto ACR',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kielson Zinn da Silva',
    author_email='automatic.code.review@gmail.com',
    url='https://github.com/automatic-code-review/automatic-code-review-commons',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
