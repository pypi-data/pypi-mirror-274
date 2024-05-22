from setuptools import setup, find_packages

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="typing_test_sdd",
    version="1.0.2",
    author="Gaurav Surve",
    url="https://github.com/GauravS2507/Gaurav-Surve-SDD2-Project---Typing-Test",
    description="TKinter GUI Typing Test - Gaurav Surve 122SDD2",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    platforms="any",
    include_package_data=True,
    install_requires=[
        "customtkinter",
        "pillow",
    ],
    entry_points={
        "gui_scripts": [
            "typing-ctk = typing_test_sdd:start_app"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Games/Entertainment"
    ]
)