# # setup.pyの例
# from setuptools import setup, find_packages

# setup(
#     name='commute_agci',
#     version='0.1.1',
#     packages=find_packages(),
#     install_requires=[
#         'numpy',
#         'pandas',
#         'matplotlib',
#         'scipy'
#     ],
#     entry_points={
#         'console_scripts': [
#             'agci=agci:main',
#         ],
#     },
# )
# # Licence: MIT

from setuptools import setup

DESCRIPTION = 'commute_agci is a Python package for analyzing commute data.'
NAME = 'commute_agci'
AUTHOR = 'Udai kishimoto'
AUTHOR_EMAIL = 's2222012@stu.musashino-u.ac.jp'
URL = 'https://github.com/Ryomo0797/AudioAlchemist.git'
LICENSE = 'MIT'
DOWNLOAD_URL = URL
VERSION = '0.4.6'
PYTHON_REQUIRES = '>=3.6'
INSTALL_REQUIRES = [
    'numpy',
    'pandas',
    'matplotlib',
    'scipy'
]
PACKAGES = [
    'commute_agci'
]
KEYWORDS = 'commute_agci commute analysis data visualization'
CLASSIFIERS=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6'
]
with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)