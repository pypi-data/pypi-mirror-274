from setuptools import setup, find_packages

setup(
    name='predict_v2_mk',
    version='0.3',  # Increment the version number
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'tensorflow==2.12.0',
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
