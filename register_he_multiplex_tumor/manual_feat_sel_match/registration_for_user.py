import cv2
import numpy as np
import scipy.io
import os
import time
from namelists import namelists
import sys
import os
from shutil import move
basefolder=os.getcwd()
datafolder=basefolder+'/input_images/'
mode=sys.argv[1]
doregi=1#int(sys.argv[2])

name_lists=[]
name_lists.append(sys.argv[2])
name_lists.append(sys.argv[3])
#name_lists.append(sys.argv[4])
print(name_lists)
def homo_regi(name_lists,doUI):
  #Do homography registration
  #name_lists: lists of image path
  #doUI: flag 1/0 for whether  do UI
  #output:registered: a list of images that are registered
 
  namelists={'namelists':name_lists}
  scipy.io.savemat(basefolder+'/namelists.mat',namelists)
  if not os.path.exists(basefolder+'/registered_images/'):
    os.mkdir(basefolder+'/registered_images/')
  if not os.path.exists(basefolder+'/points_save/'):
    os.mkdir(basefolder+'/points_save/')
  if not os.path.exists(basefolder+'/registered_images/'+mode):
    os.mkdir(basefolder+'/registered_images/'+mode)
  if doUI:
    #os.system('matlab -r -nodesktop "run /nfs/data01/shared/mazhao6/k_17/UI"')
    os.system('matlab -nodesktop -r "run "UI;""')
    while not os.path.exists(basefolder+'/UIflag.mat'):
      time.sleep(3)
      print('waiting for 3 sec')
    os.remove(basefolder+'/UIflag.mat')
    move(basefolder+'/UIpoints.mat',basefolder+'/points_save/UIpoints_'+mode+'.mat')
  print('registrating')
  points=scipy.io.loadmat(basefolder+'/points_save/UIpoints_'+mode+'.mat')
  
  # Read destination image.
  im_dst = cv2.imread(datafolder+namelists['namelists'][0])#
  print(im_dst.shape)
  # Four corners of the book in destination image.
  pts_dst = points['P'][0][0]#np.array([[318, 256],[534, 372],[316, 670],[73, 473]])
  registered=[]
  registered.append(im_dst)
  for i in range(len(namelists['namelists'])-1):
    print(i)
    # Read source image.
    im_src = cv2.imread(datafolder+namelists['namelists'][i+1])
    # Four corners of the book in source image
    pts_src = points['P'][0][i+1]#np.array([[141, 131], [480, 159], [493, 630],[64, 601]])
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
    
    #none0area=(im_out>0)
    #im_dst_none0=im_dst*none0area
    #cv2.imwrite("Destination_n0"+str(i)+".jpg", im_dst_none0)
    # Display images
    cv2.imwrite(basefolder+'/registered_images/'+mode+'/'+name_lists[0]+'.jpg', im_dst)
    #cv2.imwrite("Destination"+str(i)+".jpg", im_dst)
    cv2.imwrite(basefolder+'/registered_images/'+mode+'/'+name_lists[i+1]+'.jpg', im_out)
    registered.append(im_out)
    
  return registered
  

regied_im=homo_regi(name_lists,doregi)
print('finish registration')

    

