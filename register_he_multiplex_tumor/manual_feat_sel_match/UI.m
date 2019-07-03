
function flag=UI()

load('namelists.mat')
P={};

%figure(1), subplot(1,3,1),imshow(imread(['C:\Users\maozheng\test\cropped_h\',strtrim(namelists(0,:))])),
%subplot(1,3,2),imshow(imread(['C:\Users\maozheng\test\cropped_h\',strtrim(namelists(1,:))])),
%subplot(1,3,3),imshow(imread(['C:\Users\maozheng\test\cropped_h\',strtrim(namelists(2,:))])),
figure,
img1={}
for i=1:size(namelists)
  strtrim(namelists(i,:))
  %img1{i}=imread([pwd,'/input_images/',strtrim(namelists(i,:))]);%'/nfs/data01/shared/mazhao6/K_17_page/cropped_h/',
  img1{i}=imread([strtrim(namelists(i,:))]);%'/nfs/data01/shared/mazhao6/K_17_page/cropped_h/',
  subplot(1,2,i),imshow(img1{i}),title(['image',num2str(i)])
end

for i=1:size(namelists)
  strtrim(namelists(i,:))
  img=img1{i};%imread(['C:\Users\maozheng\test\input_images\',strtrim(namelists(i,:))]);%'/nfs/data01/shared/mazhao6/K_17_page/cropped_h/',
  'success'
  figure, 
  imshow(img),title(['image ',num2str(i),': please select points'])
  [y1, x1] = getpts;
  hold on
  plot(y1,x1,'*')
  P{i}=[y1 x1];
end
flag=0;
save(['UIpoints.mat'],'P')
save('UIflag.mat','flag')
exit;
