from setuptools import setup, find_packages
import os

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
    version='1.0.14',
    author="spx220",
    author_email="eric2173459@gmail.com",
    long_description_content_type = 'text/markdown',
    packages=find_packages(),
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        #'': ['*.jpg', '*.png', '*.mp3', '*.yml'],
        # And include any *.msg files found in the 'hello' package, too:
        'FirstGame': ['*.jpg', '*.png', '*.mp3', '*.yml', '*.ico'],
    },
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