from setuptools import setup

setup(
    name='us_vis',

    version='1.0',

    description='Visualisation tools for umbrella sampling calculations',

    long_description = 'This is a series of script that allow to visualize and modify graphs obtained through umbrella sampling calculations from AMBER (https://ambermd.org/index.php) and WHAM (http://membrane.urmc.rochester.edu/?page_id=126) software. For full documentation see: https://us-vis.readthedocs.io/en/latest/', 

    packages=['us_vis'],

    install_requires=["pandas", "matplotlib"],

    setup_requires=["pandas", "matplotlib"],

    extras_require={
        'docs': [
            'sphinx'
        ],
        'dev': [
            'pytest',
        ],
    },

    zip_safe=False
)
