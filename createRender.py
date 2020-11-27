import open3d
import numpy as np
import math

#make pcd read the xyz file and specify the format as xyz
pcd = open3d.io.read_point_cloud("holdXYZ.xyz", format = 'xyz')
lines = [] #this is where we store the vecs

for i in range(4): #use the nested for loop to append the new line vectors for creating singular planes
    for j in range(171):
        lines.append([j+i*171,j+i*171+171]) #append here 

for i in range(4):#connect the points from prev to next using the nested loops for attaching the singular planes
    for j in range(171):
        if j == 170: #connect the last coordinate to the 0th one. 
            lines.append([j + i * 171, 0 + i * 171])
        else: #connect all other coordinates
            lines.append([j + i * 171, j + 1 + i * 171])
            
#make open3d obeject
lines_set = open3d.geometry.LineSet()
#make open3d obeject
lines_set.points = open3d.utility.Vector3dVector(np.asarray(pcd.points))
#make open3d obeject
lines_set.lines = open3d.utility.Vector2iVector(lines)
#make model
open3d.visualization.draw_geometries([lines_set])
