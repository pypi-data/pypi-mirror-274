from setuptools import setup, find_packages

setup(
    name='data_store_connector',
    version='0.1.0',
    description='A brief description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Chandani7250/CONNECTOR',
    author='Chandani Kumari',
    author_email='chandani@chandani.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here.
        # e.g. 'numpy>=1.18.0', 'requests>=2.23.0',
    ],
    python_requires='>=3.6',
)
