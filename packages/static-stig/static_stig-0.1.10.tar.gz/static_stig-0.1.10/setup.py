from setuptools import setup

setup(
    name='static-stig',
    version='0.1.10',
    packages=['static_stig'],
    install_requires=[],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'static-stig = static_stig.stig_runner:main'
        ],
    },
)