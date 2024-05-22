
from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'picSearch'
LONG_DESCRIPTION = 'picSearch'

# Setting up
setup(
        name="picSearch", 
        version=VERSION,
        author="YHTest",
        author_email="yihua.wang@flex.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        include_package_data=True,
        install_requires=['numpy',
                           'requests',
                           'io',
                           'PIL',
                           'os',
                           'gradio',
			   'minio'
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