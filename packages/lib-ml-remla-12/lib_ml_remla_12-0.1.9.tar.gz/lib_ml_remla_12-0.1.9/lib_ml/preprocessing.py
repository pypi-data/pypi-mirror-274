import pandas as pd

from keras_preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

def parse_data(file):
    "Parse external txt data into raw dataframes"

    data = [line.strip() for line in file.readlines()[1:]]
    raw_x = [line.split("\t")[1] for line in data]
    raw_y = [line.split("\t")[0] for line in data]

    return pd.DataFrame({"url": raw_x, "label": raw_y })

def process_data(raw_train, raw_val, raw_test):
    "Tokenize and encode raw dataframes"

    raw_x_train = raw_train['url'].to_list()
    raw_y_train = raw_train['label']

    raw_x_val = raw_val['url'].to_list()
    raw_y_val = raw_val['label']

    raw_x_test = raw_test['url'].to_list()
    raw_y_test = raw_test['label']

    tokenizer = Tokenizer(lower=True, char_level=True, oov_token='-n-')
    tokenizer.fit_on_texts(raw_x_train + raw_x_val + raw_x_test)
    char_index = tokenizer.word_index
    sequence_length=200
    x_train = pad_sequences(tokenizer.texts_to_sequences(raw_x_train), maxlen=sequence_length)
    x_val = pad_sequences(tokenizer.texts_to_sequences(raw_x_val), maxlen=sequence_length)
    x_test = pad_sequences(tokenizer.texts_to_sequences(raw_x_test), maxlen=sequence_length)

    encoder = LabelEncoder()

    y_train = encoder.fit_transform(raw_y_train)
    y_val = encoder.transform(raw_y_val)
    y_test = encoder.transform(raw_y_test)

    return {
        "char_index": char_index,
        "x_train": x_train,
        "x_val": x_val,
        "x_test": x_test,
        "y_train": y_train,
        "y_val": y_val,
        "y_test": y_test
    }

def process_new_input(url):
    "Tokenize new input"

    input_data = list([url.strip()])

    tokenizer = Tokenizer(lower=True, char_level=True, oov_token='-n-')
    tokenizer.fit_on_texts(input_data)

    return pad_sequences(tokenizer.texts_to_sequences(input_data), maxlen=200)
