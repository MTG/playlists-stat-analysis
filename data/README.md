# How to Add a New Playlist Dataset to Analyze
> If you have any problem during the procedure, please let me know at lorenzo.porcaro at gmail.com

### Create a New Folder for the Data of the New Dataset
After cloning the repo, you can choose to analyze your own dataset. For doing that, start with creating the dataset folder:
```
cd playlist/data
mkdir THE_NAME_OF_YOUR_DATASET
```

### Add Your Dataset Within the Allowed Ones
Open the file `playlist/src/utils.py` and modify the line 9, adding the name of your dataset in the list `ALLOWED_DATASETS`
```python
import logging
import csv
import numpy as np
from annoy import AnnoyIndex

ALLOWED_DATASETS = ["AOTM", "CORN", "DEEZ", "SPOT", "THE_NAME_OF_YOUR_DATASET"]
```

### Add Data to Your Folder for Performing the Popularity Analysis
You need to add two files in the folder `playlist/data/THE_NAME_OF_YOUR_DATASET`:
- `tracklist.tsv` : a TSV file with the complete list of tracks contained in the playlists. It needs to have three column: 1) Track ID ; 2) Artist Name; 3) Track Name (NO HEADER needed). Be sure that the track IDs are the same used in the playlist file. 
- `playlists.tsv`: a TSV file with the complete list of playlists in your dataset. Each line represents a playlists, which will be formed by tab-separated track IDs (i.e. `1\t35\t56\t...etc`)

### Add Data to Your Folder for Performing the Semantic Diversity Analysis
Apart from the files needed for the Popularity Analysis, you need the Tag-embeddings, and the list of tracks with tags associated. 
#### Add Tag-Embeddings
First, create a folder for the embeddings
```
cd playlist/data
mkdir tag_embeds
```
Then, add in the folder the file with the embeddings previously computed. No needs for using GloVe instead of other embeddings. You can try other architectures (and let us know how it works!). The file with the embedding should be a `.txt` file in the following format: 
```
tag_name value1 value2 .... valueN
```
Notice that is not tab-separated, just white-space separated. The dimension of the embeddings by default is 100. If you want to use embeddings with different dimensions, open the file  `playlist/src/utils.py` and modify the line 156, changing the value of the sanity check, by default set at 100:
```python
if len(embs) != THE_DIMENSION_OF_YOUR_EMBEDDINGS:
  logging.error('Problem importing the embeddings')
  break
```
The file with the embedding should be located in the folder previously created, and named as the dataset:
```
playlist/data/tag_embeds/THE_NAME_OF_YOUR_DATSET.txt
```

#### Add Tag-Tracks
First, create a folder for the embeddings
```
cd playlist/data
mkdir lastfm_tags
```
Then, add in the folder the file with the tags previously retrieved. No needs for using LastFm instead of other tags. You can try other tags (and let us know how it works!). The files with the tags should be a TSV file in the following format:
```
ArtistName|TrackName\t[('tag1', w1), ('tag2',w2), ('tag3',w3),('tag4', w5), ('tag5', w5)]
```
Example
```
randy+roos|ray's+passage\t[('guitar virtuoso', 100), ('Mindracers', 100), ('Still Behind the Wheel', 100), ('guitar bud', 100), ('mindracer', 50)]
```

where the `w` are the weights associated to each tag. If you don't have it or don't want to take into account the weights, just set 100 to every `w` (if you are asking why, just read the [paper](http://mtg.upf.edu/node/3959) section 3.3.2 ;) ). `ArtistName` and `Trackname` should be formatted using the [norm_str](https://github.com/LPorcaro/playlist/blob/master/src/utils.py#L81) function defined in `playlist/src/utils.py` (line 81). There is room for improving the normalization function, but for now is the only way to be able to map strings used in different places.

The file with the tags should be located in the folder previously created, and named as following:
```
playlist/data/lastfm_tags/lastfm_tags.tsv
```
