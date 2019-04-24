#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse
import logging

from sklearn.manifold import TSNE

from utils import set_log_config, PreProcessing, ALLOWED_DATASETS


def tsne_plot_similar_words(title, labels, embedding_clusters, word_clusters,
                            a, filename):
    """
    """
    plt.figure(figsize=(16, 9))
    colors = cm.rainbow(np.linspace(0, 1, len(labels)))
    markers = ['^', 's', '+', 'o', 'D']
    for label, embeddings, words, color, marker in zip(
            labels, embedding_clusters, word_clusters, colors, markers):
        x = embeddings[:, 0]
        y = embeddings[:, 1]
        plt.scatter(x, y, c=color, marker=marker, alpha=a, label=label)
        for i, word in enumerate(words):
            plt.annotate(word, alpha=0.5, xy=(x[i], y[i]), xytext=(5, 2),
                         textcoords='offset points', ha='right',
                         va='bottom', size=18)
    plt.legend(loc=1, fontsize='x-large')
    plt.title(title)
    plt.grid(False)
    plt.axis('off')
    if filename:
        plt.savefig(filename, format='png', dpi=150, bbox_inches='tight')
    plt.show()


def create_clusters(DictEmbeds, DictKeyEmbeds, keys, a_idx, item_sim):
    """
    """
    embedding_clusters = []
    word_clusters = []

    for word in keys:
        for key in DictKeyEmbeds:
            if key == word:
                embeddings, words = ([], [])
                for similar_word in \
                    a_idx.get_nns_by_item(DictKeyEmbeds[key], item_sim,
                                          search_k=30,
                                          include_distances=False):

                    words += (
                        [k for k, v in DictKeyEmbeds.items()
                         if DictKeyEmbeds[k] == similar_word])
                    embeddings.append(DictEmbeds[similar_word])
                embedding_clusters.append(embeddings)
                word_clusters.append(words)

    return embedding_clusters, word_clusters


def run(dataset, item_sim, keys):
    """
    """
    glove_embs = os.path.join("../data", "tag_embeds", dataset+'.txt')
    pp = PreProcessing()

    DictEmbeds, DictKeyEmbeds = pp.import_embeddings(glove_embs)
    a_idx = pp.create_annoy_idx(DictEmbeds)

    embedding_clusters, word_clusters = create_clusters(DictEmbeds,
                                                        DictKeyEmbeds,
                                                        keys,
                                                        a_idx,
                                                        item_sim)

    embedding_clusters = np.array(embedding_clusters)
    n, m, k = embedding_clusters.shape

    tsne_model_en_2d = TSNE(perplexity=15, n_components=2, init='pca',
                            n_iter=3500, random_state=32)

    embeddings_en_2d = np.array(tsne_model_en_2d.fit_transform(
                                embedding_clusters.reshape(n * m, k))
                                ).reshape(n, m, 2)

    tsne_plot_similar_words('', keys, embeddings_en_2d, word_clusters,
                            0.7, filename=None)


def arg_parser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, dest='dataset',
                        help="Dataset name")
    parser.add_argument("-i", "--items-sim", type=int, dest='item_sim',
                        default=5, help="Similar tags to plot [1-5]")
    parser.add_argument('-k', '--keys', nargs='+', dest='keys',
                        default=['rock', 'pop', 'jazz',
                                 'electronic', 'classical'],
                        help='Key Tags (max 5 keys)')
    parser.add_argument("-l", "--logfile", type=str, help="Log file path")

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = arg_parser()
    set_log_config(args.logfile, logging.INFO)

    if args.dataset not in ALLOWED_DATASETS:
        logging.error("Dataset '{}' not allowed!".format(args.dataset))
        logging.info("DATASET ALLOWED:")
        logging.info("{}".format(ALLOWED_DATASETS))
        sys.exit()

    else:
        run(args.dataset,
            args.item_sim,
            args.keys)
