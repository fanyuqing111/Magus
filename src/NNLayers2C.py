import re

import numpy as np
import tensorflow


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    # positive_examples = list(open(positive_data_file, "r").readlines())
    positive_examples = [tensorflow.reshape([1] * (300 * 70), [-1, 300, 70, 1]) for _ in range(20)]
    positive_examples = [[[[0]] * 300] * 70 for _ in range(20)]

    # negative_examples = list(open(negative_data_file, "r").readlines())
    negative_examples = [tensorflow.reshape([0] * (300 * 70), [-1, 300, 70, 1]) for _ in range(20)]
    negative_examples = [[[[0]] * 300] * 70 for _ in range(20)]

    # Split by words
    # x_text = positive_examples + negative_examples
    # x_text = [clean_str(sent) for sent in x_text]

    # Generate labels
    positive_labels = [[0, 1] for _ in range(20)]
    negative_labels = [[1, 0] for _ in range(20)]

    x = np.concatenate([positive_examples, negative_examples], 0)
    y = np.concatenate([positive_labels, negative_labels], 0)

    return [x, y]


def batch_iter(x, y, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """

    data_size = len(x)

    data = np.array(list(zip(x, y)))

    num_batches_per_epoch = int((len(x) - 1) / batch_size) + 1
    for epoch in range(num_epochs):

        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data

        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)

            x_list = []
            y_list = []
            for i in range(start_index, end_index):
                x_list.append(shuffled_data[i][0])
                y_list.append(shuffled_data[i][1])

            yield x_list, y_list
