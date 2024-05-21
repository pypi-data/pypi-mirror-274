from setuptools import setup, find_packages

setup(
    name='xspace-dl',  # Updated package name
    version='0.1.24',  # Increment the version number
    author='RoseBabaGanoush',
    author_email='hello@rosebabaganoush.com',
    description='A python module to download Twitter spaces',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RoseBabaganoush/xspace-dl',  # Update with your repository URL
    packages=find_packages(),
    install_requires=[
        'requests',
        'mutagen',  # Add mutagen to dependencies
    ],
    entry_points={
        'console_scripts': [
            'xspace-dl=xspace.main:main',  # Adjust as per your CLI entry point
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
