% Randy Laffler & Alex Mills  29.May.2019 - added comments 27.July.2022

% For .tiff image files

% Loads dark images from directory 'baseDir' and claculates the mean dark
% image (Master dark) and noise image (Master STD) using sigma clipping.
% Saves those iamges and a histogram of the noise image in the same
% directory as .fig files.

% lambdaFit is the parameter of a Poisson fit to the noise histogram.
% lambdaErr is the error of the Poisson fit.
% These two can be removed those if they get annoying.

function [MasterDark,MasterSTDDark,lambdaFit,lambdaErr] = calcDarkMaster_v3(baseDir)

import matlab.io.*; % not sure if necessary

fNames = dir(fullfile(baseDir,'*.tif')) % load .tiff image names in baseDir
NumFiles = length(fNames); % get number of .tiff images in baseDir
fileName = [baseDir,fNames(1).name]; % file name of first .tiff
t = Tiff(fileName); % load first .tiff image
data1 = read(t); % read data of first .tiff image
close(t);

iSize = size(data1); % get height and width of .tiff image for memory allocation

nSigma = 5; % sigma clipping threshold

highPixCut = inf; % for cutting hot pixels

% Initilaize (allocate memory for) some variables
prelimMeanDark = zeros(iSize); % preliminary mean dark initial image
Num_Good_per_pixel = ones(iSize)*NumFiles; % pixel count image
prelimSumN = sum(Num_Good_per_pixel(:)); % sum of pixels used

disp('Preliminary Mean Calculation')

for i = 1:NumFiles % loop over darks to get preliminary mean dark image
    
    fileName = strcat(baseDir,fNames(i).name); % .tiff name
    t = Tiff(fileName); % load .tiff
    tempMat = double(read(t)); % read .tiff
    close(t);
    highPixInd = tempMat > highPixCut; % hot pixel cut mask
    tempMat(highPixInd) = 0; % hot pixel cut
    prelimMeanDark = prelimMeanDark + tempMat; % sum up darks for mean calculation
    % remove hot pixel from total pixel count
    Num_Good_per_pixel(highPixInd) = Num_Good_per_pixel(highPixInd) - 1;
    
    if i == 1 % turn off annoying .tiff read messages
        w = warning('query','last');
        id = w.identifier;
        warning('off',id);
    end
    
end

prelimMeanDark = prelimMeanDark./Num_Good_per_pixel; % calculate mean dark

% read in all dark images, calc std

disp('Preliminary STD Calculation')
tempChi2 = zeros(iSize); % intermediate set in std dev calculation initial image

for i = 1:NumFiles % loop over darks to get preliminary noise image
    
    fileName = strcat(baseDir,fNames(i).name); % .tiff name
    t = Tiff(fileName); % load .tiff
    tempMat = double(read(t)); % read .tiff
    close(t);
    highPixInd = tempMat > highPixCut; % hot pixel cut mask
    tempMat(highPixInd) = prelimMeanDark(highPixInd); % hot pixel cut
    % first part of standard deviation calculation
    tempChi2 = tempChi2 + (tempMat - prelimMeanDark).^2;
    
end

% second part of standard deviation calculation: the noise image
prelimSTDDark = sqrt(tempChi2./(Num_Good_per_pixel - 1));

disp('Finished Preliminary STD')

tempSTDDark = prelimSTDDark; % store preliminary noise image
tempMeanDark = prelimMeanDark; % store preliminary mean dark image
sumN = prelimSumN; % sum of pixels used, part of while loop exit condition
prevSumN = 0; % previous sum of pixels used, other part of while loop exit condition
n = 0; % while loop loop counter

