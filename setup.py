from setuptools import find_packages, setup
setup(
    name='mcqgenerator',
    version='0.0.1',
    author='anuragsinghaakash',
    author_email="anuragsinghaakash@gmail.com",
    install_requires=["openai", "langchain","streamlet",'python-dotenv','PyPDF2'],
    packages=find_packages()
)