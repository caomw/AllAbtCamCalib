#include <stdio.h>
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <cstdio>
#include <stdio.h>
#include <stdlib.h>
#include <cstdlib>
#include <sys/types.h>
#include <dirent.h>
#include <string>
#include <stdarg.h>
#include <cv.h>
#include <highgui.h>
#include <fstream>
#include <map>
#include <string.h>
struct TreeNode{
	TreeNode * left_node;
	TreeNode * right_node;
	int val; //swtich to * Data if you want
};

struct Chessboard {
	TreeNode * lookup_table;
	double height;	 //phyiscal height
	double rows; // # of rows
	double cols; // # of cols
        double width;

	Chessboard(double r, double c, double x, double y):rows(r),cols(c),width(x), height(y){}
};

struct Intrinsic {
	//Intrinsics.. focus_X, focus_Y, pptx, ppty
	double focus_x, focus_y, pptx, ppty;
	Intrinsic(double f_x, double f_y, double p_x, double p_y):focus_x(f_x), focus_y(f_y),
	pptx(p_x), ppty(p_y){}
};

struct Extrinsic {
	// all in CV rouguious form
	cv::Mat  Rot, Trans;
	Extrinsic(cv::Mat r, cv::Mat t): Rot(r), Trans(t){}
};

class AppleJuice{
	private:
		Chessboard chessboard;
		std::vector<std::vector<cv::Mat>> ImageLists;
		std::vector<std::vector<cv::Mat>> BinaryImages;
		std::vector<std::vector<cv::Point2f>> FeaturePool;
		std::vector<std::vector<cv::Point3f>> PatternPtsPool;
		cv::Point3f SearchPoints(std::string s);
		Intrinsic intrinsic;

	public:
		//read lookup table from txt 
		// 	>> Chessboard struct
		void ReadLookup_table();
		//read image from DIR 
		//	>> ImageLists
		void ReadImageLists();
		//Biinarize all images 
		//	>> BinaryImages
		void BinarizeAllImages();
		//Extract all control pts 
		//	>> FeaturePools & PatternPtsPool 
		void ExtractControlPts();
		//Get Init. Guess from standart OpenCV Camera Calibration
		//	>> Intrisics >> Extrinsic
		void InitCameraCalibration();
		// Full BundleAdjustment
		//  >> ???
		void AppleBundleAdjustment();

		void ComputeReprojectionError();

		void ExportResults();
			
		


};
