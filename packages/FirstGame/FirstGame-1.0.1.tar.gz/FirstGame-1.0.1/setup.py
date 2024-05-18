from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

# 列出資源文件，如圖片、音頻等
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths


extra_files = package_files('FirstGame/resources')


setup(
    name='FirstGame',
    version='1.0.1',
    author="spx220",
    author_email="eric2173459@gmail.com",
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    packages=find_packages(),
    package_data={'': extra_files},
    license='MIT',
    zip_safe=False,
    keywords=['spx', 'kpop', 'anime', 'FirstGame'],
    install_requires=[
        'pygame==2.5.2',
        'pymysql==1.1.0',
        'pillow==10.2.0',
        'pyyaml==6.0.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'FirstGame=FirstGame.main:main',
        ],
    },
)