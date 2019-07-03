def namelists(mode):
  name_lists=''
  if mode=='N3':
    name_lists=['N0090_B11_K17_CROP_3.tif','N0090_B11_HE_CROP_3.tif','N0090_B11_K19_CROP_3.tif']
  elif mode=='N2':
    name_lists=['N0090_B11_K17_CROP_2.tif','N0090_B11_HE_CROP_2.tif','N0090_B11_K19_CROP_2.tif']
  elif mode=='N1':
    name_lists=['N0090_B11_K17_CROP.tif','N0090_B11_HE_CROP.tif','N0090_B11_K19_CROP.tif']
  elif mode=='02':
    name_lists=['021073_D7_K17_CROP.tif','021073_D7_HE_CROP.tif','021073_D7_K19_CROP.tif']
  elif mode=='02half':
    name_lists=['021073_D7_K17_CROP_half.tif','021073_D7_HE_CROP_half.tif','021073_D7_K19_CROP_half.tif']
  elif mode=='2M3':
    name_lists=['M3669k17_cropped.tif','M3669he_cropped.tif','M3669k19_cropped.tif']
  elif mode=='2N2':
    name_lists=['N22034k17_cropped.tif','N22034he_cropped.tif','N22034k19_cropped.tif']
  elif mode=='2H9':
    name_lists=['H9430k17_cropped.tif','N9430he_cropped.tif','H9430k19_cropped.tif']
  elif mode=='wN9':
    name_lists=['N9430K17_1_1.tiff','N9430H&E_1_1.tiff','N9430K19_1_1.tiff']
  elif mode=='k19noregi':
    name_lists=['N22034k19_cropped.tif','M3669k19_cropped.tif','H9430k19_cropped.tif']
  return name_lists
    
