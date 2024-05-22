# outputdecorator

***
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/saneksking/outputdecorator)](https://github.com/saneksking/outputdecorator/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/outputdecorator?label=pypi%20downloads)](https://pypi.org/project/outputdecorator/)
![GitHub top language](https://img.shields.io/github/languages/top/saneksking/outputdecorator)
[![PyPI](https://img.shields.io/pypi/v/outputdecorator)](https://pypi.org/project/outputdecorator)
[![GitHub](https://img.shields.io/github/license/saneksking/outputdecorator)](https://github.com/saneksking/outputdecorator/blob/master/LICENSE)
[![PyPI - Format](https://img.shields.io/pypi/format/outputdecorator)](https://pypi.org/project/outputdecorator)
***

## Help:

`pip install outputdecorator`

```python
from output_decorator import StringDecorator

text = StringDecorator.string_decorate(text='Python', symbol='*', print_flag=False)
print(text) # ************************************ Python ***********************************

StringDecorator.string_decorate(text='Python', symbol='*', print_flag=True) 
# Output: ************************************ Python ***********************************

```