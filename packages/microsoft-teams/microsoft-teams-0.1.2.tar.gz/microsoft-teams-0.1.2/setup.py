from setuptools import setup, find_packages

setup(
    name='microsoft-teams',
    version='0.1.2',
    packages=['microsoft_teams'],
    install_requires=[
        'requests'
    ],
    author='Rashelle Woudberg',
    author_email='rashelle@al.co.za',
    description='A Python wrapper to send messages to Microsoft Teams.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/microsoft-teams',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)