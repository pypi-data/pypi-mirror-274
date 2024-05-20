from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Run the post_install.py script after installation
        subprocess.call([sys.executable, 'src/post_install.py'])

setup(
    name='eras',
    version='0.1.8',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'openai==1.26.0',
        'keyboard==0.13.5',
        'python-dotenv==1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'eras=main:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    author='Jason McAffee',
    author_email='jasonlmcaffee@gmail.com',
    description='A terminal command library that provides a Natural Language Interface for running shell commands.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jasonmcaffee/eras',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
