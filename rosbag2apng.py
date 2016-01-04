#!/usr/bin/python2

"""rosbag2apng.

Usage:
  rosbag2apng.py -b BAG -t TOPIC [-o OUT] [-d DELAY] [-s SKIP] [--sx SCALEX] [--sy SCALEY]
  rosbag2apng.py (-h | --help)

Options:
  -h --help     Show this screen.
  -b BAG        specify input rosbag file
  -t TOPIC      specify topic 
  -o OUT        specify output file name [default: ./rosbag.png]
  -d DELAY      specify animated png delay between each frame
  -s SKIP       skip SKIP frame after each written frame [default: 0]
  --sx SCALEX    scale the image width to SCALEX pixel
  --sy SCALEY    scale the image width to SCALEY pixel
  
"""

from docopt import docopt

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpngw
import cv2

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    BAG = arguments['-b']
    print("Opening {} ...".format(BAG))
    bag = rosbag.Bag(BAG, 'r')
    print("bag file opened")
    to_skip=0
    SKIP = int(arguments['-s'])
    bridge = CvBridge()
    images=[]
    max_frame = 2
    scale = arguments['--sx'] and arguments['--sy']
    added_image_n = 0
    if scale:
        scalex, scaley = int(arguments['--sx']), int(arguments['--sy'])
    for topic, msg, t in bag.read_messages(topics=[arguments['-t']]):
        if to_skip > 0:
            to_skip -= 1
            continue
        if SKIP > 0:
            to_skip = SKIP
        cv_image = bridge.imgmsg_to_cv2(msg)
        if scale:
            cv_image = cv2.resize(cv_image, (scalex, scaley))
        images.append(cv_image)
        max_frame -= 1
        added_image_n += 1
        print ("added image {}".format(added_image_n))
        # if max_frame <= 0:
            # break
    OUT = arguments['-o']
    print ("bag finished, writing to {}".format(OUT))
    numpngw.write_apng(OUT, images, delay=arguments['-d'], use_palette=True)
    bag.close()
