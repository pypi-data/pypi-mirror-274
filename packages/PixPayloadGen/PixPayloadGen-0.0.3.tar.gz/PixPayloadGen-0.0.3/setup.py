from setuptools import setup
import codecs

with codecs.open("README.md", "r", "utf-8") as fh:
        readme = fh.read()

setup(name='PixPayloadGen',
    version='0.0.3',
    license='MIT License',
    author='REIZINHODEV',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='edleyteixeira@hotmail.com',
    keywords='pix payload gerar',
    description=u'Gerar Payload pix com QRCODE',
    packages=['PixPayloadGen'],
    install_requires=['crcmod', 'qrcode[pil]'],)