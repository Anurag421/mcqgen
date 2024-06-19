from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='anuragsinghaakash',
    author_email="anuragsinghaakash@gmail.com",
    install_requires=["openai",
                      "langchain",
                      "streamlit",
                      "python-dotenv",
                      "PyPDF2",
                      "langchain_community"],
    packages=find_packages()
)
