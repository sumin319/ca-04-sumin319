__author__ = "Shishir Shah"
__version__ = "1.0.0"
__copyright__ = "Copyright 2022 by Shishir Shah, Quantitative Imaging Laboratory (QIL), Department of Computer  \
                Science, University of Houston.  All rights reserved.  This software is property of the QIL, and  \
                should not be distributed, reproduced, or shared online, without the permission of the author."


import sys
from imageops.DSImage import MyImage as MyImage
from dpcourse import Stack
from dpcourse import Queue
from dpcourse import LinkedList
import random
import math


class Blob:

    ''' Already defined is the constructor that initializes
    the attributes to be maintained to an identified binary
    labeled object (region) in an image.'''
    def __init__(self):
        '''This is the linked list to store all pixel positions belonging to the blob (region).'''
        self.region = LinkedList.LinkedList()
        '''This is the color assigned to be blob (region) during connected component analysis.'''
        self.color = [0, 0, 0]
        '''This is the centroid specified as x and y image coordinate for the blob (region).'''
        self.centroid_x = 0
        self.centroid_y = 0
        '''This is the total number of pixels that belong to the blob (region), 
        also considered as the area of the blob.'''
        self.size = 0
        '''This is the bounding box coordinates for the blob specified
        as [min_x, min_y, max_x, max_y].'''
        self.bbox = []
        '''This is the id or a count given to the blob considering that each blob is unique.'''
        self.id = 0

    '''Write a method that adds the pixel location given 
    as 'x_pos' and 'y_pos' to the linked list that maintains 
    a list of pixels belonging to a particular region.'''
    def add(self, x_pos, y_pos):
        self.region.add([x_pos, y_pos])
        self.centroid_x = (self.size * self.centroid_x + x_pos) / (self.size + 1)
        self.centroid_y = (self.size * self.centroid_y + y_pos) / (self.size + 1)
        self.size += 1

    '''Write a method to set the id for the blob (region) 
    given the input argument 'num'.'''
    def set_id(self, num):
        self.id = num

    '''Write a method to get the id for the blob (region).'''
    def get_id(self):
        return self.id

    '''Write a method to set the color for the blob (region) 
    such that it can be used to generate a blob image.'''
    def set_color(self, color):
        self.color = color

    '''Write a method to get the color for the blob (region) 
    such that it can be used to generate a blob image.'''
    def get_color(self):
        return self.color

    def set_central_moments(self):
        m01 = m10 = m11 = m02 = m20 = m12 = m21 = m03 = m30 = 0
        mu11 = mu02 = mu20 = mu12 = mu21 = mu03 = mu30 = 0
        for pos in self.region:
            val = pos.get_data()
            x = val[0]
            y = val[1]
            m01 = m01 + y*255
            m10 = m10 + x*255
            m11 = m11 + x*y*255
            m02 = m02 + y*y*255
            m20 = m20 + x*x*255
            m12 = m12 + x*(y*y)*255
            m21 = m21 + (x*x)*y*255
            m03 = m03 + x*x*x*255
            m30 = m30 + y*y*y*255
            # central moments
            mu11 = mu11 + (x - self.mean_x) * (y - self.mean_y) * 255
            mu02 = mu02 + (y - self.mean_y) ** 2 * 255
            mu20 = mu20 + (x - self.mean_x) ** 2 * 255
            mu12 = mu12 + (x - self.mean_x) * (y - self.mean_y) ** 2 * 255
            mu21 = mu21 + (x - self.mean_x) ** 2 * (y - self.mean_y) * 255
            mu03 = mu03 + (y - self.mean_y) ** 3 * 255
            mu30 = mu30 + (x - self.mean_x) ** 3 * 255


        print(m10/(self.size*255), m01/(self.size*255), self.mean_x, self.mean_y, mu11, mu02, mu20, mu12, mu21, mu03, mu30)
        print(0.5*math.atan((2*(m11/self.size) - self.mean_y*self.mean_x) / ((m20/self.size - self.mean_x*self.mean_x) - (m02/self.size - self.mean_y*self.mean_y))))
        # central moments
        # moments['mu01']= sum((y-moments['mean_y'])*image) # should be 0
        # moments['mu10']= sum((x-moments['mean_x'])*image) # should be 0

        return

    '''Write a method to return the centroid of the blob (region).'''
    def get_centroid(self):
        return [self.centroid_x, self.centroid_y]

    '''Write a method to return the size (area) of the blob (region).'''
    def get_size(self):
        return self.size

    '''Write a method to set the bounding box of the blob (region).
    The bounding box should be specified as the upper left coordinates (min_x, min_y)
    and the lower right coordinates (max_x, max_y) that surrounds the blob (region).'''
    def set_bbox(self):
        if self.size == 0:
            return

        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")
        for pos in self.region:
            val = pos.get_data()
            if val[0] < min_x:
                min_x = val[0]
            if val[1] < min_y:
                min_y = val[1]
                # Set max coords
            if val[0] > max_x:
                max_x = val[0]
            elif val[1] > max_y:
                max_y = val[1]
        if self.size == 1:
            min_x = min_x - 1
            min_y = min_y - 1
            max_x = min_x + 2
            max_y = min_y + 2
        else:
            min_x = min_x - 1
            min_y = min_y - 1
            max_x = max_x + 1
            max_y = max_y + 1
        self.bbox = [min_x, min_y, max_x, max_y]
        return

    '''Write method to return the bounding box of the blob (region).'''
    def get_bbox(self):
        if len(self.bbox) == 0:
            self.set_bbox()
        return self.bbox

    def print_blob(self):
        print(self.region)
        return


