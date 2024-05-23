# CLABE

[//]: # ([![test]&#40;https://github.com/cuenca-mx/clabe-python/workflows/test/badge.svg&#41;]&#40;https://github.com/cuenca-mx/clabe-python/actions?query=workflow%3Atest&#41;)

[//]: # ([![codecov]&#40;https://codecov.io/gh/cuenca-mx/clabe-python/branch/main/graph/badge.svg&#41;]&#40;https://codecov.io/gh/cuenca-mx/clabe-python&#41;)

[//]: # ([![PyPI]&#40;https://img.shields.io/pypi/v/clabe.svg&#41;]&#40;https://pypi.org/project/clabe/&#41;)

[//]: # ([![Downloads]&#40;https://pepy.tech/badge/clabe&#41;]&#40;https://pepy.tech/project/clabe&#41;)

Librería para validar y calcular un número CLABE basado en
https://es.wikipedia.org/wiki/CLABE

## Requerimientos

Python ^3.11

## Instalación

Se puede instalar desde Pypi usando

```
pip install clabe_pydantic2
```

## Pruebas

Para ejecutar las pruebas

```
$ make test
```

## Uso básico

Obtener el dígito de control de un número CLABE

```python
import clabe_pydantic2
clabe.compute_control_digit('00200000000000000')
```

Para validar si un número CLABE es válido

```python
import clabe_pydantic2
clabe.validate_clabe('002000000000000008')
```

Para obtener el banco a partir de 3 dígitos

```python
import clabe_pydantic2
clabe.get_bank_name('002')
```

Para generar nuevo válido CLABES

```python
import clabe_pydantic2
clabe.generate_new_clabes(10, '002123456')
```
