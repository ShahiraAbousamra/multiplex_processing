import cv2
import numpy as np
import scipy.io
import os
import time
from namelists import namelists
import sys
import os
from shutil import move
#basefolder=os.getcwd()

OVERLAY_ALPHA = 0.9;

def homo_regi(img1_filepath, img2_filepath, tmp_dir, tmp_base_name, doUI):
  #Do homography registration
  #name_lists: lists of image path
  #doUI: flag 1/0 for whether  do UI
  #output:registered: a list of images that are registered
 
  name_lists=[]
  name_lists.append(img1_filepath)
  name_lists.append(img2_filepath)
  namelists={'namelists':name_lists}
  scipy.io.savemat(tmp_dir+'/namelists.mat',namelists)

  if not os.path.exists(tmp_dir+'/points_save/'):
    os.mkdir(tmp_dir+'/points_save/')
  #if not os.path.exists(basefolder+'/registered_images/'+mode):
  #  os.mkdir(basefolder+'/registered_images/'+mode)
  if doUI:
    #os.system('matlab -r -nodesktop "run /nfs/data01/shared/mazhao6/k_17/UI"')
    os.system('matlab -nodesktop -r "run "UI;""')
    while not os.path.exists(tmp_dir+'/UIflag.mat'):
      time.sleep(3)
      print('waiting for 3 sec')
    os.remove(tmp_dir+'/UIflag.mat')
    move(tmp_dir+'/UIpoints.mat',tmp_dir+'/points_save/UIpoints_'+tmp_base_name+'.mat')
  print('registrating')
  points=scipy.io.loadmat(tmp_dir+'/points_save/UIpoints_'+tmp_base_name+'.mat')
  
  # Read destination image.
  im_dst = cv2.imread(img1_filepath)#
  print(im_dst.shape)
  # Four corners of the book in destination image.
  pts_dst = points['P'][0][0]#np.array([[318, 256],[534, 372],[316, 670],[73, 473]])
  registered=[]
  registered.append(im_dst)
  
  
  # Read source image.
  im_src = cv2.imread(img2_filepath)
  # Four corners of the book in source image
  pts_src = points['P'][0][1]#np.array([[141, 131], [480, 159], [493, 630],[64, 601]])
  # Calculate Homography
  h, status = cv2.findHomography(pts_src, pts_dst)
  # Warp source image to destination based on homography
  #im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
  

  # Display images
  #cv2.imwrite(basefolder+'/registered_images/'+mode+'/'+name_lists[0]+'.jpg', im_dst)
  #cv2.imwrite(basefolder+'/registered_images/'+mode+'/'+name_lists[i+1]+'.jpg', im_out)
  #registered.append(im_
  target_width, target_height = im_dst.shape[1],im_dst.shape[0]

  return h, target_width, target_height;
  
def use_homography(h, img_filepath, out_dir, out_filename, width, height ):
  img = cv2.imread(img_filepath,1)
  img_out = cv2.warpPerspective(img, h, (width, height ))
  cv2.imwrite(os.path.join(out_dir, out_filename), img_out)
  return img_out;

def overlay(img_filepath, img_overlay, out_dir, out_filename):
  img = cv2.imread(img_filepath,1)
  print(img.shape)
  print(img_overlay.shape)
  img_out = img * OVERLAY_ALPHA + img_overlay * (1-OVERLAY_ALPHA);
  cv2.imwrite(os.path.join(out_dir, out_filename), img_out.astype(np.uint8))
  return img_out;


if __name__=='__main__':


  in_dir_multi = '/data08/shared/shahira/multiplex/validate/wsi_multiplex_resize50'
  in_dir_he = '/data08/shared/shahira/multiplex/validate/wsi_he_resize50'
  in_dir_tumor = '/data08/shared/shahira/multiplex/validate/tumor_resize50'
  
  out_dir = '/data08/shared/shahira/multiplex/validate/registered_manual_anno_tmp';
  #tmp_dir = '/data08/shared/shahira/multiplex/validate/reg_manual_anno_tmp'
  tmp_dir = os.getcwd();

  he_list = [];
  multiplex_list = [];
 
  #he_list.append('N-4277_C9-1-multires.tif');
  #multiplex_list.append('N4277-multires.tif');

  he_list.append('N9430_HE-multires.tif');
  multiplex_list.append('N9430-multires.tif');

  #he_list.append('N22034he_cropped-multires.tif');
  #multiplex_list.append('N22034-multires.tif');

  for i in range(len(he_list)):
    he_filename = he_list[i];
    multiplex_filename = multiplex_list[i];
    print(multiplex_filename);
    print(he_filename);
    print(' ');

    multi_filepath = os.path.join(in_dir_multi, multiplex_filename);
    he_filepath = os.path.join(in_dir_he, he_filename)
    he_tumor_filepath = os.path.join(in_dir_tumor, os.path.splitext(he_filename)[0]+'_tumor.tif')
    tumor_mask_filepath = os.path.join(in_dir_tumor, os.path.splitext(he_filename)[0]+'_tumor_mask.tif')

    doUI = True;
    out_base_filename = os.path.splitext(multiplex_filename)[0];
    ext = '.tif'
    h, target_width, target_height = homo_regi(multi_filepath, he_filepath, tmp_dir, out_base_filename, doUI)

    img_he_reg = use_homography(h, he_filepath, out_dir, out_base_filename + '_he_registered'+ext, target_width, target_height);
    img_he_tumor_reg = use_homography(h, he_tumor_filepath, out_dir, out_base_filename + '_he_tumor_registered' +ext, target_width, target_height);
    img_tumor_reg = use_homography(h, tumor_mask_filepath, out_dir, out_base_filename + '_tumor_mask_registered' +ext, target_width, target_height);
    
    img_multiplex_tumor_reg = overlay(multi_filepath, img_tumor_reg, out_dir, out_base_filename + '_multiplex_overlay_tumor'+ext )




  print('finish registration')

    

