from setuptools import setup, find_packages

setup(
    name='slack-progress',
    version='0.5',
    packages=find_packages(),
    description='A realtime progress bar for Slack',
    author='Bradley Cicenas',
    author_email='bradley@vektor.nyc',
    url='https://github.com/bcicen/slack-progress',
    install_requires=['slacker>=0.9.25'],
    license='http://opensource.org/licenses/MIT',
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ),
    keywords='slack chatops devops',
    extras_require={'test': ['pytest', 'responses', ]}
)
