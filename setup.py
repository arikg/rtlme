try
    from setuptools import setup
except ImportError
    from distutils.core import setup

config = {
    'description' 'An rtl parser that helps add RTL (right-to-left) support to web sites',
    'author' 'Arik Galansky',
    'url' 'http://www.arikg.co.il/rtlme',
    'download_url' 'http://www.arikg.co.il/rtlme',
    'author_email' 'arik.galansky@gmail.com',
    'version' '0.1',
    'install_requires' ['nose'],
    'packages' ['rtlparse'],
    'scripts' [],
    'name' 'rtlme'
}

setup(config)