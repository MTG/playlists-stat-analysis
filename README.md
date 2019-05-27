# playlist


git clone https://github.com/LPorcaro/playlist.git
cd playlist/src/
git clone https://github.com/oliviaguest/gini

Create a virtual environment (tested on Python 3.5)
pip install -r requirements.txt
 
 mkdir ../data
  ./download_datasets.sh # Approx ~5-10 min , needed ~2GB of free disk
  
For Last.fm tags and tags embeddings write to lorenzo.porcaro at gmail.com


python playlist_popularity.py -d AOTM
python playlist_diversity.py -d AOTM  (# ~20 min for CORN dataset, due to longness of average playlist) 
python playlist_qualia.py -d AOTM 

python plot_embeddings_tsne.py -d AOTM
