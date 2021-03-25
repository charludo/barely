import setuptools


setuptools.setup(name='barely',
                 version='0.1',
                 description='barely Development',
                 url='#',
                 author='charlotte',
                 author_email='',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 entry_points={"console_scripts": ["barely = barely.cli:run"]}
                 )
