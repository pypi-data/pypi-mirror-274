from setuptools import setup, find_packages

setup(
    name='discord_invite',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'tls-client',
    ],
    author='Lacia Hax',
    author_email='yuitanmiruku@outlook.jp',
    description='A python of discord joiner',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LaciaHax/discord_joiner',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
