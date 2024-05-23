import setuptools 

PACKAGE_NAME = "profile-zoominfo-graphql-imp-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/profile-zoominfo-graphql-imp-local
    version='0.0.13',
    author="Circles",
    author_email="info@circlez.ai",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f"{package_dir}/src"},
    package_data={package_dir: ['*.py']},
    long_description="Profile ZoomInfo GraphQL Implementation Local Python Package",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "zoomus>=1.2.1",
        "language-remote>=0.0.20",
        "logger-local>=0.0.135",
        "profile-local>=0.0.64",
        "python-sdk-remote>=0.0.93",
    ]
)
