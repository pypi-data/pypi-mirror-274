# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['frogr', 'frogr.taurex']

package_data = \
{'': ['*'], 'frogr': ['data/*', 'data/chem/*']}

install_requires = \
['astropy>=5.1.1,<6.0.0',
 'ipywidgets>=8.0.4,<9.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'scipy>=1.9.3,<2.0.0',
 'taurex>=3.1.1a0,<4.0.0',
 'twine>=4.0.2,<5.0.0']

entry_points = \
{'console_scripts': ['atmopy = atmopy.__main__:main'],
 'taurex.plugins': ['atmo = atmopy.taurex']}

setup_kwargs = {
    'name': 'frogr',
    'version': '0.0.0',
    'description': 'ATMOpy',
    'long_description': '# frogr: from gas to retrieval\n\n[![PyPI](https://img.shields.io/pypi/v/atmopy.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/atmopy.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/atmopy)][python version]\n[![License](https://img.shields.io/pypi/l/atmopy)][license]\n\n[![Read the documentation at https://frogr-from-gas-to-retrieval.readthedocs.io/](https://img.shields.io/readthedocs/atmopy/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/mfbieger/atmopy/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/mfbieger/atmopy/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/frogr/\n[status]: https://pypi.org/project/frogr/\n[python version]: https://pypi.org/project/frogr\n[read the docs]: https://frogr-from-gas-to-retrieval.readthedocs.io/\n[tests]: https://github.com/michellebieger/frogr/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/michellebieger/frogr\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- Use the ATMO equilibrium chemistry plugin in your TauREx 3.1 forward models and retrievals.\n\n## Requirements\n\n- Ensure that you have a working installation of ATMO on your machine (https://www.gitlab.erc-atmo.eu/1-2d_tools/atmo). If you need access to ATMO, please contact Pascal Tremblin: pascal.tremblin@cea.fr\n- You will need a working installation of TauREx 3.1 on your machine, with associated required Python packages: https://taurex3-public.readthedocs.io/\n\n## Installation\n\n<!-- You can install _frogr_ via [pip] from [PyPI]:\n\n```console\n$ pip install frogr\n```\n\nAlternatively, clone this Github and install via terminal with. This is done by: -->\n\nYou can install _frogr_ by cloning this Github and installing via the terminal. This is done by:\n\nCloning the directory using:\n\n```console\n$ git clone https://github.com/michellebieger/frogr.git\n```\n\nMove into frogr\'s folder:\n\n```console\n$ cd frogr\n```\n\nInstall by then typing in:\n\n```console\n$ pip install .\n```\n\nIf you are unable to install, a common error for HPC systems can be the Poetry log install requirements, which dictate a high-level version of Python. Try creating a new conda environment and then try pip installing once more:\n\n```console\n$ conda create -n [insertpreferredenvname] python=3.8\n```\n\nYou can check the installation by importing frogr into Python:\n\n```console\n$ python -c "import atmopy"\n```\n\nTo check that TauREx 3.1 has correctly registered your plugin:\n\n```console\n$ taurex --plugins\n```\n\nIf there are no errors, you have been successful!\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## License\n\nDistributed under the terms of the [GPL 3.0 license][license],\n_frogr_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems, please email michellebieger@live.com with a detailed description of the issue.\n\n<!-- please [file an issue] along with a detailed description. -->\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n\n<!-- [file an issue]: https://github.com/mfbieger/frogr/issues -->\n\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/michellebieger/frogr/blob/main/LICENSE\n[contributor guide]: https://github.com/michellebieger/frogr/blob/main/CONTRIBUTING.md\n[command-line reference]: https://frogr-from-gas-to-retrieval.readthedocs.io/en/latest/usage.html\n',
    'author': 'M. F. Bieger',
    'author_email': 'mb987@exeter.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mfbieger/atmopy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
