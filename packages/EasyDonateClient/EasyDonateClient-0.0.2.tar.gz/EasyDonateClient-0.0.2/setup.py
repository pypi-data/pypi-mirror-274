from io import open
from setuptools import setup

version = '0.0.2'

long_description = '''Простой не официальный модуль для управления вашим магазином на EasyDonate!
Лучший среди всех. Документация: https://tinyteam-1.gitbook.io/python-easydonateclient/'''


setup(
    name='EasyDonateClient',
    version=version,

    author="TheFilik",
    author_email='filikt415@gmail.com',

    description='Неофициальный модуль для EasyDonateApi.',
    long_description=long_description,
    #long_description_content_type='text/markdown'

    packages=['EasyDonateClient'],
)

    

