from setuptools import setup, find_packages

setup(
    name='e2tapi',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        'protobuf>=3.0.0',
    ],
    include_package_data=True,
    description='SDK for e2t OMS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://gitlab.event2trading.com/utilities/e2tapi.git',
    author='Event2trading',
    author_email='admin@event2trading.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
