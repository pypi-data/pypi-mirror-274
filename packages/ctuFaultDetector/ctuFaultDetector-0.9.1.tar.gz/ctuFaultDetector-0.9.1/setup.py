from setuptools import setup, find_packages


setup(
    name="ctuFaultDetector",
    version="0.9.1",
    author="Ales Trna",
    author_email="altrna@fel.cvut.cz",
    description="Anomaly detection in time series model",
    long_description="Contains only the feature and deviation classifiers to make the package more lightweight",
    packages=find_packages(),
    url="https://github.com/altrna/Anomaly-detection-in-timeseries",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'scikit_learn',
        'scipy',
        'tslearn',
    ],
)
