from setuptools import setup

setup(
    name='mmk_updater',
    version='0.12.1',
    packages=['mmk_updater'],
    url='https://github.com/melianmiko/python-updater',
    license='Apache 2.0',
    install_requires=[],
    extras_require={
        "tk": ["tkinter"]
    },
    author='MelianMiko',
    author_email='melianmiko@yandex.ru',
    description='Updater tool',
    include_package_data=True
)
