import openslide;
import os;
import glob;


RESIZE_FACTOR = 50

# resize image from level 0 by dividing by the given resize factor
def resize_img(filepath, resize_factor, out_dir):
    slide = openslide.OpenSlide(filepath)
    img = slide.get_thumbnail((slide.dimensions[0]/resize_factor, slide.dimensions[1]/resize_factor))
    img.save(os.path.join(out_dir,os.path.split(filepath)[1]))



if __name__=='__main__':
    in_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images/he'
    out_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/he';
    files = glob.glob(os.path.join(in_dir, '*.tif'));
    resize_factor = RESIZE_FACTOR
    for file in files:
        print(file);
        resize_img(file, resize_factor, out_dir);

    in_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images/multiplex'
    out_dir = '/gpfs/projects/KurcGroup/sabousamra/multiplex/register_he_multi/images_resize50/multiplex';
    files = glob.glob(os.path.join(in_dir, '*.tif'));
    resize_factor = RESIZE_FACTOR
    for file in files:
        print(file);
        resize_img(file, resize_factor, out_dir);
