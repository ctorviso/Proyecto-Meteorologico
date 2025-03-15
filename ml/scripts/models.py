from keras.api.models import Sequential
from keras.api.layers import Input, Dense, LSTM, GRU, SimpleRNN


def create_gru_v1(shape):

    model = Sequential()

    model.add(Input(shape=shape))

    model.add(GRU(units=50, return_sequences=True))
    model.add(GRU(units=50))

    model.add(Dense(units=1))

    return model

def create_lstm_v1(shape):

    model = Sequential()

    model.add(Input(shape=shape))

    model.add(LSTM(units=50, return_sequences=True))
    model.add(LSTM(units=50))

    model.add(Dense(units=1))

    return model

def create_simplernn_v1(shape):

    model = Sequential()

    model.add(Input(shape=shape))

    model.add(SimpleRNN(units=50, return_sequences=True))
    model.add(SimpleRNN(units=50))

    model.add(Dense(units=1))

    return model
