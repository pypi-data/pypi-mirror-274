from setuptools import setup, find_packages

setup(
    name="number_wakeru_photo",  # パッケージ名
    version="0.1.0",  # バージョン
    packages=find_packages(),  # パッケージの自動探索
    install_requires=[],  # 依存関係があればここに記述
    author="haoto_yokota",
    author_email="s2222097@stu.musashino-u.ac.jp",
    description="パッケージの簡単な説明",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yokota26262626/number_wakeru_photo",  # GitHubのリポジトリURL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

