#!/usr/bin/env python
# encoding: utf-8

import logging
import csv
import numpy as np
from annoy import AnnoyIndex

ALLOWED_DATASETS = ["AOTM", "CORN", "DEEZ", "SPOT"]

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'


def set_log_config(logfile, level):
    """
    Configure log file
    """
    if logfile:
        logging.basicConfig(filename=logfile,
                            format=LOG_FORMAT,
                            level=level)
    else:
        logging.basicConfig(format=LOG_FORMAT,
                            level=level)


class Stats(object):

    def __init__(self):
        """
        """
        pass

    def shannon_di(self, data):
        """
        """
        from math import log as ln

        def p(n, N):
            if n is 0:
                return 0
            else:
                return (float(n)/N) * ln(float(n)/N)

        N = sum([x for x in data.values()])
        return -sum(p(n, N) for n in data.values() if n is not 0)

    def simpson_di(self, data):
        """
        """
        N = sum([x for x in data.values()])
        n = sum([x*(x-1) for x in data.values()])

        return 1 - (n/float((N*(N-1))))

    def qcd(self, array):
        """
        Quartile coefficient of dispersion
        """
        array = np.array(array)
        q3, q1 = np.percentile(array, [75, 25])

        return ((q3-q1)/(q3+q1))

    def pdiff(self, a, b):
        """
        """
        c = abs(a-b)
        d = (a+b)/float(2)
        return round(100*c/float(d))


class PreProcessing(object):

    def __init__(self):
        """
        """
        pass

    def norm_str(self, input):
        return input.replace(
            '#', '+').replace(
            '&', ' ').replace(
            ' ', '+').replace(
            '++', '+').lower().strip()

    def import_playlists(self, infile, min_tracks):
        """
        """
        logging.info("Importing playlists...")
        playlists = []

        with open(infile, 'r') as inf:
            _reader = csv.reader(inf, delimiter='\t')
            for row in _reader:
                playlist = set([int(x) for x in row if x])
                if playlist and len(playlist) > min_tracks:
                        playlists.append(playlist)

        logging.info(
            'Imported {} playlists with more than {} tracks'.format(
                len(playlists), min_tracks))
        return playlists

    def filter_playlists(self, playlists):
        """
        """
        # Interquantile range
        playlist_lens = [len(x) for x in playlists]
        q75, q25 = np.percentile(playlist_lens, [75, 25])
        iqr = q75 - q25
        IQ_min, IQ_max = [q25 - (iqr*1.5), q75 + (iqr*1.5)]

        logging.info(
            "min(len)={}, max(len)={}".format(
                min(playlist_lens), max(playlist_lens)))

        max_len = 10000000000
        min_len = -1
        logging.info("Removing outliers...")
        while max_len > IQ_max or min_len < IQ_min:
            for playlist in playlists:
                if len(playlist) < IQ_min:
                    playlists.remove(playlist)
                elif len(playlist) > IQ_max:
                    playlists.remove(playlist)
            playlist_lens_new = [len(x) for x in playlists]
            max_len = max(playlist_lens_new)
            min_len = min(playlist_lens_new)

        logging.info(
            "Total playlists (w/o outliers): {}".format(len(playlists)))
        logging.info(
            "min(len)={}, max(len)={} (w/o outliers)".format(min_len, max_len))

        return playlists

    def import_embeddings(self, glove_embs):
        """
        """
        logging.info('Importing GloVe tag-embeddings...')
        DictEmbeds = {}
        DictKeyEmbeds = {}
        with open(glove_embs, 'r+') as inf:
            _reader = csv.reader(inf, delimiter=' ')
            for c, row in enumerate(_reader):
                key = row[0]
                embs = [float(x) for x in row[1:]]
                if len(embs) < 100:
                    logging.error('Problem importing the embeddings')
                    break
                DictEmbeds[c] = embs
                DictKeyEmbeds[key] = c

        logging.info("Stored Tag embeddings: {}".format(len(DictEmbeds)))
        return DictEmbeds, DictKeyEmbeds

    def import_track_tags(self, tag_file):
        """
        """
        logging.info("Importing Last.fm tags...")
        DictTrackTag = {}
        with open(tag_file, 'r+') as inf:
            _reader = csv.reader(inf, delimiter='\t')
            for c, row in enumerate(_reader):
                if len(row) != 2:
                    logging.debug("Row not formatted properly")
                    logging.debug(row)
                    continue
                key, tags = row
                if key not in DictTrackTag:
                    DictTrackTag[key] = eval(tags)
        logging.info("Stored Track-tags: {}".format(len(DictTrackTag)))
        logging.info("Done!")
        return DictTrackTag

    def import_tracklist(self, tracklist):
        """
        """
        DictTrack = {}
        with open(tracklist, 'r+') as inf:
            _reader = csv.reader(inf, delimiter='\t')
            for row in _reader:
                if len(row) != 3:
                    logging.debug("Row not formatted properly")
                    logging.debug(row)
                    continue
                count, artist_name, track_name = row
                count = count.strip()
                artist_name = self.norm_str(artist_name)
                track_name = self.norm_str(track_name)
                if artist_name and track_name:
                    key = '|'.join([artist_name, track_name])
                    DictTrack[count] = key
        logging.info("Stored tracks: {}".format(len(DictTrack)))
        return DictTrack

    def create_annoy_idx(self, DictEmbeddings):
        """
        """
        logging.info("Creating Annoy Index...")
        t = AnnoyIndex(100, metric="angular")
        for key in DictEmbeddings:
            t.add_item(key, DictEmbeddings[key])
        t.build(200)
        logging.info("Done!")
        return t
