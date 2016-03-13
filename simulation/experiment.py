"""
Runs experiment on calibration.
"""

import exp_util as util
import camera as cam

"""
Functions for running experiment and analyzing experiment results.
"""

# def rotate_to_match_corners(board, true_cam, cam_loc, detection_noise):
# 	"""
# 	Rotate camera to capture images that matches the four corners of chessboard to
#     four corners of the camera
#     Return a list of points seen in different images captured.
# 	"""
# 	# @TODO
# 	return None, None

def target_at_layered_grids(nlayer, grid_size, aov, board):
	"""
	Simulates the situation of a static camera, while the calibration target 
	appears on several planes of different depth to the camera.
	TODO: Assumes camera position at (0,0,0;0,0,1) for now, could be changed to 
	other positions later.

	Args:
		nlayer: positive integer, number of depth layered_grids
		grid_size: tuple of two positive integer, (grid_height, grid_width)
		fov: tuple of two positive number, (aov_vertical, aov_horizontal), 
		     representing camera angle of view angle in degrees
		board: calibration target to be used with, generated by 
			   util.gen_calib_board
	Returns:
		A list of dictionaries (boards), representing the 3D locations of the 
		calibration target control points. 
	"""

	#@TODO
	pass

"""
Running the experiment.
"""
noise3d_lvls = [0, 0.5, 1, 2]
noise2d_lvls = [0, 0.5, 1, 2]
board_height = 5
board_width = 7
board_sqsize = 23
board_location = [0,0,0]
board_orientation = [0,0,0]


true_cam = cam.Camera.make_pinhole_camera()
print true_cam
cam_loc = cam.Extrinsics.init_with_numbers(0,0,0,0,0,1) #TODO: input numbers
for noise3d in noise3d_lvls:
	for noise2d in noise2d_lvls:

		print "Experiment with target noise:(mm)", noise3d, "detection noise:(pxl)", noise2d
		board = util.gen_calib_board(board_height, board_width, board_sqsize, \
			board_location, board_orientation, noise3d)

		# Move the calibration target on different grid layers
		layered_grids = target_at_layered_grids(3, (5, 7), true_cam.aov, board)
		img_pts = true_cam.capture_images(layered_grids)

		# Estimate camera parameters from captured images
		esti_cam = cam.Camera.calibrate_camera(img_pts, board, true_cam.size)

		# Analyze error
		diff = util.compute_estimation_diff(esti_cam, \
										true_cam, cam_loc)
print "experiment DONE"
