%%%%%%%%
% The 2nd file to run. Writes Perseus files.
% 
% Requires:
%   - image files Experiments/XXXXX/frames/frame?????.png
%   - parameter file Experiments/XXXXX/parameters.csv
% Outputs: Perseus files Experiments/XXXXX/perseusYZ/frame?????.csv, where
%   - Y is 'n' for normalised image files, '' otherwise
%   - Z is 'i' for inverted image files, '' otherwise
%%%%%%%%

video = '6chbt20c';
normalised = 1; % pixel intensities normalised? 0 = no, 1 = yes
inverted = 0; % pixel intensities inverted? 0 = no, 1 = yes

folder = 'perseus';
if normalised
    folder = strcat(folder,'n');
end
if inverted
    folder = strcat(folder,'i');
end
cd ../Experiments
cd(video)
mkdir(folder)

% Read parameters.csv
param = num2cell(csvread('parameters.csv')');
[start,inc,endd,height,width,affI] = param{:};

% Writing Perseus files
npix   = width*height;
for i = start:inc:endd
    filename = strcat('frame',num2str(i,'%.5d'))
    R = imread(strcat('frames/',filename,'.png'));
    if inverted
        R = imcomplement(R);
    end
    R = double(R);
    if normalised
        R = R/affI;
    end
    A=reshape(R',npix,1);
    data=[2.0;width;height;A];
    csvwrite(strcat(folder,'/',filename,'.csv'),data);
end

cd ../../Code