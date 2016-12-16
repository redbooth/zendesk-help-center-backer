#!/usr/bin/env python
import setuptools

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()
    requirements = [x for x in requirements if not x.startswith('#')]

setuptools.setup(   
    name='zendesk-help-center-backer',
    version='0.2',
    description='A Zendesk help center backer written in Python',
    long_description='A Zendesk help center backer written in Python',
    keywords='zendesk,solution,help center,knowledge base',
    author='AeroFS',
    author_email='oss@aerofs.com',
    url='https://github.com/aerofs/zendesk-help-center-backer',
    packages=['zendesk', 'zendesk.scripts'],
    entry_points={
        'console_scripts': [
            'zendesk-new = zendesk.create_new_post_shell:main',
            'zendesk-track = zendesk.track_changes:main',
            'zendesk-deploy = zendesk.deploy:main',
        ]
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
