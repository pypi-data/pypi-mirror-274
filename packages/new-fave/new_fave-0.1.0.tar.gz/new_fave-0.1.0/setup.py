# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['new_fave',
 'new_fave.measurements',
 'new_fave.optimize',
 'new_fave.patterns',
 'new_fave.speaker',
 'new_fave.utils']

package_data = \
{'': ['*'], 'new_fave': ['resources/*']}

install_requires = \
['aligned-textgrid>=0.6.6,<0.7.0',
 'click>=8.1.7,<9.0.0',
 'cloup>=3.0.5,<4.0.0',
 'fasttrackpy>=0.4.5,<0.5.0',
 'fave-measurement-point==0.1.3',
 'fave-recode>=0.3.0,<0.4.0',
 'numpy>=1.26.4,<2.0.0',
 'polars>=0.20.18,<0.21.0',
 'tqdm>=4.66.2,<5.0.0',
 'xlsx2csv>=0.8.2,<0.9.0']

extras_require = \
{':sys_platform != "win32"': ['python-magic>=0.4.27,<0.5.0'],
 ':sys_platform == "win32"': ['python-magic-bin>=0.4.14,<0.5.0']}

entry_points = \
{'console_scripts': ['fave-extract = new_fave.extract:fave_extract']}

setup_kwargs = {
    'name': 'new-fave',
    'version': '0.1.0',
    'description': 'New Vowel Extraction Suite',
    'long_description': '# new-fave\n\n[![Python CI](https://github.com/Forced-Alignment-and-Vowel-Extraction/new-fave/actions/workflows/test-and-run.yml/badge.svg)](https://github.com/Forced-Alignment-and-Vowel-Extraction/new-fave/actions/workflows/test-and-run.yml) [![codecov](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/new-fave/graph/badge.svg?token=8JRGOB9NMN)](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/new-fave)\n',
    'author': 'JoFrhwld',
    'author_email': 'jofrhwld@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.12',
}


setup(**setup_kwargs)
