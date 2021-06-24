%%%%%%%%
% The 1st file to run. Extracts frames from video, crops and writes the
% frames, and computes the normalisation constant.
% Top-level folder contains two subfolders, "Code" and "Experiments".
%
% Requires: file Experiments/XXXXX.mp4 (where XXXXX is given by the "video"
%           variable below)
% Output:
%   - image files Experiments/XXXXX/frames/frame?????.png
%   - parameter file Experiments/XXXXX/parameters.csv
%%%%%%%%


video = '6chbt20c'; % the file name of an .mp4 file in Experiments folder
startframe = 1; % the first frame analysed
increment = 5; % take every n-th frame
method = 0; % channel to take for persistent homology: 0 = greyscale,
            % 1 = red, 2 = green, 3 = blue

cd ../Experiments
videofile = strcat(video,'.mp4');
obj = VideoReader(videofile);
v = read(obj);
height = obj.Height;
width = obj.Width;
nframes = obj.NumFrames;

% cropping
left = 1;
right = width;
top = 1;
bottom = height;

% writing the images and computing the normalisation constant
mkdir(video)
cd(video)
mkdir frames
newheight = bottom-top+1;
newwidth = right-left+1;
npix = newheight*newwidth;
I=zeros(1,nframes);
for i = startframe:increment:nframes
    img = v(:,:,:,i);
    if method == 0
        imgr = rgb2gray(img);
    else
        imgr = img(:,:,method);
    end
    imgc = imgr(top:bottom,left:right);
    filename = strcat('frames/frame',num2str(i,'%.5d'),'.png')
    imwrite(imgc,filename);
    I(1,i) = sum(imgc,'all')/npix;
end
affI = max(I);

% writing the file with parameters: first frame, increment, last frame,
% height, width, normalisation constant
data = [startframe;increment;nframes;newheight;newwidth;affI];
csvwrite('parameters.csv',data);

cd ../../Code
