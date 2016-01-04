# rosbag2apng

This script takes a sensor_msgs.Image topic from a **rosbag** file and generates an animated **PNG** that can be read by most browsers. 

This can be useful when you want to generate a preview of the contents inside the rosbag file

## Example: 

```bash
rosbag2apng.py -b input.bag -t '/stereo/left/image_raw' -s 100 --sx 480 --sy 320
```

The above command will read the */stereo/left/image_raw'* topic from *input.bag*, take an image every **100** frames and write an animated 480x320px png 

