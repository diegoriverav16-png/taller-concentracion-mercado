import numpy as np


def simulacion_monte_carlo(
    numero_empresas,
    iteraciones=1000
):

    if not isinstance(numero_empresas, int):
        raise TypeError(
            "El número de empresas debe ser entero."
        )

    if numero_empresas < 2 or numero_empresas > 100:
        raise ValueError(
            "El número de empresas debe estar entre 2 y 100."
        )

    if not isinstance(iteraciones, int):
        raise TypeError(
            "El número de iteraciones debe ser entero."
        )

    if iteraciones < 1:
        raise ValueError(
            "Las iteraciones deben ser mayores que cero."
        )

    valores = np.random.random(
        (
            iteraciones,
            numero_empresas
        )
    )

    cuotas = valores / valores.sum(
        axis=1,
        keepdims=True
    )

    cuotas[:, -1] = (
        1.0
        - cuotas[:, :-1].sum(axis=1)
    )

    return cuotas