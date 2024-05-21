from setuptools import setup, find_packages

setup(
    name='testspace_annotations',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/yourusername/your-plugin-name',
    license='MIT',
    author='Marcin Augustynów',
    author_email='marcin.augustynow@gmail.com',
    description='Plugin making it easy to add annotations to your testspace test output',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pytest',
    ],
    entry_points={
        'pytest11': [
            'testspace_annotations = testspace_annotations',
        ],
    },
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
