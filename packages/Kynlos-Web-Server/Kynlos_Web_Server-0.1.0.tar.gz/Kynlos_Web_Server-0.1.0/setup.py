from setuptools import setup, find_packages

setup(
    name='Kynlos_Web_Server',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'webserve=kynlos_web_server.main:run_server',
        ],
    },
    package_data={
        'kynlos_web_server': ['htdocs/*', 'config.json'],
    },
    author='Kynlo Akari',
    author_email='kynloakari@gmail.com',
    description='A full-featured web server with PHP support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Kynlos/KynlosWebServer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
