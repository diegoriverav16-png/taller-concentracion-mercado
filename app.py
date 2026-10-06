import streamlit as st
import numpy as np

# =========================================================
# IMPORTAR LOS MÓDULOS DEL PROYECTO
# =========================================================

from indicadores import (
    crk,
    ihh,
    indice_dominancia,
    indice_entropia
)

from simulacion import simulacion_monte_carlo

from visualizacion import (
    calcular_distribucion,
    graficar_distribucion
)

from evaluador import (
    clasificar_concentracion,
    evaluar_respuesta
)


# =========================================================
# CONFIGURACIÓN GENERAL DE STREAMLIT
# =========================================================

st.set_page_config(
    page_title="Simulador de Concentración de Mercado",
    layout="wide"
)

st.title("Simulador de Concentración de Mercado")

st.write(
    "Aplicación interactiva para analizar indicadores de "
    "concentración mediante simulaciones de Monte Carlo."
)


# =========================================================
# 1. SELECCIÓN DE INDICADORES
# =========================================================

st.subheader("1. Indicadores de concentración")

indicadores_seleccionados = st.multiselect(
    "Seleccione uno o más indicadores:",
    options=[
        "Ratio de Concentración (CRk)",
        "Índice Herfindahl-Hirschman (IHH)",
        "Índice de Dominancia (ID)",
        "Índice de Entropía (IE)"
    ]
)

if not indicadores_seleccionados:
    st.warning(
        "Debe seleccionar al menos un indicador."
    )


# =========================================================
# 2. NÚMERO DE EMPRESAS
# =========================================================

st.subheader("2. Número de empresas")

numero_empresas = st.number_input(
    "Número de empresas (N):",
    min_value=2,
    max_value=100,
    value=5,
    step=1
)

numero_empresas = int(numero_empresas)


# =========================================================
# 3. CASO PARTICULAR DE CUOTAS
# =========================================================

st.subheader("3. Caso particular de cuotas de mercado")

modo_cuotas = st.radio(
    "Seleccione cómo desea ingresar las cuotas:",
    options=[
        "Entrada manual",
        "Generación aleatoria"
    ]
)

cuotas_particulares = None


# ---------------------------------------------------------
# ENTRADA MANUAL
# ---------------------------------------------------------

if modo_cuotas == "Entrada manual":

    texto_cuotas = st.text_input(
        "Ingrese las cuotas separadas por comas:",
        placeholder="Ejemplo: 40, 30, 20, 10"
    )

    if texto_cuotas:

        try:

            cuotas_particulares = [
                float(valor.strip())
                for valor in texto_cuotas.split(",")
            ]

            if len(cuotas_particulares) != numero_empresas:

                st.error(
                    f"Debe ingresar exactamente "
                    f"{numero_empresas} cuotas."
                )

                cuotas_particulares = None

        except ValueError:

            st.error(
                "Las cuotas deben contener únicamente "
                "valores numéricos."
            )

            cuotas_particulares = None


# ---------------------------------------------------------
# GENERACIÓN ALEATORIA
# ---------------------------------------------------------

else:

    if st.button("Generar cuotas aleatorias"):

        cuotas_generadas = simulacion_monte_carlo(
            numero_empresas,
            iteraciones=1
        )[0]

        st.session_state["cuotas_aleatorias"] = cuotas_generadas
        st.session_state["n_cuotas_aleatorias"] = numero_empresas


    if "cuotas_aleatorias" in st.session_state:

        # Evitar utilizar cuotas generadas anteriormente
        # para un número diferente de empresas.
        if (
            st.session_state.get("n_cuotas_aleatorias")
            == numero_empresas
        ):

            cuotas_particulares = st.session_state[
                "cuotas_aleatorias"
            ]

            st.write("Cuotas generadas (%):")

            st.write(
                np.round(
                    cuotas_particulares * 100,
                    2
                )
            )

        else:

            st.info(
                "El número de empresas cambió. "
                "Genere nuevamente las cuotas aleatorias."
            )


# =========================================================
# 4. CONFIGURACIÓN DE MONTE CARLO
# =========================================================

st.subheader("4. Simulación de Monte Carlo")

iteraciones = st.number_input(
    "Número de iteraciones:",
    min_value=100,
    max_value=100000,
    value=1000,
    step=100
)

