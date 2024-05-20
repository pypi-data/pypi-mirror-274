from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="minaibot",
    version="0.1.2",
    description="BotFramework",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Nikita Minai",
    author_email="nikita.minai@ya.ru",
    url="https://github.com/nikita-minai/minaibot",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "pyTelegramBotAPI",
        "telebot",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'minaibot_setup=post_install:create_directories_and_files',
        ],
    },
)
