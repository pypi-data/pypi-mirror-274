from setuptools import setup, find_packages

setup(
    name='quokkaio',
    version='0.1.1',
    description='API wrapper for the Quokka security software',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/smercer-quokka/quokkaio',
    author='Quokka.io',
    author_email='smercer@quokka.io',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'Requests==2.0.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.7',
)