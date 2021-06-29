Code to compute cubical persistent homology and other topological descriptors (via Gudhi)

1. write_images.m
   Transforms video frames to grayscale (or other user-defined scale), 
   Input: video or video frames from experiments
   Output: cropped grey-scale images (might produce R,G B channels too; *.png files)  and parameters.csv
   
   
2. write_perseus.m
    Produces perseus-formatted files from processed frames.
	Input: write_images.m output files
	Output: perseus-formatted files (*.txt)
   
3. write_persistence.py
   It computes persistence diagrams.
   Input data: write_perseus.py output files
   Output data: csv files for each dimension computed; each file contains births and deaths of a persistence diagram given separate in two columns.
   (*.csv)

4. write_images.py
   Creates the persistence diagram plot.
   Input: write_persistence.py output files
   Output: persistence diagram in all dimensions (*.png)
   
5. images+PD_horiz.py
   creates a video where every frame puts together, in a horizontal position, a grey-scale image and its corresponding persistence diagram.
   Input: write_images.py and write_PDimages.py output files
   Output: a single video (*.mp4)
   
6. norm_persistence.py
   Compute the p-norm of each persistence diagram.
   Input: write_persistence.py output data
   Output: a single csv file (for each dimension computed in persistece) containing the p-norm of each peristence diagram
   
7. Wasserstein_distance.py
   Compute the p-norm of each persistence diagram.
   Input: write_persistence.py output data
   Output: a single csv file (for each dimension computed in persistence) containing the p-Warssestein distance matrix. 
