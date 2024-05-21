from setuptools import setup, find_packages

with open("/tmp/projdir.pwd", "r") as f:
    project_path = f.read().strip()

with open(f"{project_path}/README.md", "r") as f:
    long_description = f.read()

with open(f"{project_path}/requirements.txt", "r") as f:
    required_packages = f.read().splitlines()

with open(f"{project_path}/LICENSE", "r") as f:
    license_text = f.read()

setup(
    name="atl",
    version="1.0",
    packages=find_packages(),
    description="ambedded.ch ambedded-technology-lab python3 library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ambedded.ch",
    author_email="info@ambedded.ch",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=required_packages,
    license=license_text,
    url="https://gitlab.com/ambedded-labs/al-pypi-ambedded-atl",
)
