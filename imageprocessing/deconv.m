%Removes master dark image, runs a low pass gaussian filter, and performs a
%Richardson-Lucy deconvolution of the image
%Requires image processing toolbox

clear all;
close all;

imagefile = '/Users/magnus/Documents/MIGDAL/Ar_0634/images/MIG_full_readout_Fe55_Ar_CF4_220805T150634.CAL.0244.TIFF'
darkfile = '/Users/magnus/Documents/MIGDAL/maxratenoise/masterDark.fig'
resolution = 1152;
outputnamestem = 'ar_0634_img0244'

%Standard deviations of the pointspread functions in real and fourier space
%respectively
pointspread = 8;
filtercutoff = 120;

%Extract the mean dark image data from the .fig file containing it
fig = openfig(darkfile, 'new', 'invisible');
imgs = findobj(fig, 'Type', 'image');
meandark = get(imgs(1), 'CData');

%load image file and read it as an array
rawimage = Tiff(imagefile);
rawdata = double(read(rawimage));

%Subtract mean dark
darkremoved = rawdata - meandark;

%Generate gaussian profiles for the point spread function (psf) and
%gaussian filter to remove the hole pattern
[gaussianfilter] = Gaussian2d(resolution,filtercutoff);
[psf] = Gaussian2d(resolution,pointspread);


%Implement gaussian filter
FFT_image = fft2(darkremoved);
filtered_FFT_image = FFT_image.*fftshift(gaussianfilter);
filtered_image = real(ifft2(filtered_FFT_image));

%Perform RL deconvolution 
deconvoled_image = deconvlucy(filtered_image, psf, 10);

tagstruct.ImageLength = resolution; 
tagstruct.ImageWidth = resolution;
tagstruct.BitsPerSample = 32;
tagstruct.Photometric = 1
tagstruct.SampleFormat = 2
tagstruct.SamplesPerPixel = 1;
tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky; 
tagstruct.Software = 'MATLAB'; 

figure(1)
clf % clear any previous figure
fmd = gcf; % get figure handle for saving
fmd.Color = 'w'; % set figure background to white, the default gray is awful
imagesc(deconvoled_image);
title(strcat(outputnamestem,': \sigma =  ',string(pointspread)))
print(strcat(outputnamestem,'.png'),'-dpng','-r600');
%t1 = Tiff(strcat(outputnamestem,'.tif'),'w')
%setTag(t1,tagstruct)
%write(t1,int32(deconvoled_image*65535))
%close(t1)
imwrite(uint16(deconvoled_image*65535), strcat(outputnamestem,'.tif'))

%axis off;

figure(2)
clf % clear any previous figure
fmd = gcf; % get figure handle for saving
fmd.Color = 'w'; % set figure background to white, the default gray is awful
imagesc(rawdata);
title(strcat(outputnamestem,' no dark'))
print(strcat(outputnamestem,'.png'),'-dpng','-r600');
%t2 = Tiff(strcat(outputnamestem,'nodark','.tif'),'w')
%setTag(t2,tagstruct)
%write(t2,int32(darkremoved))
%close(t2)
imwrite(uint16(darkremoved), strcat(outputnamestem,'nodark','.tif'))