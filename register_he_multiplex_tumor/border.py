#import openslide;
import os;
import cv2 as cv;
import numpy as np;
import json;
import skimage.io as io;

RESIZE_FACTOR = 50
# Number of features to extract
# The wsi patch is assumed to be larger than the reference patch and so the number of features extracted is larger
# Number of features to extract from the reference patch
MAX_FEATURES_1 = 5000;
# Number of features to extract from the wsi patch
MAX_FEATURES_2 = 5000;
# percent of top matched features to use
#GOOD_MATCH_PERCENT = 0.01
GOOD_MATCH_PERCENT = 0.05
# matching similarity constraints
 

def register_single(multi_filepath, he_filepath, he_tumor_filepath, tumor_mask_filepath, out_dir):
    src_filepath = multi_filepath;
    target_filepath = he_filepath;
    target_filepath2 = he_tumor_filepath;
    mask_filepath = tumor_mask_filepath;
    print('src_filepath = ', src_filepath)
    print('target_filepath = ', target_filepath)
    print('target_filepath2 = ', target_filepath2)
    print('mask_filepath = ', mask_filepath)

    # ORB features
    # Initiate ORB detector
    orb1 = cv.ORB_create(MAX_FEATURES_1)
    orb2 = cv.ORB_create(MAX_FEATURES_2)

    # read ref patch
    img1 = cv.imread(src_filepath,0) 
    # find the keypoints with ORB
    kp1, descriptors1 = orb1.detectAndCompute(img1,None)
    # draw only keypoints location,not size and orientation
    #img1_feat = cv.drawKeypoints(img1, kp1, None, color=(0,255,0), flags=0)

    found = False;
    img2 = cv.imread(target_filepath,0) 
    kp2, descriptors2 = orb2.detectAndCompute(img2,None)

    # Match features
    matcher = cv.DescriptorMatcher_create(cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)
    print('matches len = ', len(matches))

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)
 
    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]
    print('matches[0].distance = ', matches[0].distance)
    print('matches[-1].distance = ', matches[-1].distance)

    ## Draw top matches
    #imMatches = cv.drawMatches(img1, kp1, img2, kp2, matches, None)
    #cv.imwrite(os.path.join(out_dir, "matches.jpg"), imMatches);

    #if(matches[0].distance > MATCH_MIN_DIST or matches[-1].distance > MATCH_MAX_DIST):
    #    print('')
    #    print('No match found')
    #    return;

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
 
    for i, match in enumerate(matches):
        points1[i, :] = kp1[match.queryIdx].pt
        points2[i, :] = kp2[match.trainIdx].pt
   
    # Find homography
    h, mask = cv.findHomography(points2, points1, cv.RANSAC)
 
    # Use homography
    img2 = cv.imread(target_filepath,1)    
    img1 = cv.imread(src_filepath,1) 
    height, width,channels = img1.shape
    img2Reg = cv.warpPerspective(img2, h, (width, height))
    filename = os.path.splitext(os.path.split(src_filepath)[1])[0];
    ext = os.path.splitext(target_filepath)[1];
    cv.imwrite(os.path.join(out_dir, filename + '_he_registered'+ext), img2Reg)

    if(target_filepath2 is not None):
        img3 = cv.imread(target_filepath2,1)    
        img3Reg = cv.warpPerspective(img3, h, (width, height))
        #filename = os.path.splitext(os.path.split(src_filepath)[1])[0];
        #ext = os.path.splitext(target_filepath)[1];
        cv.imwrite(os.path.join(out_dir, filename + '_he_tumor_registered'+ext), img3Reg)

    if(mask_filepath is not None):
        img3 = cv.imread(mask_filepath,1)    
        img3Reg = cv.warpPerspective(img3, h, (width, height))
        #filename = os.path.splitext(os.path.split(src_filepath)[1])[0];
        #ext = os.path.splitext(target_filepath)[1];
        cv.imwrite(os.path.join(out_dir, filename + '_tumor_mask_registered'+ext), img3Reg)

        alpha = 0.9;
        img4 = img1 * alpha + img3Reg * (1-alpha);
        print(img4.shape)
        #filename = os.path.splitext(os.path.split(src_filepath)[1])[0];
        #ext = os.path.splitext(target_filepath)[1];
        cv.imwrite(os.path.join(out_dir, filename + '_multiplex_overlay_tumor'+ext), img4.astype(np.uint8))

def get_border(img_path, out_dir):
    img = cv.imread(img_path,0) 
    img_rgb = cv.imread(img_path) 
    print(img.shape)  
    print(img.min())  
    print(img.max())  
    img_binary = (img < 200) * 255;    
    cv.imwrite(os.path.join(out_dir, 'binary.png'), img_binary.astype(np.uint8))
    contours, hierarchy = cv.findContours(img_binary.astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img_rgb, contours, -1, (255,0,0,255), 2)
    cv.imwrite(os.path.join(out_dir, 'rgb_boundary.png'), img_rgb.astype(np.uint8))

if __name__=='__main__':

    #out_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/registered';
    #resize_factor = RESIZE_FACTOR

    ##multi_filepath = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/multiplex', 'O6218_MULTI_3-multires.tif')
    ##he_filepath = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/he', 'O6218-HE-CROP-multires.tif')
    ##he_tumor_filepath = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/tumor', 'O6218-HE-CROP-multires_tumor.tif')
    ##tumor_mask_filepath = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/tumor', 'O6218-HE-CROP-multires_tumor_mask.tif')

    #multi_filepath = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/multiplex', '3908-multires.tif')
    #he_filepath = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/he', 'N3908-HE-CROP-multires.tif')
    #he_tumor_filepath = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/tumor', 'N3908-HE-CROP-multires_tumor.tif')
    #tumor_mask_filepath = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/tumor', 'N3908-HE-CROP-multires_tumor_mask.tif')

    #register_single(multi_filepath, he_filepath, he_tumor_filepath, tumor_mask_filepath, out_dir);

    ##img_path = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/multiplex', 'O6218_MULTI_3-multires.tif');
    #img_path = os.path.join('/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/he', 'O6218-HE-CROP-multires.tif');
    out_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/debug';
    #get_border(img_path, out_dir);
    multi_filepath = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/debug/binary_m.png';
    he_filepath = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/debug/binary_he.png';
    register_single(multi_filepath, he_filepath, None, None, out_dir);

