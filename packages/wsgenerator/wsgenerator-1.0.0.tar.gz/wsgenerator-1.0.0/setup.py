from setuptools import setup

ext_modules = None
with open('README.md', mode='r', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='wsgenerator',
    version='1.0.0',
    description='Module for generating word search puzzles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pgolo/wsgenerator',
    author='Pavel Golovatenko-Abramov',
    author_email='p.golovatenko@gmail.com',
    packages=['wsgenerator'],
    ext_modules=ext_modules,
    include_package_data=True,
    license='MIT',
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
