from setuptools import setup
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('wizata_dsapi/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


setup(
    name='wizata-dsapi',
    version=main_ns['__version__'],
    description='Wizata Data Science Toolkit',
    author='Wizata S.A.',
    author_email='info@wizata.com',
    packages=['wizata_dsapi'],
    install_requires=[
        'requests==2.29.0',
        'dill>=0.3.8',
        'pandas>=2.2.2',
        'numpy>=1.26.4',
        'matplotlib>=3.9.0',
        'protobuf>=3.20.3',
        "tensorflow==2.16.1; sys_platform != 'darwin' or platform_machine != 'arm64'",
        "tensorflow-macos==2.16.1; sys_platform == 'darwin' and platform_machine == 'arm64'",
        "keras==3.3.3; sys_platform != 'darwin' or platform_machine != 'arm64'",
        "keras==3.3.3; sys_platform == 'darwin' and platform_machine == 'arm64'",
        'tensorflow_probability>=0.24.0',
        'scikit-learn>=1.4.2',
        'scipy>=1.13.0',
        'plotly>=5.22.0',
        'adtk>=0.6.2',
        'xgboost>=2.0.3',
        'joblib>=1.4.2',
        'explainerdashboard>=0.4.7',
        'ipywidgets>=8.1.2',
        'kaleido>=0.2.1',
        'pytest>=8.2.1',
        'pytest-cov>=5.0.0',
        'shapely>=2.0.4',
        'pyodbc>=5.1.0',
        'msal>=1.24.0',
        'u8darts>=0.29.0',
        'optuna>=3.6.1',
        'sqlalchemy>=2.0.30'
    ]
)
