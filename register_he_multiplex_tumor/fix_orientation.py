import cv2 as cv
import os


def flip_v(img_filepath):
  img1 = cv.imread(img_filepath)
  img2 = cv.flip( img1, 1 )
  cv.imwrite(img_filepath, img2);

def flip_h(img_filepath):
  img1 = cv.imread(img_filepath)
  img2 = cv.flip( img1, 0 )
  cv.imwrite(img_filepath, img2);


if __name__=='__main__':
  he_filename = 'N9430_HE-multires';
  he_filepath = os.path.join('/data08/shared/shahira/multiplex/validate/wsi_he_resize50', he_filename + '.tif') 
  he_tumor_filepath = os.path.join('/data08/shared/shahira/multiplex/validate/tumor_resize50', he_filename+'_tumor.tif')
  tumor_mask_filepath = os.path.join('/data08/shared/shahira/multiplex/validate/tumor_resize50', he_filename+'_tumor_mask.tif')
  
  flip_h(he_filepath);
  flip_h(he_tumor_filepath);
  flip_h(tumor_mask_filepath);

  flip_v(he_filepath);
  flip_v(he_tumor_filepath);
  flip_v(tumor_mask_filepath);


 
