from setuptools import setup, find_packages

setup(
    name="OrientationLandscape",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "mpi4py"
    ],
    entry_points={
        'console_scripts': [
            'orientation_analysis=OrientationLandscape.OrientationAnalysis:main',
            'landscape_projection=OrientationLandscape.LandscapeProjection:main',
            'point_select=OrientationLandscape.PointSelect:main',
            'particle_backtrack=OrientationLandscape.ParticleBacktrack:main'
        ]
    },
    author="Chengmin Li",
    author_email="chengmin.li@ucsf.edu",
    description="A suite of tools to analyze and visualize orientation landscapes.",
    url="https://github.com/yifancheng-ucsf/OrientationLandscape",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)

