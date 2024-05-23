from setuptools import setup, find_packages

setup(
    name='code-diff-review',
    version='1.2.0',
    author='Agustin Rios',
    author_email='arios6@uc.cl',
    description='Review your code diff.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=open("./requirements.txt").read().splitlines(),
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'code-diff-review=src.script:main',
        ],
    },
    classifiers=[
        # 'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)