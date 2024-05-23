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
    'version': '0.1.1',
    'description': 'New Vowel Extraction Suite',
    'long_description': '# new-fave\n\n![PyPI](https://img.shields.io/pypi/v/new-fave.png) [![Python CI](https://github.com/Forced-Alignment-and-Vowel-Extraction/new-fave/actions/workflows/test-and-run.yml/badge.svg)](https://github.com/Forced-Alignment-and-Vowel-Extraction/new-fave/actions/workflows/test-and-run.yml) [![codecov](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/new-fave/graph/badge.svg?token=8JRGOB9NMN)](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/new-fave) [![Maintainability](https://api.codeclimate.com/v1/badges/2f00920067765c0ad77f/maintainability)](https://codeclimate.com/github/Forced-Alignment-and-Vowel-Extraction/new-fave/maintainability) [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\n## What is `new-fave`?\n\n`new-fave` is a tool for automating and optimizing vowel formant extraction. It is philosophically similar (and named after) [the FAVE-suite](https://github.com/JoFrhwld/FAVE). However, `new-fave` has been completely written from scratch, and has some key differences from the FAVE-suite.\n\n1. **`new-fave` does not include a forced-aligner.**\n    It can process alignments produced by fave-align, \n    but we would recommend using the Monteal Forced Aligner instead\n2. **`new-fave` does not require speaker demographics.**\n    You can optionally pass `fave-extract` a speaker\n    demographics file to be merged into your formant data,\n    but this does *not* influence how the data is processed\n    in any way. Besides including file name and speaker\n    number data, you can pass *any* demographic information\n    you would like.\n3. **`new-fave` does not assume North American English vowels**.\n    Your alignments can contain any set of vowels, in\n    any transcription system, as long as you can provide \n    a regular expression to identify them.\n4. **`new-fave` is customizable.**\n    With config files, you can customize vowel recoding,\n    labelset parsing, and point measurement heuristics.\n5. **`new-fave` is focused on formant tracks.**\n    You can still produce single point measurements \n    for vowels, but `new-fave` is built upon \n    the [FastTrack](https://fasttrackiverse.github.io/fasttrackpy/) method. By default, it will write \n    output files including point measurements, full\n    formant tracks, and Discrete Cosine Transform \n    coefficients.\n6. **`new-fave` is maintainable**. As time goes on, and the \n    code base needs updating, the organization and \n    infrastructure of `new-fave` should allow it to be\n    readilly updateable.\n\nYou can read more at [the `new-fave` documentation](https://forced-alignment-and-vowel-extraction.github.io/new-fave/).\n\n## Installation\n\nYou can install `new-fave` with `pip`.\n\n```bash\n# bash\npip install new-fave\n```\n\n## Usage\n\nTo use the default settings (which assume CMU \ndictionary transcriptions), you can use one of these \npatterns.\n\n### A single audio + textgrid pair\n\n```bash\n# bash\nfave-extract audio-textgrid speaker1.wav speaker1.TextGrid\n```\n\n### A directory of audio + textgrid pairs\n\n```bash\n# bash\nfave-extract corpus speakers/\n```\n\n### Multiple subdirectories of audio + textgrid pairs\n\n```bash\n# bash\nfave-extract subcorpora data/*\n```',
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
