"""
setup script
"""
from setuptools import setup,find_packages
import waterdata

config = {
    'description': (
        'Python interface for accessing usgs water data via various web '
        'services and simulated web services'
    ),
    'author': 'Rawser Spicer',
    'url': waterdata.__url__,
    'download_url': waterdata.__url__,
    'author_email': 'rwspicer@alaska.edu',
    'version': waterdata.__version__,
    'install_requires': [
        'pandas',
        'pyyaml', 
        'validators',
        'BeautifulSoup4',
        'requests',
        'pyproj',
        'geojson',
        'numpy'
    ],
    'packages': find_packages(),
    'scripts': [],
    'package_data': {},
    'name': 'waterdata'
}

setup(**config)
