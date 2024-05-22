from setuptools import setup, find_packages

setup(
    name='krutrimpy',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    author='Umraz Khan',
    author_email='kumraz858@gmail.com',
    description='An unofficial wrapper for Krutrim',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Assassinumz/krutrimpy",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.10',
    keywords=['ola', 'krutrim', 'olakrutrim', 'krutrim wrapper'],
)
