from setuptools import setup, find_packages

setup(
    name="scalegen-function-calling",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        # Add other dependencies here
    ],
    include_package_data=True,
    license="MIT",
    description="A package for generating function calls using OpenAI's API for scalegen function calling model's .",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Tejesh Bhalla",
    author_email="tejeshbhalla1@gmail.com",
    url="https://github.com/ScaleGenAI/function-calling-openai-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
