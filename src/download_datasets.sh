#!/bin/sh


### AOTM ###
wget https://bmcfee.github.io/data/aotm2011_playlists.json.gz -P ../data/AOTM
gzip -d ../data/AOTM/aotm2011_playlists.json.gz
python playlist_pre.py -i ../data/AOTM/aotm2011_playlists.json -d AOTM
sort ../data/AOTM/playlists.tsv | uniq > ../data/AOTM/playlists_su.tsv
mv ../data/AOTM/playlists_su.tsv ../data/AOTM/playlists.tsv

### SPOT ###
wget https://zenodo.org/record/2594557/files/spotify_playlists.zip -P ../data/SPOT
unzip ../data/SPOT/spotify_playlists.zip -d ../data/SPOT
rm ../data/SPOT/spotify_playlists.zip
python playlist_pre.py -i ../data/SPOT/spotify_dataset.csv -d SPOT
sort ../data/SPOT/playlists.tsv | uniq > ../data/SPOT/playlists_su.tsv
mv ../data/SPOT/playlists_su.tsv ../data/SPOT/playlists.tsv

## CORN ##
wget https://www.cs.cornell.edu/~shuochen/lme/dataset.tar.gz -P ../data/CORN
tar xf ../data/CORN/dataset.tar.gz -C ../data/CORN
rm ../data/CORN/dataset.tar.gz
# Tracks
cp ../data/CORN/dataset/yes_complete/song_hash.txt ../data/CORN/tracklist.tsv
awk -F'\t' '{print $1 "\t"  $3 "\t" $2}' ../data/CORN/tracklist.tsv > \
	../data/CORN/tracklist.tmp.tsv 
mv ../data/CORN/tracklist.tmp.tsv ../data/CORN/tracklist.tsv
# Playlists
touch ../data/CORN/playlists.tsv
cat ../data/CORN/dataset/yes_complete/test.txt \
	../data/CORN/dataset/yes_complete/train.txt >> ../data/CORN/playlists.tsv
tr ' ' \\t < ../data/CORN/playlists.tsv > ../data/CORN/playlists_new.tsv
mv ../data/CORN/playlists_new.tsv  ../data/CORN/playlists.tsv
sort ../data/CORN/playlists.tsv | uniq > ../data/CORN/playlists_su.tsv
mv ../data/CORN/playlists_su.tsv ../data/CORN/playlists.tsv