#!/usr/bin/env python
# encoding: utf-8

import csv
import numpy as np
import sys
import os
import argparse
import logging

from utils import set_log_config, Stats, PreProcessing, ALLOWED_DATASETS

csv.field_size_limit(sys.maxsize)


def run(dataset, print_ex):
    """
    Analyze the 10% of playlists with the highest, and
    the 10% with the lowest diversity index.
    """
    pp = PreProcessing()
    st = Stats()

    # Define input files
    IN_DIR = os.path.join("../data", dataset)
    tracklist_file = os.path.join(
                            IN_DIR, "tracklist.tsv")
    lastfm_tags = os.path.join(
                            "../data", "lastfm_tags", "lastfm_tags.tsv")

    # Import data
    DictTrackTag = pp.import_track_tags(lastfm_tags)
    DictTrack = pp.import_tracklist(tracklist_file)
    low_pDI_playlists = os.path.join(
                                IN_DIR, 'low_pDI_playlists.tsv')
    high_pDI_playlists = os.path.join(
                                IN_DIR, 'high_pDI_playlists.tsv')

    results_pd = []

    for input_file in [low_pDI_playlists, high_pDI_playlists]:

        # Initialize variables
        tag_no = []
        tag_common = []
        ratio_tag_track = []
        artist_no = []
        tracks_no = []
        ratio_track_art = []
        distances = []
        print_c = 0
        playlist_c = 0

        with open(input_file, 'r') as inf:
            _reader = csv.reader(inf, delimiter='\t')

            # Iterate over playlists
            for row in _reader:
                playlist_c += 1
                dist, playlist = row
                playlist = eval(playlist)
                distances.append(float(dist))

                artistnames = set()
                total_tags = set()
                tags_list = []

                # Print playlist info
                if print_c < print_ex:
                    logging.info("Printing info new playlist...")
                    logging.info("Playlist pDI:{}".format(dist))
                    logging.info("Playlist Tracks:")

                # Iterate over playlist tracks
                for track in playlist:
                    track = str(track)
                    try:
                        artistname, trackname = DictTrack[track].split("|")
                    except ValueError:
                        continue
                    artistnames.add(artistname)
                    tags_tracks = set()

                    if DictTrack[track] in DictTrackTag:
                        for tag in DictTrackTag[DictTrack[track]]:
                            total_tags.add(pp.norm_str(tag[0]))
                            tags_tracks.add(pp.norm_str(tag[0]))

                        tags_list.append(tags_tracks)
                        if print_c < print_ex:
                            logging.info(
                                "{} {}".format(
                                    DictTrack[track],
                                    DictTrackTag[DictTrack[track]]))
                    else:
                        tags_list.append(set())
                        continue

                # Print playlist stats
                if print_c < print_ex:
                    logging.info(
                        "No. unique tags: {}".format(
                            len(total_tags)))
                    logging.info(
                        "No. unique tags for tracks: {}".format(
                            len(total_tags)/float(len(playlist))))
                    logging.info(
                        "No. unique artists: {}".format(
                            len(artistnames)))
                    logging.info(
                        "No. unique tracks: {}".format(
                            len(playlist)))
                    logging.info(
                        "No. unique tracks for artists: {}".format(
                            len(playlist)/float(len(artistnames))))

                print_c += 1

                tag_no.append(len(total_tags))
                ratio_tag_track.append(len(total_tags)/float(len(playlist)))
                artist_no.append(len(artistnames))
                tracks_no.append(len(playlist))
                ratio_track_art.append(len(playlist)/float(len(artistnames)))
                tag_common.append(set.intersection(*tags_list))

            common_tags = round(len([x for x in tag_common
                                     if len(x) > 1])*100/float(playlist_c))
            single_artists = round(len([x for x in artist_no
                                        if x == 1])*100/float(playlist_c))

            # Print playlist dataset qualitative analysis results
            logging.info("")
            logging.info(
                "## Qualitative analysis of playlists from {} file ## ".format(
                    input_file))
            logging.info(
                "Average pDI: {}".format(
                    np.mean(distances)))
            logging.info(
                "Average tag count: {}".format(
                    round(np.mean(tag_no))))
            logging.info(
                "Common tags(%): {}".format(common_tags))
            logging.info(
                "Average tag over tracks: {}".format(
                    round(np.mean(ratio_tag_track))))
            logging.info(
                "Average artist count: {}".format(
                    round(np.mean(artist_no))))
            logging.info(
                "Single-artist(%): {}".format(single_artists))
            logging.info(
                "Average tracks count: {}".format(
                    round(np.mean(tracks_no))))
            logging.info(
                "Average tracks over artists: {}".format(
                    round(np.mean(ratio_track_art))))

            # Store results for computing Percentual Difference
            results = [np.mean(distances),
                       round(np.mean(tag_no)),
                       common_tags,
                       round(np.mean(ratio_tag_track)),
                       round(np.mean(artist_no)),
                       single_artists,
                       round(np.mean(tracks_no)),
                       round(np.mean(ratio_track_art))]

            results_pd.append(results)

    logging.info("")
    logging.info("## Percentage Difference (PD) ## ".format(input_file))
    for c in range(0, 8):
        if c not in [2, 5]:
            logging.info(st.pdiff(results_pd[0][c], results_pd[1][c]))
        else:
            logging.info(abs(results_pd[0][c]-results_pd[1][c]))


def arg_parser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, dest='dataset',
                        help="Dataset name")
    parser.add_argument("-P", "--print-ex", type=int, dest='print_ex',
                        default=0, help="Number of playlist to print")
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
        run(args.dataset, args.print_ex)
