
from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'MachineFailurePredict'
LONG_DESCRIPTION = 'MachineFailurePredict'

# Setting up
setup(
        name="MachineFailurePredict", 
        version=VERSION,
        author="YHTest",
        author_email="Yihuain163@163.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        package_data={'': ['dataset/data/*.csv']},
        include_package_data=True,
        install_requires=['scikit-learn',
                          'pandas',
                          'seaborn',
                          'numpy'
                          ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'Flex Flow', 'Machine Learning'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows"
        ]
)
