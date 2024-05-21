from setuptools import setup, find_packages

setup(
    name='video-dev',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'typer',
    ],
    entry_points={
        'console_scripts': [
            'video-dev=cli.main:app',
        ]
    },
    author='video.dev Team',
    author_email='developer@video.dev',
    description='video.dev command-line tool.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='video.dev CLI and Python Client',
    url='https://video.dev',
)
