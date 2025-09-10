from setuptools import setup, find_packages
import os

# Attempt to load long description from README.md if available
long_description = ""
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
except Exception:
    long_description = "pip_name_generator: Deterministic and LLM-assisted PyPI package name generator."

setup(
    name="pip_name_generator",
    version="2025.9.101449",
    author="Eugene Evstafev",
    author_email="hi@eugene.plus",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chigwell/pip_name_generator",
    packages=find_packages(),
    install_requires=["requests>=2.20.0", "langchain_llm7", "llmatch_messages", "langchain_core"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
    tests_require=["unittest"],
    test_suite="test",
)