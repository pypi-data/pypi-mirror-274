from setuptools import setup, find_packages

setup(
    name="poyrazgtanima",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "matplotlib"
    ],
    author="Alperen Özer",
    author_email="alprnozr14@gmail.com",
    description="MHGFL Poyraz IHA Takımının hususi görüntü tanıma kütüphanesidir. İzinsiz kullanım kabul edilemez",
    url="https://github.com/kullaniciadi/my_library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)