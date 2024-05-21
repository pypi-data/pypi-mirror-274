from setuptools import setup, find_packages

setup(
    name='newguy103-syncserver',
    version='1.3.0',
    author='NewGuy103',
    author_email='userchouenthusiast@gmail.com',
    description='newguy103-syncserver simplifies file synchronization using Flask-based server and client modules.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'syncserver-server = syncserver.server.__main__:run_simple',
            'syncserver-server.db = syncserver.server._db:run_cli',
            'syncserver-client = syncserver.client.__main__:run_gui'
        ]
    },
    install_requires=[
        'cryptography',
        'requests',
        'flask',
        'argon2-cffi',
        'msgpack',
        'pyqt5'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    include_package_data=True,
    package_data={
        '': ['README.md'],
        'syncserver': ['client/*.py', 'server/*.py'],
    }
)
