import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(name='barely',
                 version='1.0.1',
                 description='barely is a lightweight, but highly extensible static site generator written in pure python.',
                 long_description=README,
                 long_description_content_type="text/markdown",
                 keywords=['static site generator', 'jinja2', 'markdown', 'web development'],
                 url='https://github.com/charludo/barely',
                 download_url='https://github.com/charludo/barely/archive/v_095.tar.gz',
                 author='Charlotte Hartmann Paludo',
                 author_email='contact@charlotteharludo.com',
                 license='GPL-3.0',
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 zip_safe=False,
                 entry_points={"console_scripts": ["barely = barely.cli:run"]},
                 install_requires=[
                    "click>=8.0.0",
                    "click-default-group>=1.2.2",
                    "coloredlogs>=15.0.0",
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
                 ],
                 classifiers=[
                    'Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers',
                    'Topic :: Text Processing :: Markup :: HTML',
                    'Topic :: Text Processing :: General',
                    'Topic :: Software Development :: Build Tools',
                    'Topic :: Software Development',
                    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 3.9',
                    'Environment :: Console',
                    'Operating System :: OS Independent'
                  ]
                 )
