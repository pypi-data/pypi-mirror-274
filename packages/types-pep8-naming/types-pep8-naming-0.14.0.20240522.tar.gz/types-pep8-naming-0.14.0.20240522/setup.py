from setuptools import setup

name = "types-pep8-naming"
description = "Typing stubs for pep8-naming"
long_description = '''
## Typing stubs for pep8-naming

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pep8-naming`](https://github.com/PyCQA/pep8-naming) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pep8-naming`.

This version of `types-pep8-naming` aims to provide accurate annotations
for `pep8-naming==0.14.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pep8-naming. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `489e8dbf41d3350388331b2303bd4f3d13ecbfff` and was tested
with mypy 1.10.0, pyright 1.1.363, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="0.14.0.20240522",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pep8-naming.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pep8ext_naming-stubs'],
      package_data={'pep8ext_naming-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