class RegionAnalysis:

    def __init__(self, image):
        try:
            if not isinstance(image,MyImage):
                raise TypeError
        except TypeError:
            print('Image has to be type MyImage.')
            sys.exit(2)
        try:
            if image.get_channels() != 1:
                raise TypeError
        except TypeError:
            print("Image has to be binary image.")
            sys.exit(2)
        self.binary_image = image
        self.height = image.get_height()
        self.width = image.get_width()
        self.label_image = MyImage()
        self.label_image.new_image(self.width, self.height, [0, 0, 0])
        self.num_regions = 0

        '''The following attributes enhance the class implemented in CA-02.'''

        '''This is the linked list of all blobs (regions) in the image after 
        completing connected component analysis.'''
        self.regions = LinkedList.LinkedList()
        '''This is the blob image that would show blobs (regions) of interest.'''
        self.blob_image = MyImage()
        '''This is the initiated blob image, with all pixels being black.'''
        self.blob_image.new_image(self.width, self.height, [0, 0, 0])
        '''This is the total number of blobs (regions) of interest.'''
        self.num_blobs = 0

    '''This method generates a random trichromat value as a list to be used
    in assigning a color value.'''
    def __generate_random_labelvalue(self):
        a = random.randint(1, 255)
        b = random.randint(1, 255)
        c = random.randint(1, 255)
        return [a, b, c]

    '''This method returns the binary image generated as a 
    result of the thresholding operation.'''
    def get_binary_image(self):
        return self.binary_image

    '''This method returns the image with all identified regions such that
    each groups of pixels identified as belong to a region are assigned the 
    same color value.'''
    def get_label_image(self):
        return self.label_image

    '''This method returns the total number of regions resulting from connected
    component analysis.'''
    def get_num_regions(self):
        return self.num_regions

    '''This method performs connected component analysis on the binary image
    using the Stack data structure. This method will need to be modified to accept
    the return value from the modified floodfill method and to add generated blob (region)
    to the linked list that stores all blobs (self.regions).'''
    def connected_components_stack(self):
        data = self.binary_image.get_image_data().copy()
        self.num_regions = 0

        for i in range(self.width):
            for j in range(self.height):
                if int(data[j, i]) == 255:
                    self.num_regions += 1
                    reg = self.__floodfill_stack(data, i, j)
                    reg.set_id(self.num_regions)
                    self.regions.add(reg)
        return

    '''This method performs connected component analysis on the binary image
    using the Queue data structure. This method will need to be modified to accept
    the return value from the modified floodfill method and to add generated blob (region)
    to the linked list that stores all blobs (self.regions).'''
    def connected_components_queue(self):
        data = self.binary_image.get_image_data().copy()
        self.num_regions = 0
        for i in range(self.width):
            for j in range(self.height):
                if int(data[j, i]) == 255:
                    self.num_regions += 1
                    reg = self.__floodfill_queue(data, i, j)
                    reg.set_id(self.num_regions)
                    self.regions.add(reg)

        return

    '''This is a private method that performs the floodfill algorithm using
    the Stack data structure.  You may need to modify this method to manage
    each identified blob (region) using the given Blob class and the 
    enhanced RegionAnalysis class. This private method should return a blob (region).'''
    def __floodfill_stack(self, temp, x, y):
        ny = [-1, -1, -1, 0, 0, 1, 1, 1]
        nx = [-1, 0, 1, -1, 1, -1, 0, 1]

        frontier = Stack.Stack()

        pixel_value = int(temp[y, x])
        # target color is same as replacement
        if pixel_value != 255:
            return

        frontier.push([x, y])
        new_blob = Blob()
        new_blob.add(x, y)
        label_value = self.__generate_random_labelvalue()
        new_blob.set_color(label_value)
        self.label_image.set_image_pixel(x, y, label_value)
        temp[y, x] = 0

        while not frontier.is_empty():
            loc = frontier.pop()
            x = loc[0]
            y = loc[1]
            for k in range(len(ny)):
                # if the adjacent pixel at position (x + nx[k], y + ny[k]) is
                # is valid and has the same color as the current pixel
                if 0 <= y + ny[k] < self.height and 0 <= x + nx[k] < self.width:
                    if int(temp[y + ny[k], x + nx[k]]) == pixel_value:
                        frontier.push([x + nx[k], y + ny[k]])
                        new_blob.add(x + nx[k], y + ny[k])
                        self.label_image.set_image_pixel(x + nx[k], y + ny[k], label_value)
                        temp[y + ny[k], x + nx[k]] = 0
        return new_blob

    '''This is a private method that performs the floodfill algorithm using
    the Queue data structure. You may need to modify this method to manage
    each identified blob (region) using the given Blob class and the 
    enhanced RegionAnalysis class.  This private method should return a blob (region).'''
    def __floodfill_queue(self, temp, x, y):
        ny = [-1, -1, -1, 0, 0, 1, 1, 1]
        nx = [-1, 0, 1, -1, 1, -1, 0, 1]

        # create a queue and enqueue starting pixel
        q = Queue.Queue()
        # get the target color
        pixel_value = int(temp[y, x])

        # target color is same as replacement
        if pixel_value != 255:
            return

        q.enqueue([x, y])
        new_blob = Blob()
        new_blob.add(x, y)
        label_value = self.__generate_random_labelvalue()
        new_blob.set_color(label_value)
        self.label_image.set_image_pixel(x, y, label_value)
        temp[y, x] = 0

        # break when the queue becomes empty
        while not q.is_empty():
            # dequeue front node and process it
            loc = q.dequeue()
            x = loc[0]
            y = loc[1]

            # process all eight adjacent pixels of the current pixel and
            # enqueue each valid pixel
            for k in range(len(ny)):
                # if the adjacent pixel at position (x + nx[k], y + ny[k]) is
                # is valid and has the same color as the current pixel
                if 0 <= y + ny[k] < self.height and 0 <= x + nx[k] < self.width:
                    if int(temp[y + ny[k], x + nx[k]]) == pixel_value:
                        q.enqueue([x + nx[k], y + ny[k]])
                        new_blob.add(x + nx[k], y + ny[k])
                        self.label_image.set_image_pixel(x + nx[k], y + ny[k], label_value)
                        temp[y + ny[k], x + nx[k]] = 0
        return new_blob

    '''Write the method that performs the selection of subset of blobs (regions) from
    all the regions identified after connected component analysis and generates the
    blob image to include those blobs (region) along with a bounding box surrounding
    each of the blobs (regions).'''
    def set_blob_image(self, size_threshold=0):
        self.num_blobs = 0
        for a_blob in self.regions:
            blob = a_blob.get_data()
            if blob.get_size() > size_threshold:
                self.num_blobs += 1
                color = blob.get_color()
                box = blob.get_bbox()
                min_x = box[0]
                min_y = box[1]
                max_x = box[2]
                max_y = box[3]
                # blob.set_central_moments()
                if min_x < 0:
                    min_x = 0
                if min_y < 0:
                    min_y = 0
                if max_x >= self.blob_image.get_width():
                    max_x = self.blob_image.get_width()-1
                if max_y >= self.blob_image.get_height():
                    max_y = self.blob_image.get_height()-1

                for values in blob.region:
                    val = values.get_data()
                    x = val[0]
                    y = val[1]
                    self.blob_image.set_image_pixel(x, y, color)
                for x in range(min_x, max_x+1):
                    self.blob_image.set_image_pixel(x, min_y, [255, 255, 255])
                    self.blob_image.set_image_pixel(x, max_y, [255, 255, 255])
                for y in range(min_y, max_y+1):
                    self.blob_image.set_image_pixel(min_x, y, [255, 255, 255])
                    self.blob_image.set_image_pixel(max_x, y, [255, 255, 255])
        return

    '''Write the method that returns the blob image.'''
    def get_blob_image(self):
        return self.blob_image

    '''Write the method that returns the total number of blobs (regions) 
    resulting from the selection/filtering operation specified to be performed.'''
    def get_num_blobs(self):
        return self.num_blobs

    def print_regions(self):
        for region in self.regions:
            print(region)
        return
