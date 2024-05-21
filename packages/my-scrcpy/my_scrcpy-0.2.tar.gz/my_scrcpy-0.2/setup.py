from setuptools import setup, find_packages

setup(
    name='my_scrcpy',
    version='0.2',
    packages=find_packages(),
    install_requires=[],  # Các package phụ thuộc nếu có
    description='Screen copy android',
    author='NamHV4',
    author_email='namhoang2110@gmail.com',
    url='https://github.com/NamHV4/scrcpy_namhv4',  # URL đến repo của bạn
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)