from setuptools import setup, find_namespace_packages

setup(
    name='lottery_console',
    version='1.0.0',
    description='very helpful lottery',
    url='https://github.com/VadimTrubay/lottery_console',
    author='TrubayVadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['colorama'],
    entry_points={'console_scripts': ['lottery_console=lottery_console.main:main']}
)