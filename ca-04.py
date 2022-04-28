"""ca-04.py: Starter file to run homework 4"""

__author__ = "Shishir Shah"
__version__ = "1.0.0"
__copyright__ = "Copyright 2022 by Shishir Shah, Quantitative Imaging Laboratory (QIL), Department of Computer  \
                Science, University of Houston.  All rights reserved.  This software is property of the QIL, and  \
                should not be distributed, reproduced, or shared online, without the permission of the author."


import sys
import matplotlib.pyplot as plt

from imageops import DSImage as DSImage
from imageops import ImageSearch as ImageSearch
import logging
import time


def image_display(image):
    if image.get_channels() == 3:
        plt.imshow(image.get_image_data())
        plt.axis('off')
        plt.show()
    else:
        plt.imshow(image.get_image_data(), cmap='gray', vmin=0, vmax=255)
        plt.axis('off')
        plt.show()
    return


def main():
    """ The main function that parses input arguments, calls the appropriate
     method and writes the output image"""

    # Initialize logging
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"

    logging.basicConfig(filename="output/logfile.log",
                        filemode="w",
                        format=Log_Format,
                        level=logging.INFO)
    logger = logging.getLogger()
    logger.info('Logging initialized.')

    # Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-q", "--query_image", dest="query_image",
                        help="specify the name of the query image", metavar="QUERY_IMAGE")

    parser.add_argument("-s", "--image_dataset", dest="image_dataset",
                        help="specify the name of the image dataset directory to search", metavar="IMAGE_DATASET")

    parser.add_argument("-m", "--method", dest="method",
                        help="specify the use of List or Hashtable for indexing and search", metavar="METHOD")

    parser.add_argument("-n", "--number_of_images", dest="number_of_images",
                        help="specify the number of image to include from image dataset", metavar="NUMBER_OF_IMAGES")

    parser.add_argument("-d", "--display", dest="display",
                        help="specify if images should be displayed", metavar="DISPLAY")

    args = parser.parse_args()

    # Load query image
    if args.query_image is None:
        print("Please specify the name of query image")
        print("use the -h option to see usage information")
        logger.error('Query image file name not specified.')
        sys.exit(2)
    if args.image_dataset is None:
        print("Please specify the name of directory with image dataset to search")
        print("use the -h option to see usage information")
        logger.error('Image dataset directory not specified.')
        sys.exit(2)
    if args.method is None:
        print("Please specify the use of List or Hashtable for indexing and search")
        print("use the -h option to see usage information")
        logger.error('Method not specified.')
        sys.exit(2)
    if args.display is None or int(args.display) > 1:
        print("Please specify if images should be displayed or now")
        print("use the -h option to see usage information")
        logger.error('Image display option not correctly specified.')
        sys.exit(2)
    else:
        # set parameters for processing both query image and images in the search directory
        display = int(args.display)
        outputDir = 'output/'
        imagesearchDir = args.image_dataset
        search_method = args.method
        print('Query Image: ' + args.query_image)
        print('Image Search Directory: ' + imagesearchDir)
        print('Indexing and Search Method: ' + search_method)

        logger.info('Query Image: ' + args.query_image)
        logger.info('Image Search Directory: ' + imagesearchDir)
        logger.info('Indexing and Search Method: ' + search_method)

        if args.number_of_images is None:
            log_string = 'Number of images from search directory: All'
        else:
            log_string = 'Number of images from search directory: ' + args.number_of_images
        print(log_string)
        logger.info(log_string)

        log_string = 'Indexing search images...'
        print(log_string)
        logger.info(log_string)

        # Compute image representation and generate indexing using List or Hashtable as per the selected method
        s = ImageSearch.ImageSearch(29)
        s.set_search_location(imagesearchDir)
        if args.number_of_images is None:

            if search_method == 'List':
                start = time.time()
                s.create_search_index()
                end = time.time()
                log_string = 'Time taken to create searchable list: ' + str(end-start)

            if search_method == 'Hashtable':
                start = time.time()
                s.create_search_index_hash()
                end = time.time()
                log_string = 'Time taken to create searchable hash: ' + str(end-start)

            print(log_string)
            logger.info(log_string)

        else:

            if search_method == 'List':
                start = time.time()
                s.create_search_index(int(args.number_of_images))
                end = time.time()
                log_string = 'Time taken to create searchable list for ' + args.number_of_images + ': ' + str(end-start)

            if search_method == 'Hashtable':
                start = time.time()
                s.create_search_index_hash(int(args.number_of_images))
                end = time.time()
                log_string = 'Time taken to create searchable hash for ' + args.number_of_images + ': ' + str(end-start)

            print(log_string)
            logger.info(log_string)

        # Perform the search in List or Hashtable as per the selected method
        log_string = 'Searching match for query image...'
        print(log_string)
        logger.info(log_string)

        if search_method == 'List':
            start = time.time()
            matched_image_name = s.find_match_in_list(args.query_image)
            end = time.time()
            log_string = 'Time taken to match query image in searchable list: ' + str(end-start)

        if search_method == 'Hashtable':
            start = time.time()
            matched_image_name = s.find_match_in_hash(args.query_image)
            end = time.time()
            log_string = 'Time taken to match query image in searchable hash: ' + str(end-start)

        print(log_string)
        logger.info(log_string)
        if matched_image_name is not None:
            log_string = 'Matched image: ' + matched_image_name
        else:
            log_string = 'Matched image: None'
        print(log_string)
        logger.info(log_string)

        if display:
            myimage = DSImage.MyImage()
            myimage.load_image(args.query_image)
            image_display(myimage)
            print('Displaying Query Image')
            if matched_image_name is not None:
                myimage.load_image(matched_image_name)
                image_display(myimage)
                print('Displaying Matched Image')


if __name__ == "__main__":
    main()
