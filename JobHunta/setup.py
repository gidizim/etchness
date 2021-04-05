from setuptools import setup

setup(
    name='JobHunta',
    packages=['server'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)


