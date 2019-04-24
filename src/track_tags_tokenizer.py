#!/usr/bin/env python
# encoding: utf-8

import csv
import sys
import argparse
import os
import logging

from utils import set_log_config, PreProcessing, ALLOWED_DATASETS

csv.field_size_limit(sys.maxsize)


def run(dataset):
    """
    """
    pp = PreProcessing()

    # Define input files
    IN_DIR = os.path.join("../data", dataset)
    tracklist_file = os.path.join(
                            IN_DIR, 'tracklist.tsv')
    lastfm_tags = os.path.join(
                            "../data", "lastfm_tags", "lastfm_tags.tsv")
    out_token = os.path.join(
                            IN_DIR, "tracks_tags_token.txt")

    # Import data
    DictTrackTag = pp.import_track_tags(lastfm_tags)

    count_row = 0
    count_row_wrong = 0

    with open(tracklist_file, 'r+') as inf, open(out_token, 'w+') as outf:
        _reader = csv.reader(inf, delimiter='\t')
        _writer = csv.writer(outf, delimiter=' ')
        tag_final = []

        for row in _reader:
            # Skip rows bad-formatted
            if len(row) != 3:
                count_row_wrong += 1
                continue

            idx, artist_name, track_name = row

            if artist_name and track_name:
                artist_name = pp.norm_str(artist_name)
                track_name = pp.norm_str(track_name)

                key = '|'.join([artist_name, track_name])

                if key in DictTrackTag:
                    if DictTrackTag[key]:
                        count_row += 1
                        tags_row = [
                            pp.norm_str(x[0]) for x in DictTrackTag[key]
                            if x[0] != 'n']
                        if tags_row:
                            tag_final += tags_row

        _writer.writerow(tag_final)

    logging.info(
        "Rows processed: {}/{}".format(
            count_row-count_row_wrong, count_row))


def arg_parser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, dest='dataset',
                        help="Dataset name")
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
        run(args.dataset)
