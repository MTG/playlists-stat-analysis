# 20 Years of Playlists: a Statistical Analysis on Popularity and Diversity

The proposed methodology can be applied to characterize playlists in terms of popularity and semantic diversity, allowing the comparative analysis of human-generated and algorithm-generated playlists in different contexts such as historical periods, platforms and musical genres. We find extremely valuable to compare different playlist datasets, as it allows to understand how changes in the listening experience are affecting playlist creation strategies.

This repository contains code to reproduce the results of our [paper](http://mtg.upf.edu/node/3959).

#### Reference:
> Lorenzo Porcaro, Emilia Gómez (2019). 20 Years of Playlists: A Statistical Analysis on Popularity and Diversity. Paper to be presented at the 20th Conference of the International Society for Music Information Retrieval (ISMIR 2019), Delft, The Netherlands, 4-8 November.

#### Contact:
>lorenzo.porcaro at gmail.com

#### Clone repos:
```
git clone https://github.com/LPorcaro/playlist.git
cd playlist/src/
git clone https://github.com/oliviaguest/gini
```

#### Installation:
Create a virtual environment (tested on Python 3.5), then launch the following command for installing the dependencies (be sure to be in the `src` folder):
 ```
pip install -r requirements.txt
 ```
 
 #### Download dataset (optional):
 It lasts between 5 and 10 minutes, and it is needed around 2GB of free disk
 ```
 mkdir ../data
  ./download_datasets.sh
```

 #### Add new dataset (optional):
 Check [data/README.md](https://github.com/LPorcaro/playlist/blob/master/data/README.md)

 #### Tags data:
For Last.fm tags and tags embeddings write to 
> lorenzo.porcaro at gmail.com

 #### Analyze Dataset:
 For instance, to analyze AOTM dataset launch the following commands: 
 
##### Playlist Popularity Analysis:
```
python playlist_popularity.py -d AOTM
```
##### Playlist Diversity Analysis:
```
python playlist_diversity.py -d AOTM
```
##### Playlist Qualitative Analysis:
```
python playlist_qualia.py -d AOTM 
```
##### Plot tag-embeddings using [t-SNE](https://lvdmaaten.github.io/tsne/) algorithm:
```
python plot_embeddings_tsne.py -d AOTM
```
In the case of CORN dataset, `playlist_diversity.py` lasts ~20 min, due to longness of average playlist.
