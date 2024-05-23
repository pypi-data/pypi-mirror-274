import setuptools

PACAKGE_NAME = "sql-to-code-local"
package_dir = PACAKGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACAKGE_NAME,  # https://pypi.org/project/sql-to-code-local
    version='0.0.14',  # update each time
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles sql-to-code-local Local Python",
    long_description="PyPI Package for Circles sql-to-code-local Local Python",
    long_description_content_type='text/markdown',
    # TODO: fix the link in the following comment
    url="https://github.com/circ-zone/sql2code-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "mysql-connector>=2.2.9",  # https://pypi.org/project/mysql-connector/
        "python-dotenv>=1.0.0",  # https://pypi.org/project/python-dotenv/
        "logger-local>=0.0.71",  # https://pypi.org/project/logger-local/
        "pytest>=7.4.3",  # https://pypi.org/project/pytest/
        "PyMySQL>=1.1.0",  # https://pypi.org/project/pymysql/
        "database-mysql-local>=0.0.179",  # https://pypi.org/project/database-infrastructure-local/
    ]
)
