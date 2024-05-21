
from pathlib import Path

import setuptools


def parse_requirements(requirements: str):
    with open(requirements) as f:
        return [
            l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')
        ]


setuptools.setup(
    name='dashtable2',
    packages=[
        'dashtable',
        'dashtable.dashutils',
        'dashtable.data2md',
        'dashtable.data2rst',
        'dashtable.data2simplerst',
        'dashtable.grid2data',
        'dashtable.html2data',
        'dashtable.simple2data',
        'dashtable.data2rst.cell',
        'dashtable.html2data.restructify',
        'dashtable.html2data.restructify.converters'
    ],
    version=Path('version.txt').read_text(encoding='utf-8').strip(),

    description='A library for converting a HTML tables into ASCII tables, rowspan and colspan allowed!',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    author='doakey3 & gustavklopp & pasaopasen',
    author_email='qtckpuhdsa@gmail.com',
    url='https://github.com/PasaOpasen/dashtable2',
    license='MIT',
    keywords=[
        'text table', 'conversion', 'documentation'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires=parse_requirements('./requirements.txt'),

)
