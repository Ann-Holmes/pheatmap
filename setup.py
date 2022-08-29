from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pheatmap",  # Required
    version="0.1.0.dev2",  # Required
    description="pheatmap for Python",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/Ann-Holmes/pheatmap",  # Optional
    author="Zongliang Hou",  # Optional
    author_email="zonglianghou@163.com",  # Optional
    classifiers=[  # Optional
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: POSIX :: Linux"
    ],
    keywords="heatmap, gene, expression, visualization",  # Optional
    package_dir={"": "src"},  # Optional
    packages=find_packages(where="src", exclude=["tests"]),  # Required
    python_requires=">=3.8, <4",
    install_requires=["numpy", "matplotlib", "pandas"],  # Optional
    extras_require={  # Optional
        "dev": ["sphinx", "myst-parser"]
    },
    project_urls={  # Optional
        # "Documents": "",
        "Bug Reports": "https://github.com/Ann-Holmes/pheatmap/issues",
        "Source": "https://github.com/Ann-Holmes/pheatmap",
    },
)
