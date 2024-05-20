from setuptools import setup

def readme():
  with open('README.md', 'r', encoding="utf8") as f:
    return f.read()

setup(
    name='lptp',
    version='1.0.2',
    author='zoomdev',
    author_email='zoomdeveloper@yandex.ru',
    description='Данный протокол является протоколом RPC вида и служит для вызова процедур на удалённом сервере. Проект является исключительно учебным и не рекомендуется для реального использования.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    package_dir={"": "src"},
    keywords='rpc',
    url="https://github.com/Zoom-Developer/LPTP",
    python_requires='>=3.10'
)