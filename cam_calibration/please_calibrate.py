# Import required modules
import cv2
import numpy as np
import os
import glob


# Define the dimensions of checkerboard
CHECKERBOARD = (6, 9)


# stop the iteration when specified
# accuracy, epsilon, is reached or
# specified number of iterations are completed.
criteria = (cv2.TERM_CRITERIA_EPS +
			cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# Vector for 3D points
threedpoints = []

# Vector for 2D points
twodpoints = []


# 3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0]
					* CHECKERBOARD[1],
					3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
							0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None


# Extracting path of individual image stored
# in a given directory. Since no path is
# specified, it will take current directory
# jpg files alone
images = glob.glob('../test_images/MicrosoftLifeCam/*.jpg')

for filename in images:
	image = cv2.imread(filename)
	grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Find the chess board corners
	# If desired number of corners are
	# found in the image then ret = true
	ret, corners = cv2.findChessboardCorners(
					grayColor, CHECKERBOARD,
					cv2.CALIB_CB_ADAPTIVE_THRESH
					+ cv2.CALIB_CB_FAST_CHECK +
					cv2.CALIB_CB_NORMALIZE_IMAGE)

	# If desired number of corners can be detected then,
	# refine the pixel coordinates and display
	# them on the images of checker board
	if ret == True:
		threedpoints.append(objectp3d)

		# Refining pixel coordinates
		# for given 2d points.
		corners2 = cv2.cornerSubPix(
			grayColor, corners, (11, 11), (-1, -1), criteria)

		twodpoints.append(corners2)

		# Draw and display the corners
		image = cv2.drawChessboardCorners(image,
										CHECKERBOARD,
										corners2, ret)

	cv2.imshow('img', image)
	cv2.waitKey(0)

cv2.destroyAllWindows()

h, w = image.shape[:2]


# Perform camera calibration by
# passing the value of above found out 3D points (threedpoints)
# and its corresponding pixel coordinates of the
# detected corners (twodpoints)
ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
	threedpoints, twodpoints, grayColor.shape[::-1], None, None)




#####################################
#####################################
#####################################
#####################################
#####################################


print('#####################################')
print('## Copy to config/camera_info.yaml')
print('#####################################')

# Displaying required output for camera matrix
print("camera_matrix:")
listmatrix = np.asarray(matrix).tolist()
print(f'  cols: {len(listmatrix[0])}')
print('  data:')
for m in listmatrix:
    for p in m:
        print(f'  - {p}')
print(f'  rows: {len(listmatrix)}')


# Displaying required output for distortion coefficients
print("distortion_coefficients:")
listdist = np.asarray(distortion).tolist()
print(f'  cols: {len(listdist[0])}')
print('  data:')
for m in listdist:
    for p in m:
        print(f'  - {p}')
print(f'  rows: {len(listdist)}')


# Displaying required output for image dimensions
print(f'image_height: {h}')
print(f'image_width: {w}')




#print("\n Rotation Vectors:")
#print(r_vecs)
#print("\n Translation Vectors:")
#print(t_vecs)
print('\n\n\n\n')


print('#####################################')
print('## Copy to config/usb_cam_params.yaml')
print('#####################################')

camera_name = 'bob'
video_device = '/dev/video3'

print(f'''/**:
  ros__parameters:
    auto_white_balance: true
    autoexposure: true
    autofocus: false
    av_device_format: YUV422P
    brightness: -1
    camera_info_url: package://cam_calibration/config/camera_info.yaml
    camera_name: {camera_name}
    contrast: -1
    exposure: 100
    focus: -1
    frame_id: camera
    framerate: 30.0
    gain: -1
    image_height: {h}
    image_width: {w}
    io_method: mmap
    pixel_format: mjpeg2rgb
    saturation: -1
    sharpness: -1
    video_device: {video_device}
    white_balance: 4000''')


print('#####################################')
print('## Test with:')
print('ros2 run usb_cam usb_cam_node_exe --ros-args --params-file usb_cam_params.yaml')
print('#####################################')

