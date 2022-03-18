from setuptools import setup, find_packages

requires = [
    'flask',
    'pandas',
]

setup(
    name='StrengthChecker',
    version='1.0',
    description='An application that allows you to compare your SBD strength to IPF contestants',
    author='Thomas Mcinally',
    author_email='thomasmcinally@hotmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)