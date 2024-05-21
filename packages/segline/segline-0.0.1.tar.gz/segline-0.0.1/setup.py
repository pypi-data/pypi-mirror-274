from setuptools import setup, find_packages

setup(
    name='segline',
    version='0.0.1',
    author='LugandaOCR',
    author_email='beijukab@gmail.com',
    description='Package for line segmentation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python-headless', 
    ],
    package_data={'segline': ['image_processor/*']},
    include_package_data=True,
    license='MIT',
)

