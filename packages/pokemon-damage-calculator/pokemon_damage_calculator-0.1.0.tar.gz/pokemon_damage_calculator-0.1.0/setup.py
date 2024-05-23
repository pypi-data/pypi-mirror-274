from setuptools import setup, find_packages

setup(
    name='pokemon_damage_calculator',
    version='0.1.0',
    description='A simple Pokémon damage calculator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/siro-rai/damage_calculator.git',  # リポジトリのURL
    author='siro-rai',
    author_email='s2222013@stu.musashino-u.ac.jp',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)
