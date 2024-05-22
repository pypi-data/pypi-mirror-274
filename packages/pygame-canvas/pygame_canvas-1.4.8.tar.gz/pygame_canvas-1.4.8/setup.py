from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_desc = fh.read()

setup(
    name='pygame_canvas',
    version='1.4.8',
    packages=find_packages(),
    include_package_data=True,
    description='A library for canvas operations using pygame',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://x.com/gioseaxmc',
    install_requires=[
        'pygame',
    ],
    python_requires='>=3.6',
)
