from setuptools import setup, find_packages

setup(
   name="VeriFact",
   version="0.0.2",
   packages=find_packages(),
   install_requires=[
       #'requests', 'numpy'
      'openai',
      'anthropic',
      'tiktoken',
      'tqdm'
   ],
   author="Yixio Song",
   author_email="yixiaosong@umass.edu",
   description="Pip package for Verifact",
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   url="https://github.com/mungg/VeriScore",
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   python_requires='>=3.6',
)
