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
Create a virtual environment (tested on Python 3.5), then launch the following command for installing the dependecies (be sure to be in the `src` folder):
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
 For instance, to analyze AOTM dataset launch the following commands: 
```
python playlist_popularity.py -d AOTM
python playlist_diversity.py -d AOTM  
python playlist_qualia.py -d AOTM 
python plot_embeddings_tsne.py -d AOTM
```
In the case of CORN dataset, `playlist_diversity.py` lasts ~20 min, due to longness of average playlist.
