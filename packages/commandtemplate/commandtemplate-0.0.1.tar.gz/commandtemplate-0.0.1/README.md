# commandtemplate

A python package that provides a command template for easy execution.

Usage:

```python
from commandtemplate.conda import run_template_bash
output_func = lambda **kwargs: [kwargs['o']]

run_template_bash(
    "cp {i} {o}",
    conda_env="some_conda_environment",
    i="input_file",
    o="output_file"
    
)
```

