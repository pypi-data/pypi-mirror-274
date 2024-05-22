from setuptools import setup, find_packages

setup(
    name='smart_terminal',
    version='0.0.2',
    author='Aditya Kakarla',
    author_email='adityak0523@gmail.com',
    description='The copilot for running terminal commands.',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "copilot = smart_terminal.cli_tool:cli"
        ]
    },
    install_requires=[
        'click',
        'ollama',
        'click_default_group'
    ],
    package_data={'smart_terminal': ['config.json']}
)
