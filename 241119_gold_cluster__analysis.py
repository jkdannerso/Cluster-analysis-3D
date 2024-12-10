# -*- coding: utf-8 -*-
"""241119_Gold_cluster _analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1weqtz_4Ua8xmsJ8uV8gkd92kZzlswq7-
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

name_csv = "TS_4_rec.xyz.csv"

data = pd.read_csv(name_csv)

data

# make xyz into columns in dataframe

data.iloc[0,0]

# Create a new DataFrame with separate columns for x, y, and z coordinates
new_data = pd.DataFrame(columns=['x', 'y', 'z'])

# Iterate over each row in the original DataFrame
for index, row in data.iterrows():
    coordinates = row['coordinates'].split()
    new_data.loc[index] = coordinates

# Display the new DataFrame
new_data

# make values numeric
new_data['x'] = pd.to_numeric(new_data['x'])
new_data['y'] = pd.to_numeric(new_data['y'])
new_data['z'] = pd.to_numeric(new_data['z'])

# 3d scatterplot using plotly
import plotly.graph_objs as go

trace = go.Scatter3d(x=new_data['x'].values,
                     y=new_data['y'].values,
                     z=new_data['z'].values,
                     mode='markers',
                     # Use hoverinfo and set it to 'text' to display hover labels
                    hoverinfo='text',
                     # Use text to set the content of the hover labels
                     text = [f"Index: {index}<br>X: {x}<br>X: {y}<br>Z: {z}" for index, x, y, z in zip(new_data.index, new_data['x'].values, new_data['y'].values, new_data['z'].values)],
                     marker=dict(color="teal",size= 7, line=dict(color= 'orange',width = 15)))
# Define the layout, use go.Scene instead of Scene
layout = go.Layout(margin=dict(l=0,r=0),scene = go.Scene(),height = 800,width = 800)
data = [trace]
fig = go.Figure(data = data, layout = layout)
fig.show()

#perform DBscan clustering
import plotly.graph_objs as go
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=20, min_samples=2)
dbscan.fit(new_data[['x', 'y', 'z']])  # Use fit instead of fit_predict
cluster_assignment = dbscan.labels_  # Get cluster assignments from labels_

# add cluster label to dataframe
new_data['DBscan_cluster'] = cluster_assignment
new_data


# plot clusters

# Create a dictionary for the scene
Scene = dict(xaxis = dict(title  = 'X coordinate'),yaxis = dict(title  = 'Y coordinate'),zaxis = dict(title  = 'Z coordinate'))

# Select label to be coloured by, here DBscan cluster assignment:
labels = cluster_assignment

# Define a list of distinct colors for the clusters
colors = ['rgb(252, 252, 252)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

# Access DataFrame columns using their names and the `.values` attribute to get a NumPy array
trace = go.Scatter3d(x=new_data['x'].values,
                     y=new_data['y'].values,
                     z=new_data['z'].values,
                     mode='markers',
                     # Use hoverinfo and set it to 'text' to display hover labels
                    hoverinfo='text',
                     # Use text to set the content of the hover labels
                     text = [f"Index: {index}<br>Cluster assignment: {DBscan_cluster}<br>X: {x}<br>X: {y}<br>Z: {z}" for index, x, y, z, DBscan_cluster in zip(new_data.index, new_data['x'].values, new_data['y'].values, new_data['z'].values, new_data['DBscan_cluster'].values)],
                     # set custom colours, one per class using rgb codes
                     marker=dict(color = labels, size= 7, line=dict(color= 'black',width = 10), colorscale=colors))
# Define the layout
layout = go.Layout(margin=dict(l=0,r=0),scene = Scene,height = 800,width = 800)
data = [trace]
fig = go.Figure(data = data, layout = layout)
fig.show()

# print the cluster IDs
print(new_data['DBscan_cluster'].unique())


#######################


# obtain centroids of clusters

import pandas as pd
import numpy as np

# Group data by cluster
grouped = new_data.groupby('DBscan_cluster')
print(grouped)

for cluster_id, group_data in grouped:
        print(f"Cluster {cluster_id}:")
        print(group_data)

# Calculate centroid for each cluster
centroids = {}  # Dictionary to store centroids

for cluster_id, group_data in grouped:
    if cluster_id != -1: # Skip noise points
      centroid_x = group_data['x'].mean()
      centroid_y = group_data['y'].mean()
      centroid_z = group_data['z'].mean()
      centroids[cluster_id] = (centroid_x, centroid_y, centroid_z)

centroids

# Print centroids
for cluster_id, centroid in centroids.items():
    print(f"Cluster {cluster_id}: Centroid = {centroid}")

print(centroids)


##############################


# Add centroid coordinates into dataframe (one per cluster)

# Create a separate DataFrame for centroids
centroid_df = pd.DataFrame(centroids.values(), index=centroids.keys(), columns=['centroid_x', 'centroid_y', 'centroid_z'])
centroid_df['DBscan_cluster'] = centroid_df.index
centroid_df

# Merge centroid_df with new_data to get membrane_segment
centroid_df = pd.merge(centroid_df, new_data[['DBscan_cluster']], on='DBscan_cluster', how='left')

# Drop duplicate rows (if any) and keep only the first occurrence
centroid_df = centroid_df.drop_duplicates(subset=['DBscan_cluster'], keep='first')

# Display the updated centroid_df
centroid_df


################################


# print 3D plot with cluster centroids also displayed
import plotly.graph_objs as go

# Create a dictionary for the scene
Scene = dict(xaxis = dict(title  = 'X coordinate'),yaxis = dict(title  = 'Y coordinate'),zaxis = dict(title  = 'Z coordinate'))

# Select label to be coloured by, here DBscan cluster assignment:
labels = cluster_assignment

# Define a list of distinct colors for the clusters
colors = ['rgb(252, 252, 252)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

# Access DataFrame columns using their names and the `.values` attribute to get a NumPy array
trace = go.Scatter3d(x=new_data['x'].values,
                     y=new_data['y'].values,
                     z=new_data['z'].values,
                     mode='markers',
                     # Use hoverinfo and set it to 'text' to display hover labels
                    hoverinfo='text',
                     # Use text to set the content of the hover labels
                     text = [f"Index: {index}<br>Cluster assignment: {DBscan_cluster}<br>X: {x}<br>X: {y}<br>Z: {z}" for index, x, y, z, DBscan_cluster in zip(new_data.index, new_data['x'].values, new_data['y'].values, new_data['z'].values, new_data['DBscan_cluster'].values)],
                     # set custom colours, one per class using rgb codes
                     marker=dict(color = labels, size= 7, line=dict(color= 'black',width = 10), colorscale=colors),
                     name='Gold particles')     # Add a name to the trace)
# Define the layout
layout = go.Layout(margin=dict(l=0,r=0),scene = Scene,height = 800,width = 800)
data = [trace]
fig = go.Figure(data = data, layout = layout)

# Add trace for centroids with annotations
trace_centroids = go.Scatter3d(
    x=centroid_df['centroid_x'],
    y=centroid_df['centroid_y'],
    z=centroid_df['centroid_z'],
    mode='markers+text',  # Add 'text' to the mode
    marker=dict(
        symbol='diamond',
        size=10,
        color='gold'
    ),
    name='Centroids',
    text=centroid_df.DBscan_cluster.astype(str),  # Set text for labels
    textposition='top center',  # Adjust label position as needed
    textfont=dict(size=16, color='green')  # Customize label font
)

# Update data and layout
data = [trace, trace_centroids]  # Include both traces
layout = go.Layout(margin=dict(l=0, r=0), scene=Scene, height=800, width=800)

# Create and show the figure
fig = go.Figure(data=data, layout=layout)

fig.show()

import pandas as pd
import numpy as np

# Example list of consecutive centroid IDs
centroid_ids = [3,4]  # DEFINE SEGMENT CENTROIDS IN ORDER!!!

# Calculate distances between consecutive centroids
distances = []
for i in range(len(centroid_ids) - 1):
    centroid1_id = centroid_ids[i]
    centroid2_id = centroid_ids[i + 1]

    # Check if centroid IDs exist in centroid_df['DBscan_cluster']
    if centroid1_id in centroid_df['DBscan_cluster'].values and centroid2_id in centroid_df['DBscan_cluster'].values:
        # Get centroid coordinates from centroid_df
        centroid1 = centroid_df[centroid_df['DBscan_cluster'] == centroid1_id][['centroid_x', 'centroid_y', 'centroid_z']].values[0]
        centroid2 = centroid_df[centroid_df['DBscan_cluster'] == centroid2_id][['centroid_x', 'centroid_y', 'centroid_z']].values[0]

        # Calculate distance using Euclidean distance formula
        distance = np.sqrt((centroid2[0] - centroid1[0])**2 +
                           (centroid2[1] - centroid1[1])**2 +
                           (centroid2[2] - centroid1[2])**2)
        distances.append(distance)
    else:
        print(f"Warning: Centroid ID {centroid1_id} or {centroid2_id} not found in centroid_df['DBscan_cluster'].")

# Print the calculated distances
for i, distance in enumerate(distances):
    print(f"Distance between centroid {centroid_ids[i]} and {centroid_ids[i + 1]}: {distance}")


######################


# plot 3D plot with lines for the calculated distances
import plotly.graph_objs as go

# Create a dictionary for the scene
Scene = dict(xaxis = dict(title  = 'X coordinate'),yaxis = dict(title  = 'Y coordinate'),zaxis = dict(title  = 'Z coordinate'))

# Select label to be coloured by, here DBscan cluster assignment:
labels = cluster_assignment

# Define a list of distinct colors for the clusters
colors = ['rgb(252, 252, 252)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

# Access DataFrame columns using their names and the `.values` attribute to get a NumPy array
trace = go.Scatter3d(x=new_data['x'].values,
                     y=new_data['y'].values,
                     z=new_data['z'].values,
                     mode='markers',
                     # Use hoverinfo and set it to 'text' to display hover labels
                    hoverinfo='text',
                     # Use text to set the content of the hover labels
                     text = [f"Index: {index}<br>Cluster assignment: {DBscan_cluster}<br>X: {x}<br>X: {y}<br>Z: {z}" for index, x, y, z, DBscan_cluster in zip(new_data.index, new_data['x'].values, new_data['y'].values, new_data['z'].values, new_data['DBscan_cluster'].values)],
                     # set custom colours, one per class using rgb codes
                     marker=dict(color = labels, size=7, line=dict(color= 'black',width = 10), colorscale=colors),
                     name='Gold particles')     # Add a name to the trace)
# Define the layout
layout = go.Layout(margin=dict(l=0,r=0),scene = Scene,height = 800,width = 800)
data = [trace]
fig = go.Figure(data = data, layout = layout)

# Add trace for centroids with annotations
trace_centroids = go.Scatter3d(
    x=centroid_df['centroid_x'],
    y=centroid_df['centroid_y'],
    z=centroid_df['centroid_z'],
    mode='markers+text',  # Add 'text' to the mode
    marker=dict(
        symbol='diamond',
        size=10,
        color='gold'
    ),
    name='Centroids',
    text=centroid_df.DBscan_cluster.astype(str),
    textposition='top center',
    textfont=dict(size=12, color="black")  # Customize label font
)

cluster_order = centroid_ids

# Extract centroid coordinates in the specified order
centroids = centroid_df.set_index('DBscan_cluster').loc[
    cluster_order, ['centroid_x', 'centroid_y', 'centroid_z']
].values

# Create a list of line segments for the path
line_x = []
line_y = []
line_z = []
for i in range(len(centroids) - 1):
    line_x.extend([centroids[i, 0], centroids[i + 1, 0], None])
    line_y.extend([centroids[i, 1], centroids[i + 1, 1], None])
    line_z.extend([centroids[i, 2], centroids[i + 1, 2], None])

# Add a trace for the line segments
trace_lines = go.Scatter3d(
    x=line_x,
    y=line_y,
    z=line_z,
    mode='lines',
    line=dict(color='red', width=4),
    name='Centroid Path',
)

# Update data and layout
data = [trace, trace_centroids, trace_lines]  # Include line trace
layout = go.Layout(margin=dict(l=0, r=0), scene=Scene, height=800, width=800)

# Create and show the figure
fig = go.Figure(data=data, layout=layout)

fig.show()

# save distances to a dataframe where all distances from different datasets are collected

import pandas as pd
import numpy as np
import os

conversion_factor = 2.72

def calculate_and_save_distances(csv_file, cluster_order, distances):

    # Create or load the DataFrame, saving initially as CSV
    csv_filepath = 'distances.csv'
    if os.path.exists(csv_filepath):
        distances_df = pd.read_csv(csv_filepath)
    else:
        distances_df = pd.DataFrame(columns=['Filename', 'Distances'])
        distances_df.to_csv(csv_filepath, index=False)  # Save initial CSV

    # Apply the conversion factor to the distances
    distances = [d * conversion_factor for d in distances]

    # Add new data to the DataFrame
    new_data = pd.DataFrame({
        'Filename': [csv_file] * len(distances),
        'Distances': distances
    })

    # Append new data to CSV
    new_data.to_csv(csv_filepath, mode='a', header=False, index=False)

    # Load updated CSV and save as Excel
    distances_df = pd.read_csv(csv_filepath)
    distances_df.to_excel('distances.xlsx', index=False)

    return distances_df


# Example usage:
csv_file = name_csv  # Replace with your actual filename
cluster_order = centroid_ids

# Pass the 'distances' variable to the function call
distances_df = calculate_and_save_distances(csv_file, cluster_order, distances)
print(distances_df)

# Repeat this process for new CSV files with different membrane segment IDs


###############


# print histogram over inter-cluster distances

import matplotlib.pyplot as plt
import numpy as np

# Assuming 'distances' is your list of distances
plt.hist(distances_df['Distances'], bins=20, edgecolor='black')  # Adjust 'bins' for desired granularity
plt.xlabel('Inter-Cluster Centroid Distances')
plt.ylabel('Frequency')
plt.title('Distribution of Inter-Cluster Distances')

# Calculate and plot the average distance
avg_distance = np.mean(distances_df['Distances'])
plt.axvline(avg_distance, color='red', linestyle='dashed', linewidth=2, label=f'Average Distance: {avg_distance:.2f}')

# Calculate and visualize standard deviation
std_dev = np.std(distances_df['Distances'])
plt.axvline(avg_distance + std_dev, color='green', linestyle='dotted', linewidth=2, label=f'+1 Std Dev: {avg_distance + std_dev:.2f}')
plt.axvline(avg_distance - std_dev, color='green', linestyle='dotted', linewidth=2, label=f'-1 Std Dev: {avg_distance - std_dev:.2f}')

plt.legend()  # Show the legend to display the average distance line label
plt.show()

# remove distances over 350 nm

distances_sorted = distances_df

distances_sorted = distances_sorted[distances_sorted['Distances'] < 350]
distances_sorted

import matplotlib.pyplot as plt
import numpy as np

# Assuming 'distances' is your list of distances
plt.hist(distances_sorted['Distances'], bins=20, edgecolor='black')  # Adjust 'bins' for desired granularity
plt.xlabel('Inter-Cluster Centroid Distances')
plt.ylabel('Frequency')
plt.title('Distribution of Inter-Cluster Distances (<350 nm)')

# Calculate and plot the average distance
avg_distance = np.mean(distances_sorted['Distances'])
plt.axvline(avg_distance, color='red', linestyle='dashed', linewidth=2, label=f'Average Distance: {avg_distance:.2f}')

# Calculate and visualize standard deviation
std_dev = np.std(distances_sorted['Distances'])
plt.axvline(avg_distance + std_dev, color='green', linestyle='dotted', linewidth=2, label=f'+1 Std Dev: {avg_distance + std_dev:.2f}')
plt.axvline(avg_distance - std_dev, color='green', linestyle='dotted', linewidth=2, label=f'-1 Std Dev: {avg_distance - std_dev:.2f}')

plt.legend()  # Show the legend to display the average distance line label
plt.show()