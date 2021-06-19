import setuptools


setuptools.setup(name='barely',
                 version='1.0.0',
                 description='barely is a lightweight, but highly extensible static site generator written in pure python.',
                 url='https://github.com/charludo/barely',
                 author='Charlotte Hartmann Paludo',
                 author_email='contact@charlotteharludo.com',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 entry_points={"console_scripts": ["barely = barely.cli:run"]},
                 install_requires=[
                    "click>=8.0.0",
                    "mock>=4.0.0",
                    "pyyaml>=5.3.0",
                    "watchdog>=2.0.0",
                    "pillow>=8.0.0",
                    "GitPython>=3.0.0",
                    "pygments>=2.5.0",
                    "libsass>=0.21.0",
                    "pysftp>=0.2.5",
                    "livereload>=2.5.0",
                    "binaryornot>=0.4.0",
                    "jinja2>=3.0.0",
                    "mistune==2.0.0rc1",
                    "calmjs>=3.3.0"
                 ]
                 )