iteraciones = int(iteraciones)

st.warning(
    "Advertencia de carga computacional: aumentar el número "
    "de iteraciones incrementa el tiempo de procesamiento, "
    "la latencia de respuesta y el consumo de recursos "
    "computacionales de la aplicación."
)


# =========================================================
# CONFIGURACIÓN DE k PARA CRk
# =========================================================

k = None

if "Ratio de Concentración (CRk)" in indicadores_seleccionados:

    k = st.number_input(
        "Valor de k para el Ratio de Concentración (CRk):",
        min_value=1,
        max_value=numero_empresas,
        value=min(4, numero_empresas),
        step=1
    )

    k = int(k)


# =========================================================
# 5. EJECUCIÓN Y VISUALIZACIÓN DE MONTE CARLO
# =========================================================

st.subheader("5. Distribución de Monte Carlo")

if st.button(
    "Ejecutar simulación",
    type="primary"
):

    # -----------------------------------------------------
    # VALIDACIONES PREVIAS
    # -----------------------------------------------------

    if not indicadores_seleccionados:

        st.error(
            "Debe seleccionar al menos un indicador."
        )

    elif cuotas_particulares is None:

        st.error(
            "Debe ingresar o generar un caso particular "
            "antes de ejecutar la simulación."
        )

    else:

        try:

            # -------------------------------------------------
            # GENERAR SIMULACIONES DE MONTE CARLO
            # -------------------------------------------------

            simulaciones = simulacion_monte_carlo(
                numero_empresas,
                iteraciones
            )


            # Diccionarios donde se guardarán los resultados
            resultados_guardados = {}
            valores_guardados = {}


            # -------------------------------------------------
            # CALCULAR CADA INDICADOR SELECCIONADO
            # -------------------------------------------------

            for indicador in indicadores_seleccionados:

                # Distribución del indicador para todas
                # las simulaciones de Monte Carlo
                resultados = calcular_distribucion(
                    simulaciones,
                    indicador,
                    k
                )


                # ---------------------------------------------
                # CALCULAR EL CASO PARTICULAR
                # ---------------------------------------------

                if indicador == "Ratio de Concentración (CRk)":

                    valor_particular = crk(
                        list(cuotas_particulares),
                        k
                    )


                elif indicador == (
                    "Índice Herfindahl-Hirschman (IHH)"
                ):

                    valor_particular = ihh(
                        list(cuotas_particulares)
                    )


                elif indicador == "Índice de Dominancia (ID)":

                    valor_particular = indice_dominancia(
                        list(cuotas_particulares)
                    )


                elif indicador == "Índice de Entropía (IE)":

                    valor_particular = indice_entropia(
                        list(cuotas_particulares)
                    )


                # Guardar resultados
                resultados_guardados[indicador] = resultados

                valores_guardados[indicador] = valor_particular


            # -------------------------------------------------
            # GUARDAR INFORMACIÓN EN SESSION STATE
            # -------------------------------------------------

            st.session_state[
                "resultados_simulacion"
            ] = resultados_guardados

            st.session_state[
                "valores_particulares"
            ] = valores_guardados

            st.session_state[
                "empresas_simulacion"
            ] = numero_empresas

            st.session_state[
                "iteraciones_simulacion"
            ] = iteraciones

            st.session_state[
                "k_simulacion"
            ] = k

            st.success(
                "Simulación ejecutada correctamente."
            )


        except (ValueError, TypeError) as error:

            st.error(
                f"Error en los datos ingresados: {error}"
            )


# =========================================================
# MOSTRAR GRÁFICOS
# =========================================================

if "resultados_simulacion" in st.session_state:

    st.markdown("---")

    st.subheader(
        "Resultados de la simulación"
    )


    for indicador, resultados in (
        st.session_state[
            "resultados_simulacion"
        ].items()
    ):

        valor_particular = (
            st.session_state[
                "valores_particulares"
            ][indicador]
        )


        # -----------------------------------------------------
        # CREAR GRÁFICO
        # -----------------------------------------------------

        fig = graficar_distribucion(
            resultados,
            valor_particular,
            indicador
        )


        # -----------------------------------------------------
        # MOSTRAR INDICADOR Y GRÁFICO
        # -----------------------------------------------------

        st.markdown(
            f"### {indicador}"
        )

        st.pyplot(fig)


        # -----------------------------------------------------
        # MOSTRAR VALOR DEL CASO PARTICULAR
        # -----------------------------------------------------

        if indicador == "Ratio de Concentración (CRk)":

            st.write(
                f"**Valor del caso particular:** "
                f"{valor_particular:.2f}%"
            )


        elif indicador == (
            "Índice Herfindahl-Hirschman (IHH)"
        ):

            st.write(
                f"**Valor del caso particular:** "
                f"{valor_particular:.2f} puntos IHH"
            )


        else:

            st.write(
                f"**Valor del caso particular:** "
                f"{valor_particular:.4f}"
            )


