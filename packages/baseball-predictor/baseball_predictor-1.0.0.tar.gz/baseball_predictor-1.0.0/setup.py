from setuptools import setup, find_packages

setup(
    name='baseball_predictor',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'streamlit'
    ],
    entry_points={
        'console_scripts': [
            'baseball_predictor = baseball_predictor.app:main'
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
