# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from libs.embeddings_handler import EmbeddingHandler
from libs.tweet_parser import TweetParser
from m_cores.magus_core import MagusCore


class WordEmbeddingCore(MagusCore):
    def __init__(self, input_queue, output_queue, tag="Word Embedding", worker_number=0):
        MagusCore.__init__(self, tag, worker_number, input_queue, output_queue)
        self.embeddings = EmbeddingHandler("words", 300, 80)

    def run_core(self):
        def callback(tweet_string):
            if not tweet_string:
                return

            tweet = self.serializer.loads(tweet_string)
            if not tweet:
                self._log("Can't deserialize tweet")
                return
            self.out_queue.send_message(tweet_string)

            matrix = self.embeddings.get_embedding_matrix(tweet["words"])

            with open("vectors/word_matrix_{}".format(tweet[TweetParser.TWEET_ID])) as matrix_file:
                matrix_file.write(self.serializer.dumps(matrix))

        self.in_queue.receive_messages(callback)
