import gensim

from libs.sentence_yield import TrainSentenceGenerator
from tokenizer.word_tokenizer import WordTokenizer


def generate_embeddings():
    sentences = TrainSentenceGenerator(["../tweets", "../bulk"], WordTokenizer)
    model = gensim.models.Word2Vec(sentences, min_count=1, size=300)
    word_vector = model.wv
    a = word_vector.most_similar(positive=['fox'], topn=5)
    print (a)
    word_vector.save('./mymodel.mdl')

generate_embeddings()
