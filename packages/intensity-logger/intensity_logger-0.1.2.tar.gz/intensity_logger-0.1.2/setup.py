from setuptools import setup, find_packages

setup(
    name='intensity-logger',
    version='0.1.2',
    author='idkconsole, eagledev1337, homicide3301',
    author_email='idkconsole@proton.me',
    description='A logging utility for Python applications with customizable intensity',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/idkconsole/intensity-logger',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
    keywords='logging logger intensity color logs',
    package_data={},
    include_package_data=True,
    zip_safe=False
)