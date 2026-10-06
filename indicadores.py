import math
from numbers import Real


def _validar_y_normalizar(cuotas):

    if not isinstance(cuotas, list):
        raise TypeError(
            "Las cuotas deben ingresarse en una lista."
        )

    if len(cuotas) == 0:
        raise ValueError(
            "La lista de cuotas no puede estar vacía."
        )

    for cuota in cuotas:

        if isinstance(cuota, bool) or not isinstance(cuota, Real):
            raise TypeError(
                "Cada cuota debe ser un valor numérico."
            )

        if not math.isfinite(cuota):
            raise ValueError(
                "Las cuotas deben ser valores finitos."
            )

        if cuota < 0 or cuota > 100:
            raise ValueError(
                "Cada cuota debe estar entre 0 y 100."
            )

    total = sum(cuotas)

    if all(cuota <= 1 for cuota in cuotas):

        if math.isclose(total, 1.0, abs_tol=1e-6):

            cuotas_normalizadas = [
                float(cuota)
                for cuota in cuotas
            ]

        elif math.isclose(total, 100.0, abs_tol=1e-6):

            cuotas_normalizadas = [
                cuota / 100
                for cuota in cuotas
            ]

        else:

            raise ValueError(
                "Las cuotas deben sumar 1 o 100."
            )

    else:

        if not math.isclose(total, 100.0, abs_tol=1e-6):

            raise ValueError(
                "Las cuotas porcentuales deben sumar 100."
            )

        cuotas_normalizadas = [
            cuota / 100
            for cuota in cuotas
        ]

    return cuotas_normalizadas


def crk(cuotas, k):

    cuotas = _validar_y_normalizar(cuotas)

    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k debe ser un número entero.")

    if k < 1 or k > len(cuotas):
        raise ValueError(
            "k debe estar entre 1 y el número de empresas."
        )

    cuotas_ordenadas = sorted(
        cuotas,
        reverse=True
    )

    return sum(cuotas_ordenadas[:k]) * 100


def ihh(cuotas):

    cuotas = _validar_y_normalizar(cuotas)

    resultado = sum(
        cuota ** 2
        for cuota in cuotas
    )

    return resultado * 10000


def indice_dominancia(cuotas):

    cuotas = _validar_y_normalizar(cuotas)

    ihh_normalizado = sum(
        cuota ** 2
        for cuota in cuotas
    )

    resultado = sum(
        (cuota ** 2 / ihh_normalizado) ** 2
        for cuota in cuotas
    )

    return resultado


def indice_entropia(cuotas):

    cuotas = _validar_y_normalizar(cuotas)

    entropia = 0

    for cuota in cuotas:

        if cuota > 0:

            entropia -= cuota * math.log(cuota)

    return entropia