# README

> ambedded.ch ambedded-technology-lab python3 library

## basic construct

```bash
my_package/
│
├── module1/
│   ├── __init__.py
│   └── functions1.py
│
├── module2/
│   ├── __init__.py
│   └── functions2.py
│
├── main.py
│
└── setup.py
```

## deploying to PyPI

To deploy your package to PyPI, you'll need to register an account on the PyPI website if you haven't already. Once registered, you can use twine to upload your package.

Edit setup.py (Version,..) and requirements.txt before uploading!

### token auth

> To use this API token:
> Set your username to __token__
> Set your password to the token value, including the pypi- prefix
> For example, if you are using Twine to upload multiple projects to PyPI, > you can set up your $HOME/.pypirc file like this:

```txt
[distutils]
  index-servers =
    pypi

[pypi]
  username = __token__
  password = # either a user-scoped token or a project-scoped token you want to set as the default
```
