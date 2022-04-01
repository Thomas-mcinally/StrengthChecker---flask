from setuptools import setup, find_packages

requires = [
    'click==8.1.2'
    ,'colorama==0.4.4'
    ,'Flask==2.1.1'
    ,'itsdangerous==2.1.2'
    ,'Jinja2==3.1.1'
    ,'MarkupSafe==2.1.1'
    ,'numpy==1.22.3'
    ,'pandas==1.4.1'
    ,'python-dateutil==2.8.2'
    ,'pytz==2022.1'
    ,'six==1.16.0'
    ,'Werkzeug==2.1.0'
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