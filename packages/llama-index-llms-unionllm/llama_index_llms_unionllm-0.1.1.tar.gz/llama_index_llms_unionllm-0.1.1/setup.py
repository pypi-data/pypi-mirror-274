from setuptools import setup, find_packages

setup(
    name='llama-index-llms-unionllm',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'llama-index',
        # 其他依赖项
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A custom LlamaIndex Llms integration for UnionLLM',
    url='https://github.com/yourusername/llama-index-llms-unionllm',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
