%Run master dark calculation

darkDir = '/Users/magnus/Documents/MIGDAL/maxratenoise/';

bLoadMasterDarkFig = false; % true: load from .fig; false: run dark noise calculation


masterDarkFileName = 'masterDarkfast.fig';
masterSTDFileName = 'masterSTDDarkfast.fig';

 

if ~bLoadMasterDarkFig

    % Calculate Master Dark

    figure(1); close 1 % close figures used by calcDarkMaster_v3
    figure(2); close 2
    figure(3); close 3   

    [MasterDark,MasterSigmaDark,lambdaFit,lambdaErr] = calcDarkMaster_v3(darkDir);

else

    try

        figMasterDark = open(strcat(darkDir,masterDarkFileName));

        figSTDDark = open(strcat(darkDir,masterSTDFileName));

        

        % extract Master Dark

        axesObjsMD = get(figMasterDark,'CurrentAxes');  % axes handle

        dataObjsMD = get(axesObjsMD,'Children'); % handles to low-level graphics objects in axes

        MasterDark = dataObjsMD.CData;

        

        % extract noise image

        axesObjsSTD = get(figSTDDark,'CurrentAxes');  % axes handle

        dataObjsSTD = get(axesObjsSTD,'Children'); % handles to low-level graphics objects in axes

        STD = dataObjsSTD.CData;

        

        close(figMasterDark)

        close(figSTDDark)

        

    catch % exits if mean dark and/or noise .figs are unloadable or don't exist

        disp('Error Loading Master Dark')

        return

    end
end