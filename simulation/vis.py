"""
For visualizing calibration targets, cameras, etc.
"""
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import axes3d

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.backends.backend_pdf import PdfPages

import numpy as np
import exp_util as util

def plot_calib_boards(boards, board_dim):
	"""
	Plots a board in 3D

	Args:
		boards: a list of dictionaries, where each dictionary is a board
		board_dim: (board_height, board_width)
	"""
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	clist = colors.cnames.keys()

	for i in xrange(len(boards)):
		board = boards[i]
		X, Y, Z = util.board_dict2array(board, board_dim)
		ax.plot_wireframe(X, Y, Z, color=clist[i])
		#print X[0,0], Y[0,0], Z[0,0]
	plt.show()

def compare_board_estimations(esti_extrinsics, board, board_dim, \
								actual_boards, save_name=None):
	"""
	Plots true and estimated boards on the same figure
	@TODO: Doesn't save figure. Can 3D figure be saved?
	Args:
		esti_extrinsics: dictionary, keyed by image number, values are Extrinsics
		board:
		board_dim: (board_height, board_width)
		actual_boards: list of dictionaries
		save_name: filename, string
	"""
	for i in xrange(len(actual_boards)):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		act_board = actual_boards[i]
		aX, aY, aZ = util.board_dict2array(act_board, board_dim)
		ax.plot_wireframe(aX, aY, aZ, color='b')

		if i in esti_extrinsics:
			esti_loc = esti_extrinsics[i].trans_vec
			esti_board = util.move_board(board, esti_loc)
			eX, eY, eZ = util.board_dict2array(esti_board, board_dim)
			ax.plot_wireframe(eX, eY, eZ, color='r')

		plt.show()

def plot_all_chessboards_in_camera(img_pts, img_size, save_name=None):
	if save_name:
		pp = PdfPages(save_name)

	for i in range(len(img_pts)):
		viewed_pts = np.asarray(img_pts[i].values())
		plt.axis([0, img_size[1], 0, img_size[0]])
		plt.grid(True)
		if viewed_pts.size == 0:
			print "chessboard " + str(i) + " is not seen in camera\n"
		else:
			plt.plot(viewed_pts[:,1,:], viewed_pts[:,0,:], 'ro')
		plt.ylabel('chessboard' + str(i))
		if pp:
			pp.savefig()
		else:
			plt.show()
		plt.clf()

	# Plot all points on images of whole board on the same page
	# Assuming at least one saw all points on board
	tot_pts_num = 0
	for i in range(len(img_pts)):
		if len(img_pts[i]) > tot_pts_num:
			tot_pts_num = len(img_pts[i])
	plt.axis([0, img_size[1], 0, img_size[0]])
	plt.grid(True)		
	for i in range(len(img_pts)):
		if len(img_pts[i]) == tot_pts_num:
			viewed_pts = np.asarray(img_pts[i].values())
			plt.plot(viewed_pts[:,1,:], viewed_pts[:,0,:], 'ro')
	plt.ylabel('all points used') 
	if pp:
		pp.savefig()
	else:
		plt.show()

	if pp:
		pp.close()
	else:
		plt.close('all')

def plot_camera_pose(extrin, save_name=None):
	"""
	Plots the location of the camera given extrinsics of board
	@TODO: Currently labels image number text on the location of camera, could 
	       add in the orientation and a 3D camera figure
	Args:
		extrin: a dictionary keyed by image number, whose values are Extrinsics
		save_name: if save_name is provided, figure will be saved to that name; 
		           otherwise, the figure will be shown on screen
	"""
	print 'plot_camera_pose not implemented yet!'
	pass

def write_esti_results(estimations, true_cam, save_name_pre):
	"""
	Args:
		estimations: list of Cameras from calibration results 
		true_cam: actual camera parameters
		save_name_pre: filename without .txt or .pdf extensions
	"""
	ftxt = open(save_name_pre+'.txt', 'w')
	fpdf = PdfPages(save_name_pre+'.pdf')

	# focal length x
	fx_arr = np.asarray([est_cam.intrinsics.intri_mat[0,0] for est_cam in estimations])
	print >> ftxt, 'focal length x\tground truth:{0}\testimation mean:{1}\testimation std:{2}'.format(\
		true_cam.intrinsics.intri_mat[0,0], np.mean(fx_arr), np.std(fx_arr))
	fig, ax = plt.subplots()
	bars = plt.bar(range(len(fx_arr)), fx_arr)
	plt.ylabel('focal length x') 
	fpdf.savefig()

	# focal length y
	fy_arr = np.asarray([est_cam.intrinsics.intri_mat[1,1] for est_cam in estimations])
	print >> ftxt, 'focal length y\tground truth:{0}\testimation mean:{1}\testimation std:{2}'.format(\
		true_cam.intrinsics.intri_mat[1,1], np.mean(fy_arr), np.std(fy_arr))
	fig, ax = plt.subplots()
	bars = plt.bar(range(len(fy_arr)), fy_arr)
	plt.ylabel('focal length y') 
	fpdf.savefig()

	# principal point x
	px_arr = np.asarray([est_cam.intrinsics.intri_mat[0,2] for est_cam in estimations])
	print >> ftxt, 'principal point x\tground truth:{0}\testimation mean:{1}\testimation std:{2}'.format(\
		true_cam.intrinsics.intri_mat[0,2], np.mean(px_arr), np.std(px_arr))
	fig, ax = plt.subplots()
	bars = plt.bar(range(len(px_arr)), px_arr)
	plt.ylabel('principal point x') 
	fpdf.savefig()

	# principal point y
	py_arr = np.asarray([est_cam.intrinsics.intri_mat[1,2] for est_cam in estimations])
	print >> ftxt, 'principal point y\tground truth:{0}\testimation mean:{1}\testimation std:{2}'.format(\
		true_cam.intrinsics.intri_mat[1,2], np.mean(py_arr), np.std(py_arr))
	fig, ax = plt.subplots()
	bars = plt.bar(range(len(py_arr)), py_arr)
	plt.ylabel('principal point y') 
	fpdf.savefig()

	# extrinsics diff r1
	# extrinsics diff r2
	# extrinsics diff r3
	# extrinsics diff t1
	# extrinsics diff t2
	# extrinsics diff t3

	ftxt.close()
	fpdf.close()
	
	print 'write_esti_results not FULLY implemented yet!'
	
def plot_directions(orientations, location=np.asarray([0,0,0])):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for orient in orientations:
		ax.quiver(location[0], location[1], location[2], \
			orient[0], orient[1], orient[2], pivot='tail')
	ax.set_xlim(-1,1)
	ax.set_ylim(-1,1)
	ax.set_zlim(-1,1)
	plt.show()

