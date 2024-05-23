from setuptools import setup

setup(
    name="ludoman",
    version="1.0.0",
    description="Some additional libraries for binance trading: custom websocket managing, ploting graphs",
    author="Zakhar Maksymiv",
    author_email="zakhar.maksymiv@gmail.com",
    packages=['ludoman'],     #find_packages(),  # Automatically discover and include all packages
    install_requires=[  # List your library's dependencies here
        "python-binance",
        "matplotlib",
    ]
)
