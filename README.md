# playlist

#### Contact:
>lorenzo.porcaro at gmail.com

#### Clone repos:
```
git clone https://github.com/LPorcaro/playlist.git
cd playlist/src/
git clone https://github.com/oliviaguest/gini
```

#### Installation:
Create a virtual environment (tested on Python 3.5), then launch the following command
 ```
pip install -r requirements.txt
 ```
 
 #### Download dataset (optional):
 It lasts between 5 and 10 minuts, and it is needed around 2GB of free disk
 ```
 mkdir ../data
  ./download_datasets.sh
```

 #### Add new dataset (optional):
 To be updated

 #### Tags data:
For Last.fm tags and tags embeddings write to 
> lorenzo.porcaro at gmail.com

 #### Performing analysis:
```
python playlist_popularity.py -d AOTM
python playlist_diversity.py -d AOTM  (# ~20 min for CORN dataset, due to longness of average playlist) 
python playlist_qualia.py -d AOTM 
python plot_embeddings_tsne.py -d AOTM
```
