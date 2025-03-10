import streamlit as st
from src.streamlit_app.Pages.ML.RNNs import show
from src.streamlit_app.Pages.ML.Intro import show as show_intro

intro, gru, lstm, simple_rnn, prophet = st.tabs(["Introducción", "GRU", "LSTM", "SimpleRNN", "Prophet"])

with intro:
    show_intro(intro)

with gru:
    gru.markdown("""
    ## Modelo Gated Recurrent Unit (GRU)

    El modelo GRU es una variante de las redes neuronales recurrentes (RNN) que intenta resolver el problema de la desaparición del gradiente. A diferencia de las RNN tradicionales, las GRU tienen una estructura más simple y solo tienen dos puertas: una de reinicio y otra de actualización. Estas puertas permiten que las GRU "olviden" o "recuerden" información de manera más eficiente que las RNN tradicionales.

    """)

    show(gru, "gru")

with simple_rnn:

    simple_rnn.markdown("""
    
    ## Modelo SimpleRNN
    
    El modelo SimpleRNN es una variante de las redes neuronales recurrentes (RNN) que intenta resolver el problema de la desaparición del gradiente. A diferencia de las RNN tradicionales, las SimpleRNN tienen una estructura más simple y solo tienen una puerta. Esta puerta permite que las SimpleRNN "olviden" o "recuerden" información de manera más eficiente que las RNN tradicionales.
    
    """)

    show(simple_rnn, "simplernn")

with lstm:

    lstm.markdown("""
    ## Modelo Long Short-Term Memory (LSTM)

    El modelo LSTM es una variante de las redes neuronales recurrentes (RNN) que intenta resolver el problema de la desaparición del gradiente. A diferencia de las RNN tradicionales, las LSTM tienen una estructura más compleja y tienen tres puertas: una de reinicio, una de actualización y una de olvido. Estas puertas permiten que las LSTM "olviden" o "recuerden" información de manera más eficiente que las RNN tradicionales.

    """)

    show(lstm, "lstm")

with prophet:

    prophet.markdown("""
    ## Modelo Prophet

    Prophet es una librería de código abierto desarrollada por Facebook. Esta librería está diseñada para realizar pronósticos de series temporales de manera sencilla y eficiente. Prophet es capaz de manejar series temporales con tendencias, estacionalidades y días festivos. Además, Prophet es capaz de manejar datos faltantes y outliers de manera eficiente.

    """)

    show(prophet, "prophet")