import setuptools
PACKAGE_NAME = "sms-message-inforu-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.4',  # https://pypi.org/project/sms-message-inforu-local/
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles Project SMS",
    long_description="PyPI Package for Circles Project SMS",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[# "api-management-local>=0.0.61",
                      'logger-local>=0.0.135',
                      "message-local>=0.0.123",
                      "database-mysql-local>=0.0.290",
                      "python-sdk-remote>=0.0.93"],
)
