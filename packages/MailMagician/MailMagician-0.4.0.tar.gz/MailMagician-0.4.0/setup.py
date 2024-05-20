from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [] 
setup(
    name="MailMagician",
    version="0.4.0",
    author="Tao Xiang",
    author_email="tao.xiang@tum.de",
    description="A package of email robots",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/MailBot",
    packages=find_packages(),
    # py_modules=['timedd']
    install_requires=requirements,
    classifiers=[
  "Programming Language :: Python :: 3.8",
  "License :: OSI Approved :: MIT License",
    ],
)
