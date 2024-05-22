from setuptools import setup, find_packages

setup(
    name='xssbase',
    version='1.0.0',
    author='Fidal',
    maintainer='Fidal',
    maintainer_email='mrfidal@proton.me',
    description='A professional tool for scanning XSS vulnerabilities.',
    url='https://mrfidal.in/cyber-security/xssbase',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'xssbase = xssbase.cli:main',
        ],
    },
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    keywords=['XSS', 'cross-site scripting', 'security', 'vulnerability', 'scanner'],
    long_description='XSSBase is a professional tool for scanning websites for Cross-Site Scripting (XSS) vulnerabilities. For more information, visit https://mrfidal.in/cyber-security/xssbase',
    long_description_content_type='text/plain',
    license='MIT',
)
