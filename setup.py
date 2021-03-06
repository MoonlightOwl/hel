import os

from hel.utils import VERSION
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pymongo >= 3.0',
    'rfc3987',
    'semantic_version',
    'waitress'
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    'pytest-capturelog',
    'pytest-pep8'
]

setup(name='hel',
      version=VERSION,
      description='OpenComputers package repository',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          'Development Status :: 1 - Planning',
          'Programming Language :: Python',
          'Framework :: Pyramid',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
          'Topic :: Software Development :: Libraries'
      ],
      author='Totoro',
      author_email='murky.owl@gmail.com',
      license='MIT',
      url='https://api.fomalhaut.me/',
      keywords='repository oc ccru lua',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = hel:main
      """)
