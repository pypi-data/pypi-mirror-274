from setuptools import setup, find_namespace_packages

def read_requirements():
    """Reads requirements from requirements.txt file."""
    try:
        with open('requirements.txt', 'r', encoding='utf-8-sig') as f:
            return f.read().splitlines()
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")
        return []

with open('README.md', "r") as f:
    description = f.read()

setup(
    name='mdtopptx',
    version='0.1.0',
    packages=find_namespace_packages(),
    install_requires=read_requirements(),
    description='Converts markdown files to PowerPoint presentations',
    long_description=description,
    long_description_content_type='text/markdown',
)
