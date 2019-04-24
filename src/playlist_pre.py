#!/usr/bin/env python
# encoding: utf-8

import os
import csv
import sys
import json
import argparse
import logging

from utils import set_log_config

csv.field_size_limit(sys.maxsize)


def process_json(infile, out_file_playlist, out_file_tracklist):
    """
    Pre-process AOTM Mix playlists JSON file.
    For more info about the dataset:
    https://bmcfee.github.io/data/aotm2011.html

    """
    logging.info("Reading input file...")
    with open(infile) as json_data:
        d = json.load(json_data)
    logging.info("Done!")

    DictPlay = {}
    DictTrack = {}
    count_track = 0

    for playlist in d:
        key_playlist = playlist['mix_id']
        for track in playlist['playlist']:
            artistname, trackname = track[0]
            key_track = '||'.join([artistname, trackname])

            if key_track not in DictTrack:
                DictTrack[key_track] = count_track
                count_track += 1

            if key_playlist not in DictPlay:
                DictPlay[key_playlist] = []

            DictPlay[key_playlist].append(DictTrack[key_track])

    logging.info("Writing playlist...")
    with open(out_file_playlist, 'w+') as out1:
        _writer1 = csv.writer(out1, delimiter='\t')
        for playlist in DictPlay:
            _writer1.writerow(DictPlay[playlist])

    logging.info("Writing tracklist...")
    with open(out_file_tracklist, 'w+') as out2:
        _writer2 = csv.writer(out2, delimiter='\t')
        for track in DictTrack:
            _writer2.writerow([DictTrack[track]]+track.split('||'))

    logging.info("Done!")

    return len(DictPlay), len(DictTrack)


def process_csv_4c(infile, out_file_playlist, out_file_tracklist):
    """
    Pre-process Twitter/Spotify playlists CSV file.
    For more info about the dataset:
    http://dbis-nowplaying.uibk.ac.at/#playlists
    """
    logging.info("Reading file...")
    with open(infile, 'r') as inf:
        _reader = csv.reader(inf)
        next(_reader)

        DictTrack = {}
        DictPlay = {}
        count = 0
        not_read, read = 0, 0

        for row in _reader:
            row = [x for x in row if x]

            if len(row) != 4 or not row:
                not_read += 1
                continue

            user_id, artistname, trackname, playlistname = row
            key_playlist = '||'.join([playlistname, user_id])
            key_track = '||'.join([artistname, trackname])

            if key_track not in DictTrack:
                DictTrack[key_track] = count
                count += 1

            if key_playlist not in DictPlay:
                DictPlay[key_playlist] = []

            DictPlay[key_playlist].append(DictTrack[key_track])
            read += 1

    logging.info("Done!")
    logging.info("Lines Processed {}/{}".format(read, read + not_read))

    logging.info("Writing playlist...")
    with open(out_file_playlist, 'w+') as out1:
        _writer1 = csv.writer(out1, delimiter='\t')
        for playlist in DictPlay:
            _writer1.writerow(DictPlay[playlist])

    logging.info("Writing tracklist...")
    with open(out_file_tracklist, 'w+') as out2:
        _writer2 = csv.writer(out2, delimiter='\t')
        for track in DictTrack:
            _writer2.writerow([DictTrack[track]]+track.split('||'))

    logging.info("Done!")

    return len(DictPlay), len(DictTrack)


def arg_parser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, dest='input_file',
                        help="Input file with playlist")
    parser.add_argument("-d", "--dataset", type=str, dest='dataset',
                        help="Dataset name")
    parser.add_argument("-l", "--logfile", type=str, help="Log file path")
    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = arg_parser()
    set_log_config(args.logfile, logging.INFO)

    if args.input_file:
        head, tail = os.path.split(args.input_file)
        out_file_playlist = os.path.join(head, "playlists.tsv")
        out_file_tracklist = os.path.join(head, "tracklist.tsv")

    if args.dataset == 'AOTM':
        playlists, tracks = process_json(args.input_file,
                                         out_file_playlist,
                                         out_file_tracklist)
    elif args.dataset == 'SPOT':
        playlists, tracks = process_csv_4c(args.input_file,
                                           out_file_playlist,
                                           out_file_tracklist)
    else:
        logging.error("Dataset '{}' not allowed!".format(args.dataset))
        logging.info("DATASET ALLOWED:")
        logging.info("[AOTM, SPOT]")
        sys.exit()        

    logging.info("Number of playlist found: {}".format(playlists))
    logging.info("Number of tracks found: {}".format(tracks))
