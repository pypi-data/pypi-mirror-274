from setuptools import setup, find_packages

setup(
    name='textsegmt',
    version='0.1.0',
    author='LugandaOCR',
    author_email='beijukab@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'opencv-python>=4.0',
        'tensorflow==2.14.0',
    ],
    python_requires='>=3.6',
    description='Text Segmentation Package',
    license='MIT',
    package_data={
        'imgproc': ['cpp/*.cpp', 'cpp/*.hpp'],
        '': ['main.py'],  
    },
)

