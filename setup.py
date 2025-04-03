from setuptools import setup, find_packages

setup(
    name='stackem',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openai>=1.0.0',
        'pandas>=1.5.0',
    ],
    entry_points={
        'console_scripts': [
            'stackem=stackem.analyze:main',
        ],
    },
    author='Behron Georgantas',
    description='Unreal Engine trace analyzer using OpenAI GPT-4. Requires tkinter for GUI support.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bresume/stackem',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)