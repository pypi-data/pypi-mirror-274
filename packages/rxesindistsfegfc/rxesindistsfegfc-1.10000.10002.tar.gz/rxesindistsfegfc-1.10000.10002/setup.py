from setuptools import setup

setup(
    name='rxesindistsfegfc',
    version='1.10000.10002',
    packages=['rxesindistsfegfc'],
    package_data={
        'rxesindistsfegfc': ['*.so']
    },
    python_requires='>=3',
    platforms=["all"]
)

