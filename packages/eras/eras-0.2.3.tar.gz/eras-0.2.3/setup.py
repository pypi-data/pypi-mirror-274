from setuptools import setup, find_packages
from setuptools.command.install import install
# from distutils.command.install import install
import subprocess
import os
import sys
#
# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         install.run(self)
#         print('Calling post_install.py')
#         post_install_script = os.path.join(os.path.dirname(__file__), 'eras', 'post_install.py')
#         # subprocess.Popen([sys.executable, post_install_script], shell=True).wait()
#
#         os.system(f'{sys.executable} -i {post_install_script}') # ??? runs during build and works, but fails during install works but the user has to ctrl+d to finish install

        # subprocess.run([sys.executable, post_install_script], check=True) # EOF when reading a line

        # child = pexpect.spawn(f'{sys.executable} {post_install_script}') # error innappropriate ioctl for device
        # child.interact()


# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         install.run(self)
#         print('Calling post_install.py')
#         post_install_script = os.path.join(os.path.dirname(__file__), 'eras', 'post_install.py')
#         # Run the post_install.py script in a new interactive shell
#         subprocess.run([sys.executable, post_install_script], check=True, stdin=sys.stdin, stdout=sys.stdout)

setup(
    name='eras',
    version='0.2.3',
    include_package_data=True,
    packages=find_packages(include=["eras", "eras.*"]),
    package_data={
        '': ['*.txt', '*.rst'],
        'eras': ['*.md'],
    },
    install_requires=[
        'openai==1.26.0',
        'keyboard==0.13.5',
        'python-dotenv==1.0.0',
        'asyncio==3.4.3'
    ],
    entry_points={
        'console_scripts': [
            'eras=eras.main:main',
        ],
    },
    # cmdclass={
    #     'install': PostInstallCommand,
    # },
    # data_files=[('', ['eras/post_install.py'])],
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
