import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="klldFN",
    version="2.0.0b1",
    author="klld",
    description="klldFN",
    long_description=long_description,
    python_requires='>=3.8.0',
    long_description_content_type="text/markdown",
    url="https://klldfn.xyz",
    packages=setuptools.find_packages(),
    classifiers=[
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
      ],
    install_requires=[
          'crayons',
          'fortnitepy-edit',
          'FortniteAPIAsync==0.1.6',
          'sanic==20.12.0',
          'requests',
          'rich',
          'aiohttp',
          'asyncio',
          'requests'
      ],
)