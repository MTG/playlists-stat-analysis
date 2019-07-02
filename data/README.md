# How to Add a New Playlist Dataset to Analyze

After cloning the repo, you can choose to analyze your own dataset. For doing that, follow this steps:

### Create a New Folder for the Data of the New Dataset
After cloning the repo 
```
cd playlist/data
mkdir THE_NAME_OF_YOUR_DATASET
```


### Add Your Dataset Within the Allowed Ones
Open the file 
`playlist/src/utils.py`
And modify the line 9, adding the name of your dataset in the list `ALLOWED_DATASETS`
```
import logging
import csv
import numpy as np
from annoy import AnnoyIndex

ALLOWED_DATASETS = ["AOTM", "CORN", "DEEZ", "SPOT", "THE_NAME_OF_YOUR_DATASET"]
```

### Add Data to Your Folder for Performing the Popularity Analysis
You need to add two files in the folder `playlist/data/THE_NAME_OF_YOUR_DATASET`
- `tracklist.tsv` : a TSV file with the whole list of tracks contained in the playlists. It needs to have three column: 1) Track ID ; 2) Artist Name; 3) Track Name (no header needed). Be sure that the track IDs are the same used in the playlist file. 
- `playlists.tsv`: a TSV file with the whole list of playlists in your dataset. Each line represents a playlists, which will be formed by tab-separated track IDs (i.e. `1\t35\t56\t...etc`)

### Add Data to Your Folder for Performing the Semantic Diversity Analysis
Apart from the files needed for the Popularity Analysis, you need the Tag-embeddings, and the list of tracks with tags associated. 
#### Add Tag-Embeddings
First, create a folder for the embeddings
```
cd playlist/data
mkdir tag_embeds
```
Then add in the folder the files with the embeddings previously computed. No needs for using GloVe instead of other embeddings. You can try other architectures (and let us know how it works!). The files with the embedding should be `.txt` file in the following format: 
```
tag_name value1 value2 .... valueN
```
Notice that is not tab-separated, just white-space separated. The dimension of the embeddings by default is 100. If you want to use embeddings with different dimensions, open the file 
`playlist/src/utils.py`
And modify the line 156, changing the value of the sanity check, by default set at 100:
```
if len(embs) != THE_DIMENSION_OF_YOUR_EMBEDDINGS:
  logging.error('Problem importing the embeddings')
  break
```
