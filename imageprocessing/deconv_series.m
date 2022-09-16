%perform deconvolution on an entire directory
%Removes master dark image, runs a low pass gaussian filter, and performs a
%Richardson-Lucy deconvolution of the image
%Requires image processing toolbox

clear all;
close all;

imagedir = '/Users/magnus/Documents/MIGDAL/MIGDAL_day_1/2022-07-25-Chamber_test/630V_580V_200ms/quiet/'
darkfile = '/Users/magnus/Documents/MIGDAL/MIGDAL_day_1/2022-07-25-Chamber_test/dark_200ms/quiet/masterDark.fig'
resolution = 1152;
outputnamestem = 'quiet630_580_200_'

darkremoveddir = "/Users/magnus/Documents/MIGDAL/MIGDAL_day_1/2022-07-25-Chamber_test/630V_580V_200ms/quietdarkremoved/"
deconvoluteddir = "/Users/magnus/Documents/MIGDAL/MIGDAL_day_1/2022-07-25-Chamber_test/630V_580V_200ms/quietdeconv/"

myFiles = dir(fullfile(imagedir,'*.tif'))

%Standard deviations of the pointspread functions in real and fourier space
%respectively
pointspread = 8;
filtercutoff = 120;

for k = 1:length(myFiles)


    baseFileName = myFiles(k).name;
    fullFileName = fullfile(imagedir, baseFileName);
    
    filename = [imagedir,myFiles(k).name]
    %Extract the mean dark image data from the .fig file containing it
    fig = openfig(darkfile, 'new', 'invisible');
    imgs = findobj(fig, 'Type', 'image');
    meandark = get(imgs(1), 'CData');

    %load image file and read it as an array
    rawimage = Tiff(filename);
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


    %figure(1)
    %clf % clear any previous figure
    %fmd = gcf; % get figure handle for saving
    %fmd.Color = 'w'; % set figure background to white, the default gray is awful
    %imagesc(deconvoled_image);
    %title(strcat(outputnamestem,': \sigma =  ',string(pointspread)))
    %print(strcat(outputnamestem,'.png'),'-dpng','-r600');
    imwrite(uint16(deconvoled_image*65535), strcat(deconvoluteddir,outputnamestem,string(k),'.tif'))

    %axis off;

    %figure(2)
    %clf % clear any previous figure
    %fmd = gcf; % get figure handle for saving
    %fmd.Color = 'w'; % set figure background to white, the default gray is awful
    %imagesc(rawdata);
    %title(strcat(outputnamestem,' no dark'))
    %print(strcat(outputnamestem,'.png'),'-dpng','-r600');
    imwrite(uint16(darkremoved), strcat(darkremoveddir,outputnamestem,string(k),'nodark','.tif'))

end