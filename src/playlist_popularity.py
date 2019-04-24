#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import numpy as np
import csv
import operator
import argparse
import logging

from gini.gini import gini
from utils import set_log_config, Stats, PreProcessing, ALLOWED_DATASETS


def get_track_popularity(playlists):
    """
    Calculating Tracks popularity
    """
    DictTrackPop = {}
    for playlist in playlists:
        for track in playlist:
            if track not in DictTrackPop:
                DictTrackPop[track] = 0
            DictTrackPop[track] += 1

    return DictTrackPop


def track_popularity_analysis(playlists):
    """
    """
    DictTrackPop = get_track_popularity(playlists)
    logging.info("Total number of tracks: {}".format(len(DictTrackPop)))

    # Get most popular track
    top_tPI = max(DictTrackPop.items(), key=operator.itemgetter(1))[0]

    logging.info(
        "Most popular track <{}>, with tPI: {} ".format(
            top_tPI, DictTrackPop[top_tPI]))

    logging.info("Top tPI divided by number of tracks: {} ".format(
            DictTrackPop[top_tPI]/len(DictTrackPop)))

    # Min-Max normalization
    min_pop, max_pop = [min(DictTrackPop.values()), max(DictTrackPop.values())]
    DictTrackPop = {k: (v-min_pop)/(max_pop-min_pop)
                    for k, v in DictTrackPop.items()}

    # Groupe in 10 groups according to tPI
    DictTrackPopGroup = {}
    for track in DictTrackPop:
        group = int(np.floor(DictTrackPop[track]*10))
        if group not in DictTrackPopGroup:
            DictTrackPopGroup[group] = 0
        DictTrackPopGroup[group] += 1

    # Compute Shannon and Simpson Indexes
    idx = Stats()
    logging.info(
        "Tracks with tPI in [0.0, 0.1) (%): {}".format(
            DictTrackPopGroup[0]*100/len(DictTrackPop)))
    logging.info(
        "Shannon Diversity Index: {}".format(
            idx.shannon_di(DictTrackPopGroup)))
    logging.info(
        "Simpson Diversity Index: {}".format(
            idx.simpson_di(DictTrackPopGroup)))

    return DictTrackPop, min_pop, max_pop


def playlist_popularity_analysis(playlists, DictTrackPop, min_pop,
                                 max_pop, avg_playlist_len):
    """
    """
    playlists_pop = []

    for playlist in playlists:
        playlist_tracks_pop = [DictTrackPop[track] for track in playlist]
        playlist_pop = np.mean(playlist_tracks_pop)
        playlists_pop.append(playlist_pop)

    logging.info(
        "Avg pPI: {}".format(
            np.mean(playlists_pop)*(max_pop-min_pop)-min_pop))

    logging.info(
        "Avg pPI (divided by avg playlist len): {}".format(
            (np.mean(playlists_pop) * (
                max_pop - min_pop) - min_pop) / avg_playlist_len))

    logging.info(
        "pPI Gini Coefficient: {}".format(
            gini(np.array(playlists_pop))))


def run(infile, min_tracks):
    """
    """
    pp = PreProcessing()
    playlists = pp.filter_playlists(
                    pp.import_playlists(
                        playlists_file, args.min_tracks))


    avg_playlist_len = int(np.mean([len(x) for x in playlists]))
    logging.info(
        "Avg playlist lenght: {}".format(avg_playlist_len))

    DictTrackPop, min_pop, max_pop = track_popularity_analysis(playlists)

    playlist_popularity_analysis(playlists,
                                 DictTrackPop,
                                 min_pop,
                                 max_pop,
                                 avg_playlist_len)


def arg_parser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, dest='dataset',
                        help="Dataset name")
    parser.add_argument("-M", "--min-tracks", type=int, dest='min_tracks',
                        default=3, help="Min. number of track for a playlist")
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
        IN_DIR = os.path.join("../data", args.dataset)
        infile = os.path.join(IN_DIR, "playlists.tsv")

    run(infile, args.min_tracks)
