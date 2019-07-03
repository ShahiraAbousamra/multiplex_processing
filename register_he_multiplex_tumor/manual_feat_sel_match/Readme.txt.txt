Firt, put input images in the directory: C:\Users\maozheng\test\input_images

Steps to do the registration:
1. open cmd
2. type the following to go to the work directory:
cd C:\Users\areeha_batool\test
3. type the following to run registration:
python registration_for_user.py <batch name> <image_name_K17> <image_name_K19> <image_name_H&E>

For example: python registration_for_user.py M3669 M3669k17_cropped.tif M3669k19_cropped.tif M3669he_cropped.tif
4. The registrated results are in the registrated_images\<batch_name>
