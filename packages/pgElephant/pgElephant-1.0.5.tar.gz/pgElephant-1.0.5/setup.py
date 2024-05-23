from setuptools import setup

with open("README.md", "r") as arquivo:
    readme = arquivo.read()

with open("LICENSE", "r") as arquivo:
    licence = arquivo.read()

setup(name='pgElephant',

    version='1.0.5',

    license=licence,

    author='Ryan Souza Anselmo',

    long_description=readme,

    long_description_content_type="text/markdown",

    author_email='ryansouza.cwb@gmail.com',

    keywords='pgElephant',

    description=u'PostgreSQL Database Manager',

    packages=['pgElephant'],

    install_requires=['psycopg2']
)