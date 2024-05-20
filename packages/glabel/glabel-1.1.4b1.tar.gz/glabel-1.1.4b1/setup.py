# setup.py for g-annotation package

from setuptools import setup, find_packages
# Read the README.md content
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='glabel',  # Name of your package
    version='1.1.4b1',  # Initial version
    author='Gaurang Ingle',  # Your name
    author_email='gaurang.ingle@gmail.com',  # Your email
    description='FastAPI-based image classification app for annotation',  # Short description
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gaurang157/glabel',  # Link to the project (e.g., GitHub)
    packages=find_packages(),  # Finds all packages in your source code
    package_data={'glabel': ['cli.py']},
    include_package_data=True,  # Include additional data files specified in MANIFEST.in
    classifiers=[  # Classifiers to categorize your package
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: FastAPI',
    ],
    keywords='image-classification, annotation, fastapi',  # Keywords for search
    install_requires=[  # Dependencies for your package
        'fastapi>=0.68.0',
        'uvicorn>=0.15.0',
        'python-multipart==0.0.9'
    ],
    entry_points={
        'console_scripts': [
            'glabel=glabel.cli:main2',  # CLI command to launch the app
        ],
    },
    python_requires='>=3.6',  # Minimum Python version required
)
