#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals
from __future__ import print_function

import tensorflow as tf
# This is a placeholder for a Google-internal import.
from grpc.beta import implementations
from tensorflow.python.framework import tensor_util
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

from libs.sentiments_handling import ANGER, ANTICIPATION, DISGUST, FEAR, JOY, NEUTRAL, SADNESS, SURPRISE, TRUST
from libs.tweet_fetcher import TweetsFetcher
from m_cores.magus_core import MagusCore

EMOTION_LOOKUP = [JOY, TRUST, FEAR, SURPRISE, SADNESS, DISGUST, ANGER, ANTICIPATION, NEUTRAL]


class ClassifierCore(MagusCore):
    def __init__(self, input_queue, output_queue, tag="Classifier", worker_number=0):
        MagusCore.__init__(self, tag, worker_number, input_queue, output_queue)
        self.tweets_stream = TweetsFetcher(locations=("Argentina",))

    def run_core(self):
        for tweet in self.tweets_stream:
            self._log("Tweet received")
            self.out_queue.send_message(self.serializer.dumps(tweet))
            self._log("Tweet sent")

        self.out_queue.close()
        return 0


tf.app.flags.DEFINE_string('server', 'localhost:9000',
                           'PredictionService host:port')
tf.app.flags.DEFINE_string('image', '', 'path to image in JPEG format')
FLAGS = tf.app.flags.FLAGS


def main(_):
    host, port = FLAGS.server.split(':')
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    # Send request
    # See prediction_service.proto for gRPC request/response details.
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'morgana'
    request.model_spec.signature_name = 'predict_tweets'

    # x_text, y = AttardiCNNSchema.get_input_data()

    request.inputs['tweet_features'].CopyFrom(
            tf.contrib.util.make_tensor_proto([[0.1 for _ in range(80)] for _ in range(300)], shape=[1, 80, 300, 1]))
    result = stub.Predict(request, 10.0)  # 10 secs timeout
    result = tensor_util.MakeNdarray(result.outputs["scores"])[0]
    for i in range(len(result)):
        print(EMOTION_LOOKUP[i], ":", result[i])
