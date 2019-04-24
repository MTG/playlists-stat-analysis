#!/usr/bin/env python
# encoding: utf-8


import itertools
import csv
import numpy as np
import random
import sys
import os
import argparse
import logging

from gini.gini import gini
from utils import set_log_config, Stats, PreProcessing, ALLOWED_DATASETS

csv.field_size_limit(sys.maxsize)


class PlaylistDI(object):
    """
    """
    def __init__(self, dataset, min_tracks):
        """
        """
        # Inizialize classes
        self.pp = PreProcessing()
        self.st = Stats()

        # Define input files
        IN_DIR = os.path.join("../data", dataset)
        playlists_file = os.path.join(
                                IN_DIR, "playlists.tsv")
        tracklist_file = os.path.join(
                                IN_DIR, "tracklist.tsv")
        glove_embs = os.path.join(
                                "../data", "tag_embeds", dataset+".txt")
        lastfm_tags = os.path.join(
                                "../data", "lastfm_tags", "lastfm_tags.tsv")

        # Import data
        DictEmbeds, self.DictKeyEmbeds = self.pp.import_embeddings(glove_embs)
        self.a_idx = self.pp.create_annoy_idx(DictEmbeds)
        self.DictTrackTag = self.pp.import_track_tags(lastfm_tags)
        self.playlists = self.pp.filter_playlists(
                            self.pp.import_playlists(
                                playlists_file, min_tracks))
        self.DictTrack = self.pp.import_tracklist(tracklist_file)

        # Define variables
        self.low_pDI_playlists = os.path.join(
                                IN_DIR, 'low_pDI_playlists.tsv')
        self.high_pDI_playlists = os.path.join(
                                IN_DIR, 'high_pDI_playlists.tsv')
        self.rand_tracks_playlist = []

    def tag_distance(self, word1, word2):
        """
        """
        word1 = self.pp.norm_str(word1)
        word2 = self.pp.norm_str(word2)
        try:
            dist = self.a_idx.get_distance(
                self.DictKeyEmbeds[word1], self.DictKeyEmbeds[word2])
        except KeyError:
            dist = -1

        return dist

    def TT_distance(self, v1, v2):
        """
        """
        if not v1 or not v2:
            return -1

        max_len = max(len(v1), len(v2))

        # TODO ### improve propagation when incomplete information
        if len(v1) < max_len:
            return -1
        elif len(v2) < max_len:
            return -1

        s = 0
        for i in range(max_len):
            max_weight = max(v1[i][1], v2[i][1])

            if max_weight == 0:
                s += 0
                max_len += -1
            else:
                dist = self.tag_distance(v1[i][0], v2[i][0])
                if dist == -1:
                    s += 0
                    max_len += -1
                else:
                    s += ((v1[i][1]+v2[i][1])/float(2*max_weight)*dist)

        if max_len == 0:
            return -1

        return(s/float(max_len))

    def log_results(self, results):
        """
        """
        logging.info("Mean pDI: {}".format(np.mean(results)))
        logging.info("Std pDI: {}".format(np.std(results)))
        logging.info("Max pDI: {}".format(max(results)))
        logging.info("Min pDI: {}".format(min(results)))
        logging.info("Gini pDI: {}".format(gini(np.array(results))))
        logging.info("QCD pDI: {}".format(self.st.qcd(results)))

    def analyze_playlist(self):
        """
        """
        logging.info("Analyzing Playlists...")
        pDI = []
        pDI_idx = []
        playlist_analyzed = 0

        for c, playlist in enumerate(self.playlists):
            playlist_track_tags = []
            playlist_tracks_tags_count = 0
            for track in playlist:
                track = str(track).strip()
                try:
                    # Continue if track has at least 1 tag associated
                    if self.DictTrackTag[self.DictTrack[track]]:
                        playlist_track_tags.append(
                            self.DictTrackTag[self.DictTrack[track]])
                        playlist_tracks_tags_count += 1

                        # Get random tracks for evaluation
                        if random.randint(0, 9) > 5:
                            self.rand_tracks_playlist.append(
                                self.DictTrackTag[self.DictTrack[track]])
                # Skip if tracks has not tags associated
                except KeyError:
                    pass

            # Skip playlist without complete information
            if playlist_tracks_tags_count >= int(1*len(playlist)):
                playlist_analyzed += 1
                pDI_sum = 0

                tracks_comb = list(itertools.combinations(
                                                playlist_track_tags, 2))

                for track_tags in tracks_comb:
                    dist = self.TT_distance(track_tags[0], track_tags[1])
                    if dist == -1:
                        tracks_comb.remove(track_tags)
                    else:
                        pDI_sum += dist
                if pDI_sum == 0:
                    pass
                else:
                    pDI.append(pDI_sum/float(len(tracks_comb)))
                    pDI_idx.append(c)

        self.log_results(pDI)

        logging.info(
            "Playlists analyzed: {}/{}".format(
                playlist_analyzed, len(self.playlists)))

        return pDI, pDI_idx

    def analyze_random_playlist(self):
        """
        """
        logging.info("Analyzing Random Playlists...")
        if 
        playlist_len_mean = int(np.mean([len(x) for x in self.playlists]))

        k = 0
        while k < 1:
            # Shuffle tracks at each iteration
            rand_tracks_playlist = random.sample(
                    self.rand_tracks_playlist, len(self.rand_tracks_playlist))

            rand_pDI = []
            random_playlists = [
                    rand_tracks_playlist[x:x+playlist_len_mean]
                    for x in range(
                        0, len(rand_tracks_playlist), playlist_len_mean)]

            for el in random_playlists:
                rand_pDI_sum = 0
                tracks_comb = list(itertools.combinations(el, 2))
                for track_tags in tracks_comb:
                    dist = self.TT_distance(track_tags[0], track_tags[1])

                    if dist == -1:
                        tracks_comb.remove(track_tags)
                    else:
                        rand_pDI_sum += dist

                if tracks_comb:
                    if rand_pDI_sum == 0:
                        pass
                    else:
                        rand_pDI.append(rand_pDI_sum/float(len(tracks_comb)))

            self.log_results(rand_pDI)
            k += 1

    def write_playlist_qualia(self, pDI, pDI_idx):
        """
        """
        dist_10pct = int(0.1*len(pDI))
        # Write most similar playlists
        with open(self.low_pDI_playlists, 'w+') as outf:
            _writer = csv.writer(outf, delimiter='\t')
            for idx in sorted(range(len(pDI)), key=lambda i: pDI[i],
                              reverse=False)[:dist_10pct]:
                row = [pDI[idx], self.playlists[pDI_idx[idx]]]
                _writer.writerow(row)

        # Write less similar playlists
        with open(self.high_pDI_playlists, 'w+') as outf:
            _writer = csv.writer(outf, delimiter='\t')
            for idx in sorted(range(len(pDI)), key=lambda i: pDI[i],
                              reverse=True)[:dist_10pct]:
                row = [pDI[idx], self.playlists[pDI_idx[idx]]]
                _writer.writerow(row)

    def run(self):
        """
        """
        pDI, pDI_idx = self.analyze_playlist()
        self.analyze_random_playlist()
        self.write_playlist_qualia(pDI, pDI_idx)


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


if __name__ == "__main__":

    args = arg_parser()
    set_log_config(args.logfile, logging.INFO)

    if args.dataset not in ALLOWED_DATASETS:
        logging.error("Dataset '{}' not allowed!".format(args.dataset))
        logging.info("DATASET ALLOWED:")
        logging.info("{}".format(ALLOWED_DATASETS))
        sys.exit()
    else:
        pDI = PlaylistDI(args.dataset, args.min_tracks)
        pDI.run()
