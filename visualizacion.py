import numpy as np
import matplotlib.pyplot as plt


def calcular_distribucion(
    simulaciones,
    indicador,
    k=None
):

    if indicador == "Ratio de Concentración (CRk)":

        if k is None:
            raise ValueError(
                "Debe especificar k."
            )

        cuotas_ordenadas = np.sort(
            simulaciones,
            axis=1
        )[:, ::-1]

        resultados = (
            cuotas_ordenadas[:, :k]
            .sum(axis=1)
            * 100
        )


    elif indicador == "Índice Herfindahl-Hirschman (IHH)":

        resultados = (
            np.sum(
                simulaciones ** 2,
                axis=1
            )
            * 10000
        )


    elif indicador == "Índice de Dominancia (ID)":

        cuadrados = simulaciones ** 2

        ihh_normalizado = np.sum(
            cuadrados,
            axis=1
        )

        resultados = np.sum(
            (
                cuadrados
                / ihh_normalizado[:, np.newaxis]
            ) ** 2,
            axis=1
        )


    elif indicador == "Índice de Entropía (IE)":

        resultados = -np.sum(
            np.where(
                simulaciones > 0,
                simulaciones
                * np.log(simulaciones),
                0
            ),
            axis=1
        )


    else:

        raise ValueError(
            "Indicador no reconocido."
        )

    return resultados


def graficar_distribucion(
    resultados,
    valor_particular,
    indicador
):

    unidades = {

        "Ratio de Concentración (CRk)":
            "Porcentaje (%)",

        "Índice Herfindahl-Hirschman (IHH)":
            "Puntos IHH",

        "Índice de Dominancia (ID)":
            "Índice (0 a 1)",

        "Índice de Entropía (IE)":
            "Valor de entropía"
    }

    fig, ax = plt.subplots()

    ax.hist(
        resultados,
        bins=30,
        alpha=0.75,
        edgecolor="black"
    )

    ax.axvline(
        valor_particular,
        linestyle="--",
        linewidth=2,
        label=(
            f"Caso particular: "
            f"{valor_particular:.4f}"
        )
    )

    ax.set_title(
        f"Distribución de Monte Carlo - {indicador}"
    )

    ax.set_xlabel(
        f"{indicador} ({unidades[indicador]})"
    )

    ax.set_ylabel(
        "Frecuencia (número de iteraciones)"
    )

    ax.legend()

    return fig