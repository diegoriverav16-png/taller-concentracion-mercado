import math
import numpy as np


def calcular_percentil(
    distribucion,
    valor_particular
):

    distribucion = np.asarray(
        distribucion,
        dtype=float
    )

    percentil = (
        np.sum(
            distribucion <= valor_particular
        )
        / distribucion.size
    ) * 100

    return float(percentil)


def _clasificar_normalizado(valor):

    valor = np.clip(
        valor,
        0,
        1
    )

    if valor < 1 / 3:
        return "Baja"

    elif valor < 2 / 3:
        return "Moderada"

    else:
        return "Alta"


def clasificar_concentracion(
    indicador,
    valor,
    numero_empresas,
    k=None
):

    if indicador == "Ratio de Concentración (CRk)":

        if k is None:
            raise ValueError(
                "Debe indicar k."
            )

        if k == 4:

            if valor < 40:
                nivel = "Baja"

            elif valor <= 60:
                nivel = "Moderada"

            else:
                nivel = "Alta"

            criterio = (
                "Para CR4 se considera concentración "
                "baja bajo 40%, moderada entre 40% y "
                "60%, y alta sobre 60%."
            )

        else:

            if k == numero_empresas:

                return None, (
                    f"CR{k} incluye todas las empresas "
                    "y siempre alcanza 100%, por lo que "
                    "no permite clasificar concentración."
                )

            minimo_teorico = (
                100 * k / numero_empresas
            )

            concentracion_normalizada = (
                (valor - minimo_teorico)
                / (100 - minimo_teorico)
            )

            nivel = _clasificar_normalizado(
                concentracion_normalizada
            )

            criterio = (
                f"CR{k} fue normalizado entre su "
                f"mínimo teórico "
                f"({minimo_teorico:.2f}%) "
                "y su máximo de 100%."
            )


    elif indicador == "Índice Herfindahl-Hirschman (IHH)":

        if valor < 1000:
            nivel = "Baja"

        elif valor <= 1800:
            nivel = "Moderada"

        else:
            nivel = "Alta"

        criterio = (
            "Para IHH se considera concentración baja "
            "bajo 1.000 puntos, moderada entre 1.000 "
            "y 1.800 y alta sobre 1.800."
        )


    elif indicador == "Índice de Dominancia (ID)":

        minimo_teorico = (
            1 / numero_empresas
        )

        concentracion_normalizada = (
            (valor - minimo_teorico)
            / (1 - minimo_teorico)
        )

        nivel = _clasificar_normalizado(
            concentracion_normalizada
        )

        criterio = (
            "El Índice de Dominancia se compara entre "
            "la situación de cuotas iguales y la "
            "dominancia máxima."
        )


    elif indicador == "Índice de Entropía (IE)":

        entropia_maxima = math.log(
            numero_empresas
        )

        concentracion_normalizada = (
            1 - valor / entropia_maxima
        )

        nivel = _clasificar_normalizado(
            concentracion_normalizada
        )

        criterio = (
            "Una menor entropía representa una mayor "
            "concentración del mercado."
        )


    else:

        raise ValueError(
            "Indicador no reconocido."
        )

    return nivel, criterio


def evaluar_respuesta(
    indicador,
    valor_particular,
    distribucion,
    respuesta_usuario,
    numero_empresas,
    k=None
):

    nivel_correcto, criterio = (
        clasificar_concentracion(
            indicador,
            valor_particular,
            numero_empresas,
            k
        )
    )

    percentil = calcular_percentil(
        distribucion,
        valor_particular
    )

    correcta = (
        respuesta_usuario
        == nivel_correcto
    )

    if indicador == "Índice de Entropía (IE)":

        interpretacion = (
            f"El caso está en el percentil "
            f"{percentil:.2f}. "
            "En entropía, un valor mayor representa "
            "menor concentración."
        )

    else:

        interpretacion = (
            f"El caso está en el percentil "
            f"{percentil:.2f}. Esto significa que "
            f"su indicador es igual o superior al de "
            f"aproximadamente {percentil:.2f}% de "
            "los mercados simulados."
        )

    return {

        "correcta": correcta,
        "nivel": nivel_correcto,
        "percentil": percentil,
        "criterio": criterio,
        "interpretacion": interpretacion
    }