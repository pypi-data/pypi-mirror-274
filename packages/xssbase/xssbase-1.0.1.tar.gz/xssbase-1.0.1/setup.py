from setuptools import setup, find_packages

setup(
    name='xssbase',
    version='1.0.1',
    description='A professional tool for scanning XSS vulnerabilities.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://mrfidal.in/cyber-security/xssbase',
    author='Fidal',
    author_email='mrfidal@proton.me',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Security',
    ],
    keywords='xssbase, xss, vulnerability, scanning, mrfidal',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'xssbase=xssbase.cli:main',
        ],
    },
)