while prevSumN ~= sumN % loop over darks until sigma clipping is finished
    
    n = n + 1; % iterate loop number
    prevSumN = sumN; % set exit parameter
    
    Num_Good_per_pixel = ones(iSize)*NumFiles; % restart all good each time
    M_plus_STD_Dark = tempMeanDark + nSigma*tempSTDDark; % upper sigma clip
    M_minus_STD_Dark = tempMeanDark - nSigma*tempSTDDark; % lower sigma clip
    
    tempMeanDark1 = zeros(iSize);
    
    for i = 1:NumFiles % loop over darks to calculate clipped mean dark image
        
        fileName = strcat(baseDir,fNames(i).name); % .tiff name
        t = Tiff(fileName); % load .tiff
        tempMat = double(read(t)); % read .tiff
        close(t);
        badIndex = ((tempMat > M_plus_STD_Dark) | ... sigma clip mask
            (tempMat < M_minus_STD_Dark)) | (tempMat > highPixCut);
        tempMat(badIndex) = 0; % sigma clip
        Num_Good_per_pixel(badIndex) = Num_Good_per_pixel(badIndex) - 1;% uncount clipped pixels
        tempMeanDark1 = tempMeanDark1 + tempMat; % sum up clipped darks
        
    end
    
    tempMeanDark = tempMeanDark1./Num_Good_per_pixel; % clipped mean dark
    
    sumN = sum(Num_Good_per_pixel(:)); % set other exit parameter
    tChi2 = zeros(iSize);
    
    for i = 1:NumFiles % loop over darks to calculate clipped noise image
        
        fileName = strcat(baseDir,fNames(i).name); % .tiff name
        t = Tiff(fileName); % load .tiff
        tempMat = double(read(t)); % read .tiff
        close(t);
        badIndex = ((tempMat > M_plus_STD_Dark) | ... sigma clip mask
            (tempMat < M_minus_STD_Dark)) | (tempMat > highPixCut);
        tempMat(badIndex) = tempMeanDark(badIndex); % sigma clip
        tChi2 = tChi2 + (tempMat - tempMeanDark).^2; % square part of std dev
        
    end
    
    tempSTDDark = sqrt(tChi2./(Num_Good_per_pixel - 1)); % rest of std dev, aka noise
    
    fprintf('Loop: %i, prevSumN = %i, sumN = %i\n',n,prevSumN,sumN)
    
end

disp('Done!  Plotting...')

MasterDark = tempMeanDark;
MasterSTDDark = tempSTDDark;

MDfileName = [baseDir,'masterDark.fig']; % mean dark image file name
figure(1) % plot mean dark image
clf % clear figure 1
fmd = gcf; % get figure handle for saving
fmd.Color = 'w'; % set figure background to white, the default gray is awful
imagesc(MasterDark)
title('Master Dark')
xlabel('X')
ylabel('Y')
colormap jet % set the best colour scheme (unless you're colorblind)
cb = colorbar; % display colorbar
cb.Label.String = 'Intensity [ADU]'; % set colorbar label
view([0,90]) % set view angle... may not be necessary
axis square % fix image axes to a square
axmd = gca; % get axis handle to set font size
axmd.FontSize = 16; % set fontsize to something readable
savefig(fmd,MDfileName);

STDfileName = [baseDir,'masterSTDDark.fig']; % noise image file name
figure(2) % plot noise image
clf % clear figure 2
fstd = gcf; % get figure handle for saving
fstd.Color = 'w'; % set figure background to white
imagesc(MasterSTDDark)
title('Master STD')
xlabel('X')
ylabel('Y')
colormap jet % set the best colour scheme
cb = colorbar; % display colorbar
cb.Label.String = 'Intensity [ADU]'; % set colorbar label
view([0,90]) % set view angle... may not be necessary
axis square % fix image axes to a square
axstd = gca; % get axis handle to set font size
axstd.FontSize = 16; % set fontsize to something readable
savefig(fstd,STDfileName);

hFileName = [baseDir,'hist_masterSTDDark.fig']; % noise histogram file name
X = prelimSTDDark(:); % vectorize pre-clipped noise image
x = MasterSTDDark(:); % vectorize sigma clipped noise image
[lambdaFit,lci] = poissfit(x); % do a poisson fit to sigma clipped noise
lambdaErr = (lci(2) - lci(1))/3.96; % calculate fit error? Randy did this.

figure(3) % plot sigma clipped noise hisgoram with comparison to pre-clipped noise
clf % clear figure 3
fh = gcf; % get figure handle for saving
fh.Color = 'w'; % set figure background to white
histogram(X,'DisplayStyle','Stair','EdgeColor','r','LineWidth',2,'BinWidth',0.1)
hold on % don't overwrite above histogram
histogram(x,'DisplayStyle','Stair','EdgeColor','k','LineWidth',2,'BinWidth',0.1)
xlabel('Master STD')
ylabel('Counts')
legend({'Raw dark sigmas','Clipped dark sigmas'},'location','best')
ax = gca; % get axis handle to manipulate axes
ax.FontSize = 16; % set fontsize to something readable
ax.YScale = 'log'; % set y axis scale to log
yly = ylim; % get y axis limits: the default cuts off single count bins (Why!?)
ylim([0.5 yly(2)]); % set y axis so bins with 1 count are visible
grid on % grids are nice
title(sprintf(['Per pixel standard deviation of master dark\nClip threshold:'...
    '%0.1f\\sigma, \\lambda = %0.3f \\pm %0.3f'],nSigma,lambdaFit,lambdaErr))
hold off % stop don't overwrite histogram for figure 3
savefig(fh,hFileName)

disp('Writing Figures to File')

end