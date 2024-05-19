from setuptools import setup, find_packages, Command
import subprocess
import sys

class InstallPlaywright(Command):
    def run(self):
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

setup(
    name='plutopdfkit',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'playwright',
    ],
    cmdclass={
        'install_playwright': InstallPlaywright,
    },
    author='Samuel Ugochukwu',
    author_email='sammycageagle@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
