from setuptools import setup, find_packages

setup(
    name='xspace-dl',
    version='0.2.26',
    author='Your Name',
    author_email='your.email@example.com',
    description='A python module to download Twitter spaces',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rosebabaganoush/xspace-dl',
    packages=find_packages(),
    install_requires=[
        'requests',
        'mutagen',
    ],
    entry_points={
        'console_scripts': [
            'xspace-dl=xspace.main:main',  # Ensure this matches your main entry point
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
