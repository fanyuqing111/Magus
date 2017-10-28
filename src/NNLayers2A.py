import tensorflow as tf


class TextCNN(object):
    """
    A CNN for text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
    """

    def __init__(
            self, sequence_length, num_classes, vocab_size,
            embedding_size, filter_sizes, num_filters, l2_reg_lambda=0.0):
        # Placeholders for input, output and dropout
        input_features, input_labels = self.create_input_layer(num_classes, sequence_length)

        self.input_x = input_features
        self.input_y = input_labels

        # TODO: Check
        convolution_layer_output, output_channels = self.create_conv_pool_layer(self.input_x,
                                                                                embedding_size,
                                                                                filter_sizes,
                                                                                num_filters,
                                                                                vocab_size)

        dropout_layer_output = self.create_dropout_layer(convolution_layer_output)

        scores, predictions, l2_loss = self.create_output_layer(dropout_layer_output, output_channels, num_classes)

        self.loss = self.get_loss(self.input_y, l2_loss, l2_reg_lambda, scores)
        self.accuracy = self.get_accuracy(self.input_y, predictions)

    @staticmethod
    def get_accuracy(input_labels, predictions):
        # Accuracy
        with tf.name_scope("accuracy"):
            correct_predictions = tf.equal(predictions, tf.argmax(input_labels, 1))
            return tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")

    @staticmethod
    def get_loss(input_labels, l2_loss, l2_reg_lambda, scores):
        # Calculate mean cross-entropy loss
        with tf.name_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(logits=scores, labels=input_labels)
            return tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

    @staticmethod
    def create_output_layer(input_layer, input_size, num_classes,
                            l2_loss=tf.constant(0.0),
                            bias=0.1):
        # Final (unnormalized) scores and predictions

        with tf.name_scope("output-layer"):
            W = tf.get_variable(
                    name="W",
                    shape=[input_size, num_classes],
                    initializer=tf.contrib.layers.xavier_initializer())

            b = tf.Variable(tf.constant(bias, shape=[num_classes]), name="b")

            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)

            scores = tf.nn.xw_plus_b(input_layer, W, b, name="scores")
            predictions = tf.argmax(scores, 1, name="predictions")

        return scores, predictions, l2_loss

    @staticmethod
    def create_dropout_layer(input_layer,
                             dropout_prob=tf.placeholder(tf.float32, name="dropout_keep_prob-X"),
                             layer_number=0):
        # Add dropout
        with tf.name_scope("dropout-{}".format(layer_number)):
            return tf.nn.dropout(input_layer, dropout_prob)

    @staticmethod
    def create_conv_pool_layer(input_layer, embedding_size, filter_sizes, num_filters, sequence_height,
                               layer_number=0):
        """Creates a convolution plus a maxpool layer for each filter size"""

        layer_outputs = []

        for i, filter_height in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-{}-{}".format(layer_number, filter_height)):
                convolution_layer = TextCNN.create_filter(input_layer, filter_height, embedding_size, num_filters)
                max_pooling_layer = TextCNN.create_max_pooling(convolution_layer, filter_height, sequence_height)
                layer_outputs.append(max_pooling_layer)

        num_filters_total = num_filters * len(filter_sizes)

        return tf.reshape(tf.concat(layer_outputs, 3), [-1, num_filters_total]), num_filters_total

    @staticmethod
    def create_max_pooling(input_layer, filter_height, sequence_length,
                           strides=(1, 1, 1, 1),
                           padding="VALID"):
        # Maxpooling over the outputs

        print(input_layer)
        print(sequence_length)
        print(filter_height)
        print()

        pooled = tf.nn.max_pool(
                input_layer,
                ksize=[1, sequence_length - filter_height + 1, 1, 1],
                strides=strides,
                padding=padding,
                name="pooling-layer")
        return pooled

    @staticmethod
    def create_filter(input_layer, filter_height, filter_width,
                      number_of_filters=32,
                      strides=(1, 1, 12, 1),
                      padding="VALID",
                      bias=0.1,
                      stddev=0.1,
                      activation=tf.nn.relu):
        # Convolution Layer
        filter_shape = [filter_height, filter_width, 1, number_of_filters]

        filters = tf.Variable(tf.truncated_normal(filter_shape, stddev=stddev), name="filters")
        filters_bias = tf.Variable(tf.constant(bias, shape=[number_of_filters]), name="filters-bias")

        convolution_layer = tf.nn.conv2d(
                input_layer,
                filters,
                strides=strides,
                padding=padding,
                name="convolution-layer")

        # Apply nonlinearity
        filter_layers = activation(tf.nn.bias_add(convolution_layer, filters_bias), name="activation")
        return filter_layers

    @staticmethod
    def create_input_layer(num_classes, sequence_length):
        # shape of input = [batch, in_height, in_width, in_channels]

        input_x = tf.placeholder(tf.float32, [1, 70, 300, 1], name="input_x")
        input_y = tf.placeholder(tf.int32, [None, num_classes], name="input_y")

        return input_x, input_y
