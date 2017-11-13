# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import pickle as Serializer

from libs.neural_classifier import NeuralClassifier
from m_cores.magus_core import MagusCore


class EmitterCore(MagusCore):
    def __init__(self, input_queue, output_queue, tag="Parser", worker_number=0):
        MagusCore.__init__(self, tag, worker_number, input_queue, output_queue)

    def run_core(self):

        def callback(tweet_string):
            if not tweet_string:
                return

            tweet = Serializer.loads(tweet_string)

            if not tweet:
                return

            latitude, longitude = tweet["latitude"], tweet["longitude"]

            coordinates = (latitude, longitude)
            message = (coordinates, NeuralClassifier().classify([]))

            self.out_queue.send_message(Serializer.dumps(message))

        self.in_queue.receive_messages(callback)