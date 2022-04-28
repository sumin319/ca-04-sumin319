__author__ = "Shishir Shah"
__version__ = "1.0.0"
__copyright__ = "Copyright 2022 by Shishir Shah, Quantitative Imaging Laboratory (QIL), Department of Computer  \
                Science, University of Houston.  All rights reserved.  This software is property of the QIL, and  \
                should not be distributed, reproduced, or shared online, without the permission of the author."


from dpcourse import HashTable
from imageops import DSImage
import numpy, math
import os


class ImageSearch:
    def __init__(self, size):
        '''This is the list data structure to be created for storing
        representations of images in the search directory'''
        self.search_index = None

        '''This is a scaling parameter in case the list size is 
        to be limited independent of the number of images in the search directory'''
        self.search_index_scaling = 1

        '''This is the hashtable data structure to be created for storing 
        representations of images in the search directory'''
        self.search_index_hashing = None

        '''This is the size of the hashtable to be generated'''
        self.search_index_hash_size = size

        '''This is the path of the search directory'''
        self.search_location = None

        '''This is the class for associating the query image'''
        self.query_image = DSImage.MyImage()

        '''This is the parameters of the resized image before the image
        representation is computed.  These are set default values and should not be changed'''
        self.image_resize_width = 9
        self.image_resize_height = 8

    '''Method to set the image search directory'''
    def set_search_location(self, directory):
        self.search_location = directory

    '''Method to get the image search directory'''
    def get_search_location(self):
        return self.search_location

    '''Method to get the list data structure'''
    def get_search_index(self):
        return self.search_index

    '''Method to get the hashtable data structure'''
    def get_search_index_hash(self):
        return self.search_index_hashing

    '''Write the method that takes the query image name as the argument
    and performs the necessary steps to find a match in the hashtable data structure
    and returns the name of the matched image'''
    def find_match_in_hash(self, query_image_name):
        pass

    '''Write the method that takes the query image name as the argument
    and performs the necessary steps to find a match in the list data structure
    and returns the name of the matched image'''
    def find_match_in_list(self, query_image_name):
        pass

    '''Write a method that reads number of files specified in the argument
    from the image search directory, creates the hashtable data structure, computes the 
    image representation for each image, and stores the necessary data in the data structure'''
    def create_search_index_hash(self, images=0):
        pass

    '''Write a method that reads number of files specified in the argument
    from the image search directory, creates the list data structure, computes the 
    image representation for each image, and stores the necessary data in the data structure'''
    def create_search_index(self, images=0):
        pass

    def __difference_hash(self, image, original_width, original_height):
        data = image.get_image_data().copy()
        new_data = self.__resize_linear(data, original_width, original_height, self.image_resize_width, self.image_resize_height)
        diff = new_data[:, 1:] > new_data[:, :-1]
        diff = diff*1
        h = sum([2 ** (i % 8) for (i, v) in enumerate(diff.flatten()) if v])
        return [int(numpy.array(h, dtype="float64")), diff.flatten()]

    def __resize_linear(self, matrix, original_width, original_height, new_width, new_height):
        """Perform a pure-numpy linear-resampled resize of an image."""
        output_image = numpy.zeros((new_height, new_width), dtype=numpy.uint8)
        inv_scale_factor_y = original_height / new_height
        inv_scale_factor_x = original_width / new_width

        for new_y in range(new_height):
            for new_x in range(new_width):
                # If you had a color image, you could repeat this with all channels here.
                # Find sub-pixels data:
                old_x = new_x * inv_scale_factor_x
                old_y = new_y * inv_scale_factor_y
                x_fraction = old_x - math.floor(old_x)
                y_fraction = old_y - math.floor(old_y)

                # Sample four neighboring pixels:
                left_upper = matrix[math.floor(old_y), math.floor(old_x)]
                right_upper = matrix[math.floor(old_y), min(matrix.shape[1] - 1, math.ceil(old_x))]
                left_lower = matrix[min(matrix.shape[0] - 1, math.ceil(old_y)), math.floor(old_x)]
                right_lower = matrix[
                    min(matrix.shape[0] - 1, math.ceil(old_y)), min(matrix.shape[1] - 1, math.ceil(old_x))]

                # Interpolate horizontally:
                blend_top = (right_upper * x_fraction) + (left_upper * (1.0 - x_fraction))
                blend_bottom = (right_lower * x_fraction) + (left_lower * (1.0 - x_fraction))
                # Interpolate vertically:
                final_blend = (blend_top * y_fraction) + (blend_bottom * (1.0 - y_fraction))
                output_image[new_y, new_x] = final_blend

        return output_image

    def __hamming(self, a, b):
        # compute and return the Hamming distance between the integers
        sum = 0
        for i in range(len(a)):
            sum += (a[i] ^ b[i])
        return sum