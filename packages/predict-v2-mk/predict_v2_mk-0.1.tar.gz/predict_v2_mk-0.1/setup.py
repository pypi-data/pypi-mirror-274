from setuptools import setup, find_packages

setup(
    name='predict_v2_mk',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'tensorflow',
    ],
    entry_points={
        'console_scripts': [
            'predict-neural=predict_v2_mk.predict:main',
        ],
    },
    package_data={
        'predict_v2_mk': ['modelv111.h5', 'new_data1.txt'],
    }
)
