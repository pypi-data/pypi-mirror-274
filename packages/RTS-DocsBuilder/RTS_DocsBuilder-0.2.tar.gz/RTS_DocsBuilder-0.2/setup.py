from setuptools import setup, find_packages

setup(
    name='RTS_DocsBuilder',
    version='0.2',
    packages=find_packages(),
    description='Create local documentations for your modules. Requires RTS_WebUIBuilder.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='RandomTimeTV',
    author_email='dergepanzerte1@gmail.com',
    license='MIT with required credit to the author.',
    url='https://github.com/RandomTimeLP/RTS_Documentations',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='Work in Progress, Documentations',
    install_requires=["RTS-WebUIBuilder"],
)