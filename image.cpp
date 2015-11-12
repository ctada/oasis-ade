#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/core/core.hpp"

using namespace std;
using namespace cv;

int main()
{
Mat image;

image = imread("4tube720x720.jpg",1);
if(image.empty())
{
cout << "Could not open or find the image" << std::endl ;
return -1;
}


namedWindow("Image", CV_WINDOW_AUTOSIZE );
imshow("Image", image);

///
   // get the image data
 int height = image.rows;
 int width = image.cols;

 printf("Processing a %dx%d image\n",height,width);

cv :: Size smallSize ( 110 , 70 );

std :: vector < Mat > smallImages ;
namedWindow("smallImages ", CV_WINDOW_AUTOSIZE );

for  ( int y =  0 ; y < image . rows ; y += smallSize . height )
{
    for  ( int x =  0 ; x < image . cols ; x += smallSize . width )
    {
        cv :: Rect rect =   cv :: Rect ( x , y , smallSize . width , smallSize . height );
        smallImages . push_back ( cv :: Mat ( image , rect ));
        imshow ( "smallImages", cv::Mat ( image, rect ));
        waitKey(0);
    }
}


return 0;
}