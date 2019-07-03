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
MAX_FEATURES_1 = 5000; # 5000
# Number of features to extract from the wsi patch
MAX_FEATURES_2 = 5000; # 5000
# percent of top matched features to use
GOOD_MATCH_PERCENT = 0.1
#GOOD_MATCH_PERCENT = 0.05
# matching similarity constraints
GRID_SIZE = 5 # 5 #12
MAX_MATCH_DISTANCE = 50;#60
MIN_MATCH_DISTANCE = 0;

 
def register_single_divided(multi_filepath, he_filepath, he_tumor_filepath, tumor_mask_filepath, out_dir):
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
    orb1 = cv.ORB_create(int(MAX_FEATURES_1/GRID_SIZE))
    orb2 = cv.ORB_create(int(MAX_FEATURES_2/GRID_SIZE))

    # read ref patch
    img1 = cv.imread(src_filepath,0)
    img2 = cv.imread(target_filepath,0)
    matcher = cv.DescriptorMatcher_create(cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
#    grid_kp1 = [[0 for j in range(GRID_SIZE) ] for i in range(GRID_SIZE)]
#    grid_kp2 = [[0 for j in range(GRID_SIZE) ] for i in range(GRID_SIZE)]
#    grid_desc1 = [[0 for j in range(GRID_SIZE) ] for i in range(GRID_SIZE)]
#    grid_desc2 = [[0 for j in range(GRID_SIZE) ] for i in range(GRID_SIZE)]
    matches = [];
    kp1 = [];
    kp2 = [];

    ystep1 = int(img1.shape[0]/GRID_SIZE);
    xstep1 = int(img1.shape[1]/GRID_SIZE);
    ystep2 = int(img2.shape[0]/GRID_SIZE);
    xstep2 = int(img2.shape[1]/GRID_SIZE);
    # find the keypoints with ORB
    #kp1, descriptors1 = orb1.detectAndCompute(img1,None)
    match_indx = 0;
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            whiteness = np.std(img1[y*ystep1: min((y+1)*ystep1, img1.shape[0]), x*xstep1: min((x+1)*xstep1, img1.shape[1])].flatten())
            if(whiteness < 5):
                continue;
            whiteness = np.std(img2[y*ystep2: min((y+1)*ystep2, img2.shape[0]), x*xstep2: min((x+1)*xstep2, img2.shape[1])].flatten())
            if(whiteness < 5):
                continue;
 
            #if(x ==0 and y ==0 or x == 0 and y == GRID_SIZE-1):
            #    continue;
            kp1_cell, desc1_cell = orb1.detectAndCompute(img1[y*ystep1: min((y+1)*ystep1, img1.shape[0]), x*xstep1: min((x+1)*xstep1, img1.shape[1])],None)
            kp2_cell, desc2_cell = orb2.detectAndCompute(img2[y*ystep2: min((y+1)*ystep2, img2.shape[0]), x*xstep2: min((x+1)*xstep2, img2.shape[1])],None)
            if(len(kp1_cell)<= 0 or len(kp2_cell)<= 0):
                continue;
            matches_cell = matcher.match(desc1_cell, desc2_cell, None)
            matches_cell.sort(key=lambda x: x.distance, reverse=False)
            print(type(kp1_cell))
            for match in matches_cell:
                if(match.distance<MIN_MATCH_DISTANCE):   
                    continue;
                if(match.distance>MAX_MATCH_DISTANCE):
                    break;
		#print('--------')
		#print(kp1_cell[match.trainIdx].size)
                #kp1_cell[match.trainIdx].pt[0] += y*ystep1;
                #kp1_cell[match.trainIdx].pt[1] += x*xstep1;
                #kp2_cell[match.queryIdx].pt[0] += y*ystep1;
                #kp2_cell[match.queryIdx].pt[1] += x*xstep1;
                kp_pnt = kp1_cell[match.queryIdx];
                #if(kp_pnt.response < 0.000001):
                #    continue;
               
                
                print(kp_pnt.pt)
                print(kp_pnt.size)
                print(kp_pnt.angle)
                print(kp_pnt.response)
                print(kp_pnt.octave)
                print(kp_pnt.class_id)
                print(match.trainIdx);
                print(match.queryIdx);
                print(match.imgIdx);
                print(len(kp1_cell))               
                print(len(kp2_cell))
                kp_pnt_new = cv.KeyPoint(kp_pnt.pt[0]+ x*xstep1, kp_pnt.pt[1]+ y*ystep1, float(kp_pnt.size), float(kp_pnt.angle), float(kp_pnt.response), kp_pnt.octave, kp_pnt.class_id);
                kp1.append(kp_pnt_new);

                kp_pnt = kp2_cell[match.trainIdx]; 
                kp_pnt_new = cv.KeyPoint(kp_pnt.pt[0]+ x*xstep2, kp_pnt.pt[1]+ y*ystep2, float(kp_pnt.size), float(kp_pnt.angle), float(kp_pnt.response), kp_pnt.octave, kp_pnt.class_id);
                kp2.append(kp_pnt_new);
                
                matches.append(cv.DMatch(match_indx, match_indx, match.distance));
                match_indx += 1;

    # draw only keypoints location,not size and orientation
    #img1_feat = cv.drawKeypoints(img1, kp1, None, color=(0,255,0), flags=0)

    #found = False;
    #img2 = cv.imread(target_filepath,0)
    #kp2, descriptors2 = orb2.detectAndCompute(img2,None)

    # Match features
    #matcher = cv.DescriptorMatcher_create(cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    #matches = matcher.match(descriptors1, descriptors2, None)
    #print('matches len = ', len(matches))

    # Sort matches by score
    #matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    #numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    #matches = matches[:numGoodMatches]
    #print('matches[0].distance = ', matches[0].distance)
    #print('matches[-1].distance = ', matches[-1].distance)

    ## Draw top matches
    imMatches = cv.drawMatches(img1, kp1, img2, kp2, matches, None)
    cv.imwrite(os.path.join(out_dir, "matches2.jpg"), imMatches);

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
    imMatches = cv.drawMatches(img1, kp1, img2, kp2, matches, None)
    cv.imwrite(os.path.join(out_dir, "matches2.jpg"), imMatches);

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

def get_border(img_path, out_dir, suffix):
    img = cv.imread(img_path,0) 
    img_rgb = cv.imread(img_path) 
    print(img.shape)  
    print(img.min())  
    print(img.max())  
    #img_binary = (img < img.max()-30) * 255;    
    kernel=np.ones((3,3))
    img_binary=cv.dilate((img < img.max()-30).astype('uint8')*255,kernel,iterations=1)
    cv.imwrite(os.path.join(out_dir, 'binary3'+suffix+'.png'), img_binary.astype(np.uint8))
    _,contours, hierarchy = cv.findContours(img_binary.astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for c in range(len(contours)):
        print(len(contours[c]));
        if(len(contours[c]) > 400):
            cv.drawContours(img_rgb, contours, c, (255,0,0,255), -1)
    cv.imwrite(os.path.join(out_dir, 'rgb_boundary3'+suffix+'.png'), img_rgb.astype(np.uint8))

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
    #out_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/debug';

    #get_border(img_path, out_dir);
    #multi_filepath = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/debug/binary_m.png';
    #he_filepath = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/debug/binary_he.png';
    #register_single(multi_filepath, he_filepath, None, None, out_dir);
    
    #he_filename = 'N22034he_cropped-multires'
    #multiplex_filename = 'N22034-multires'

    #he_filename = 'L-6745_D11-1-multires';
    #multiplex_filename = 'L6745-multires';

    #he_filename = 'O-0135-E8-1-multires';
    #multiplex_filename = 'O0135-multires';

    #he_filename = 'O-3936_C3-1-multires';
    #multiplex_filename = 'O3936-multires';

    #he_filename = 'N-4277_C9-1-multires';
    #multiplex_filename = 'N4277-multires';

    he_filename = 'N9430_HE-multires';
    multiplex_filename = 'N9430-multires';

    #he_filename = 'N22034he_cropped-multires';
    #multiplex_filename = 'N22034-multires';


    out_dir = '/data08/shared/shahira/multiplex/validate/debug';
    multi_filepath = os.path.join('/data08/shared/shahira/multiplex/validate/wsi_multiplex_resize50', multiplex_filename+'.tif')
    he_filepath = os.path.join('/data08/shared/shahira/multiplex/validate/wsi_he_resize25', he_filename + '.tif')
    he_tumor_filepath = os.path.join('/data08/shared/shahira/multiplex/validate/tumor_resize25', he_filename+'_tumor.tif')
    tumor_mask_filepath = os.path.join('/data08/shared/shahira/multiplex/validate/tumor_resize25', he_filename+'_tumor_mask.tif')
    #get_border(multi_filepath, out_dir, '_m');
    #get_border(he_filepath, out_dir, '_he');
    #register_single_divided(os.path.join('/data08/shared/shahira/multiplex/validate/registered', 'rgb_boundary3'+'_m'+'.png'), os.path.join('/data08/shared/shahira/multiplex/validate/registered', 'rgb_boundary3'+'_he'+'.png'), he_tumor_filepath, tumor_mask_filepath, out_dir);
    register_single_divided(multi_filepath, he_filepath, he_tumor_filepath, tumor_mask_filepath, out_dir);
