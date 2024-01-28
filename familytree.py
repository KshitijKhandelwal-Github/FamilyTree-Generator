from graphviz import Digraph
import pandas as pd
import numpy as np
import os
import shutil

def CreateTree(filename):
    rawdf = pd.read_excel(filename, keep_default_na=False)  ## Change file path
    el1 = rawdf[['ID','MotherID']]
    el2 = rawdf[['ID','FatherID']]
    el1.columns = ['Child', 'ParentID']
    el2.columns = el1.columns
    el = pd.concat([el1, el2])
    el.replace('', np.nan, regex=True, inplace = True)
    t = pd.DataFrame({'tmp':['no_entry'+str(i) for i in range(el.shape[0])]})
    el['ParentID'].fillna(t['tmp'], inplace=True)
    df = el.merge(rawdf, left_index=True, right_index=True, how='left')
    df['Name'] = df[df.columns[4:6]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)
    df = df.drop(['Child','FatherID', 'MotherID', 'First name', 'Last name'], axis=1)
    df = df[['ID', 'Name', 'S', 'DoB', 'DoD', 'Place of birth', 'Job', 'ParentID','SpouseID']]

    # Create the Digraph
    f = Digraph('neato', format='png', encoding='utf8', filename='familytree', node_attr={'style': 'filled'}, graph_attr={"concentrate": "true", "splines":"ortho"})
    f.attr('node', shape='box')

    # Create clusters for spouses
    spouse_clusters = {}

    placeholder_nodes = set()
    # Iterate through the dataframe to add nodes and clusters
    for index, row in df.iterrows():
        node_id = str(row['ID'])
        node_label = (
            str(row['Name'])
            + '\n' +
            str(row['Job'])
            + '\n DOB: ' +
            str(row['DoB'])
            + '\n' +
            str(row['Place of birth'])
            + '\n DOD: ' +
            str(row['DoD'])
        )
        node_color = 'lightpink' if row['S'] == 'F' else 'lightblue' if row['S'] == 'M' else 'lightgray'

        # Check if the node has a spouse
        if str(row['SpouseID']) != '':
            spouse_id = str(row['SpouseID'])

            # Check if the spouse cluster exists, if not create one
            if spouse_id not in spouse_clusters:
                spouse_clusters[spouse_id] = Digraph('cluster_' + spouse_id)
                spouse_clusters[spouse_id].attr(label='Couple', color='lightgreen', style='filled')

            # Add the node to the spouse cluster
            spouse_clusters[spouse_id].node(node_id, label=node_label, color=node_color)
        else:
            # Add nodes without spouses directly to the main Digraph
            if 'no_entry' not in node_id:
                f.node(node_id, label=node_label, color=node_color)
            else:
                placeholder_nodes.add(node_id)
            

    # Add nodes and clusters to the main Digraph
    for cluster_id, cluster in spouse_clusters.items():
        f.subgraph(cluster)

    # Add edges
    for index, row in df.iterrows():
        if 'no_entry' not in str(row["ParentID"]) and str(row["ParentID"]) not in placeholder_nodes:
            f.edge(str(row["ParentID"]), str(row["ID"]), label='')

    f.render(view=False)

    cwd=os.getcwd()
    file_path=os.path.join(cwd,'familytree.png')
    desktop_path=os.path.join(os.path.expanduser('~'),'Desktop')
    # Check if file already exists 
    try:
        shutil.move(file_path,desktop_path)
        
    except:
        shutil.copy2(file_path, desktop_path)