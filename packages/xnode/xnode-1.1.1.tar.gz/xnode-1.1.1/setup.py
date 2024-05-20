from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
setup(
    name='xnode',
    version='1.1.1',
    description='This is a CLI management tool for MicroPython-based XNode.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='chanmin.park',
    author_email='devcamp@gmail.com',
    url='https://github.com/planxstudio/xkit',
    install_requires=['click', 'python-dotenv', 'pyserial', 'genlib'],
    packages=find_packages(exclude=[]),
    keywords=['micropython', 'xnode'],
    python_requires='>=3.8',
    package_data={},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'xnode = xnode.xnode:main',    
        ],
    },
)
