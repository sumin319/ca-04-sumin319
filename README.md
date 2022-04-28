# COSC 2306 - Data Programming 
## Assignment - 4 ##

### Due Date: May 1, 11:59 PM ###

#### The goal of this assignment is to use list and hashtable for the image search task. ####

The goal of this assignment is to use and evaluate lists and hashtable for the task of image matching.  Image matching is
a common problem where the task is to search over a collection of images to find an image similar to the query image.  This task
typically requires the following steps:
1. For each image in the collection of images, compute an image representation that can be stored in a data structure
2. For the query image, compute the image representation and search the stored representations to find a match

The focus of this assignment is on the use of data structure for storing the representation and any additional information 
to facilitate the search and matching.  You will explore the use of ``list`` and ``hashtable`` and compare the two in facilitating
search.  You are provided implemented class for the ``hashtable`` data structure in the file **dpcourse/HashTable.py**.  In addition,
you are also provided a skeleton implementation of the image search class in the file **imageops/ImageSearch.py**.  Several methods of
the class are also already implemented.  Since the focus of this assignment is on data structure for store and search, methods necessary
for generating the image representation are already implemented.  The primary method to be used is **__difference_hash()**, which takes
as argument the input image and its width and height and returns as a list a representation key and a 64 dimensional binary array.

In this assignment, you will implement 4 key methods:
a. **create_search_index()** - create a list data structure to store the image representation, associated binary array, and the image file name
b. **create_search_index_hash** - create a hashtable data structure to store the image representation, associated binary array, and the image file name
c. **find_match_in_list()** - search the list data structure match the query image
d. **find_match_in_hash()** - search the hashtable data structure match the query image

The logical steps necessary in the 2 methods for creating the data structure are:
1. Initialize the data structure
2. Read image files from the search directory specified by the main program
3. For each image
   1. convert to gray scale if the image is color
   2. compute the image representation (**__difference_hash()**)
   3. store the representation along with name of the read image

The logical steps necessary in the 2 methods for searching the data structure to match the query image are:
1. Read query image
2. Convert to gray scale if the image is color
3. Compute the image representation (**__difference_hash()**)
4. Search the data structure to find match based on the image representation
5. If the match includes more than one image:
   1. compute hamming distance between the binary array of the query image and that of each matched image (**__hamming()**)
   2. select the best match as the one that has the lowest hamming distance
6. Return the matched image

You are given the driver program (ca-04.py) that calls methods to create the data structure for storing representations of images in the
search directory and then performing the match in the created data structure using the query image.   
Once you finish writing your methods, the driver program will perform the image search task and return the matched image to the input query image. 
The driver program will also report the time taken to perform the search.  Please compare the obtained results, both
for the obtained image match and the time to perform the search and comment on your observations pertaining
to the use of ``list`` and ``hashtable`` as the data structures for this task.

**Note:**

**PLEASE READ CAREFULLY ALL COMMENTS ASSOCIATED WITH EACH SKELETON METHODS TO BE IMPLEMENTED**

**Do not use any in-built functions or external modules/libraries for image operations (E.g: PIL).** In general, you can use function from numpy, math, and os library. <br/>
   
  - Please do not change the code structure.
  - Usage:
        - python ca-04.py -q <query-image-name-with-full-path> -s <image-search-directory> -m <List or Hashtable> -n <number of images to be used (optional)> -d 0
        - Example: python ca-04.py -q Images/queries/105410.ppm -s Images/search -m List -d 0
  - Please make sure the code runs when you run the above command from prompt/terminal
  - All the output images and files are saved to "output/" folder
  - You can set the value of -d to 1 if you would like to display images so you can verify the result
  - In this case, the example usage would be:
  
        - Example: python ca-04.py -q Images/queries/103100.ppm -s Images/search -m Hashtbale -d 1

To check your results, for the above usage with the specified input query image and the image search directory, the resulting match image should be **Images/search/103900.ppm**.
Several images are provided for testing in the folder Images/queries<br>

**PS. Please do not change: ca-04.py, dpcourse/HashTable.py, dpcourse/LinkedList.py, dpcourse/Stack.py, dpcourse/Queue.py, imagesops/DSImage.py, requirements.txt, and Jenkinsfile.**

-----------------------

<sub><sup>
License: Property of Quantitative Imaging Laboratory (QIL), Department of Computer Science, University of Houston. This software is property of the QIL, and should not be distributed, reproduced, or shared online, without the permission of the author This software is intended to be used by students of the Data Programming course offered at University of Houston. The contents are not to be reproduced and shared with anyone with out the permission of the author. The contents are not to be posted on any online public hosting websites without the permission of the author. The software is cloned and is available to the students for the duration of the course. At the end of the semester, the Github organization is reset and hence all the existing repositories are reset/deleted, to accommodate the next batch of students.
</sub></sup>
