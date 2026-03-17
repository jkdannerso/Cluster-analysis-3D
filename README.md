Cluster Analysis for Cryo-EM Gold Clusters\
\
This repository contains a Python script for analyzing 3D cluster distributions in Cryo-ET data.\
\
## Overview\
The script performs:\
1. **Nearest Neighbor (NN) Analysis**: Calculates distances between localization points.\
2. **DBSCAN Clustering**: Groups points into clusters based on density and spatial proximity.\
3. **Statistical Summary**: Exports cluster sizes, widths, and NN-distances to an Excel report.\
\
## Installation\
Ensure you have Python 3.8+ installed. Install dependencies using:\
```bash\
pip install -r requirements.txt\
\

Usage
1. Data Preparation

The script expects 
.xyz files in a whitespace-separated format (3 columns: x, y, z) without headers.

2. Configuration

Parameters can be adjusted directly in the 
USER-TUNABLE PARAMETERS section at the top of 3dcluster_analysis.py

PIXEL_SIZE_NM: Physical scaling \
\
DBSCAN_EPS_NM: The maximum distance (eps) for cluster inclusion\

DBSCAN_MIN_SAMPLES: Minimum points to form a cluster\

3. Execution\'a0\
Run the script from your terminal:\'a0\
bash python 3dcluster_analysis.py

4. Output
The results are saved as an Excel file containing:
nn_raw: Raw nearest neighbor distances for every localization.\
dbscan_clusters: Detailed statistics for every identified cluster.\
summary: Global mean and standard deviation for the entire dataset.
