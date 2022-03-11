from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.model_selection import train_test_split
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

time_step = 15
dimension = 12
label_size = 384


# Build features with LSTM_key format
def build_train(train, label):
    X_train, Y_train = [], []
    for i in range(train.shape[0] - time_step + 1):
        X_train.append(np.array(train[i:i+time_step]))
        Y_train.append(np.array(label[i+time_step-1,:]))
    return X_train, Y_train

# Build features from all files
def build_all_train():
    directory = '..\..\data\data_key\\'
    all_csv = [f for f in listdir(directory) if isfile(join(directory, f)) and not isTestScore(f)]
    X_train, Y_train = [], []
    for csv in all_csv:
        x, y = load_train_data(csv, include_chord = True)
        x, y = build_train(x, y)
        X_train += x
        Y_train += y
    return np.array(X_train), np.array(Y_train)

# Create the LSTM_key model
def create_model():
    model = Sequential()
    model.add(LSTM(128, batch_input_shape=(None, time_step, dimension)))
    model.add(Dense(label_size, activation='softmax'))
    model.compile(loss="mean_squared_error", optimizer='adam', metrics= ['accuracy'])
    return model

if __name__ == '__main__':
    features, label = build_all_train()
    X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.25, random_state=624)
    model = create_model()
    model.summary()

    # Train model
    history = model.fit(X_train, y_train, epochs=200, validation_data=(X_test, y_test))

    # Draw loss image
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model train vs validation loss')
    plt.xlabel('Iterations')
    plt.ylabel('loss')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.savefig('loss_all.png')

    predict = model.predict(X_test)
    predict_vec = np.argmax(predict, 1)
    answer_vec = np.argmax(y_test, 1)

    print(predict_vec)
    print(answer_vec)

    acc = np.mean(np.equal(predict_vec, answer_vec))

    print('accuracy: ', acc)

    model.save('LSTM_all')