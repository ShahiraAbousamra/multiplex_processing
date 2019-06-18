import os;
import numpy as np;
import json;
import skimage.io as io;
import glob;

RESIZE_FACTOR = 50
 
def tumor_mask(img_he_filepath, json_filepath, resize_factor, out_dir):
    img = io.imread(img_he_filepath);
    print(img.shape)
    height = img.shape[0]*resize_factor;
    width = img.shape[1]*resize_factor;
    alpha = 0.8
    a = np.array((255, 150, 0));
    mask = np.zeros(img.shape);
    
    jsonfile = open(json_filepath, 'r');
    for line in jsonfile:
        line_json = json.loads(line);
        prob = line_json['properties']['metric_value']
        x1, y1, x2, y2 = line_json['bbox'];
        x1 = int(x1 * width/resize_factor);
        x2 = int(x2 * width/resize_factor);
        y1 = int(y1 * height/resize_factor);
        y2 = int(y2 * height/resize_factor);
        if(prob > 0.5):
            img[y1:y2, x1:x2] = alpha * img[y1:y2, x1:x2] + (1-alpha)*a ;
            mask[y1:y2, x1:x2] = a;
    io.imsave(os.path.join(out_dir, os.path.splitext(os.path.split(img_he_filepath)[1])[0] + '_tumor.tif'), img);
    io.imsave(os.path.join(out_dir, os.path.splitext(os.path.split(img_he_filepath)[1])[0] + '_tumor_mask.tif'), mask.astype(np.uint8));



if __name__=='__main__':
    in_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/he'
    out_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/tumor';
    json_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi';
    files = glob.glob(os.path.join(in_dir, '*.tif'));
    resize_factor = RESIZE_FACTOR
    for file in files:
        print(file);
        json_filepath = os.path.join(json_dir, os.path.splitext('heatmap_'+os.path.split(file)[1])[0]+'.json')
        tumor_mask(file, json_filepath, resize_factor, out_dir);