# =========================================================
# 6. EVALUADOR INTERACTIVO
# =========================================================

if "resultados_simulacion" in st.session_state:

    st.markdown("---")

    st.subheader(
        "6. Evaluación del nivel de concentración"
    )

    st.write(
        "Analice el caso particular y seleccione el nivel "
        "de concentración que considere correcto."
    )


    # Datos correspondientes a la simulación ejecutada
    numero_empresas_evaluacion = (
        st.session_state[
            "empresas_simulacion"
        ]
    )

    k_evaluacion = (
        st.session_state[
            "k_simulacion"
        ]
    )


    # ---------------------------------------------------------
    # CREAR UNA PREGUNTA PARA CADA INDICADOR
    # ---------------------------------------------------------

    for i, indicador in enumerate(
        st.session_state[
            "resultados_simulacion"
        ]
    ):

        valor_particular = (
            st.session_state[
                "valores_particulares"
            ][indicador]
        )

        resultados = (
            st.session_state[
                "resultados_simulacion"
            ][indicador]
        )


        # -----------------------------------------------------
        # OBTENER CLASIFICACIÓN CORRECTA
        # -----------------------------------------------------

        nivel_correcto, criterio = (
            clasificar_concentracion(
                indicador,
                valor_particular,
                numero_empresas_evaluacion,
                k_evaluacion
            )
        )


        st.markdown(
            f"### {indicador}"
        )


        # -----------------------------------------------------
        # CASO EN QUE EL INDICADOR NO PUEDA CLASIFICARSE
        # -----------------------------------------------------

        if nivel_correcto is None:

            st.info(criterio)

            continue


        # -----------------------------------------------------
        # PREGUNTA AL USUARIO
        # -----------------------------------------------------

        respuesta = st.radio(
            "¿Cómo clasificarías el nivel de concentración "
            "del caso particular?",
            options=[
                "Baja",
                "Moderada",
                "Alta"
            ],
            index=None,
            key=f"respuesta_{i}"
        )


        # -----------------------------------------------------
        # BOTÓN PARA EVALUAR LA RESPUESTA
        # -----------------------------------------------------

        if st.button(
            "Evaluar respuesta",
            key=f"evaluar_{i}"
        ):

            if respuesta is None:

                st.warning(
                    "Debe seleccionar una respuesta."
                )

            else:

                # ---------------------------------------------
                # EVALUAR RESPUESTA Y CALCULAR PERCENTIL
                # ---------------------------------------------

                evaluacion = evaluar_respuesta(
                    indicador,
                    valor_particular,
                    resultados,
                    respuesta,
                    numero_empresas_evaluacion,
                    k_evaluacion
                )


                # ---------------------------------------------
                # INFORMAR SI LA RESPUESTA ES CORRECTA
                # ---------------------------------------------

                if evaluacion["correcta"]:

                    st.success(
                        "Respuesta correcta."
                    )

                else:

                    st.error(
                        "Respuesta incorrecta. "
                        f"El nivel correcto es "
                        f"{evaluacion['nivel']}."
                    )


                # ---------------------------------------------
                # JUSTIFICACIÓN TÉCNICA
                # ---------------------------------------------

                st.write(
                    "**Justificación técnica:** "
                    f"{evaluacion['criterio']}"
                )


                # ---------------------------------------------
                # PERCENTIL
                # ---------------------------------------------

                st.write(
                    "**Percentil del caso particular:** "
                    f"{evaluacion['percentil']:.2f}"
                )


                # ---------------------------------------------
                # RETROALIMENTACIÓN
                # ---------------------------------------------

                st.info(
                    evaluacion[
                        "interpretacion"
                    ]
                )