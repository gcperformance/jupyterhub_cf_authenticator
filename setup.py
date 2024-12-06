from setuptools import setup, find_packages

setup(
    name='cf_authenticator',
    version='0.1.0',
    description='Cloudflare Zero Trust Authenticator for JupyterHub',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gcperformance/cf_authenticator',
    license='Apache 2.0',
    author='Kyle Fletcher',
    author_email='kyle.fletcher@tbs-sct.gc.ca',
    packages=find_packages(),
    install_requires=[
        'jupyterhub>=2.0.0',
        'pyjwt[crypto]>=2.0.0',
        'urllib3>=2.0.0'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
    keywords='jupyterhub authenticator cloudflare zerotrust',
)
