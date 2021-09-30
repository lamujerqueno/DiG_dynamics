from numpy import loadtxt
from os import chdir,mkdir,path,system
from warnings import simplefilter,warn

def readSettings():
    simplefilter('always')
    SettingsFile = 'SETTINGS.txt'
    inputsource = 0
    video = ''
    images = ''
    topfolder = '../Experiments'
    folderManual = False
    method = 0
    normalised = 1
    inverted = 0
    extrafolders = []
    with open(SettingsFile) as f:
        for line in f:
            setting = line.split('#')[0].strip().split()
            if len(setting) == 1 or len(setting) >= 3:
                warn('incorrect syntax in %s, line ignored: %s.' % (SettingsFile,line), SyntaxWarning)
            if len(setting) == 2:
                if setting[0] == 'INPUTSOURCE':
                    inputsource = int(setting[1])
                elif setting[0] == 'VIDEO':
                    video = setting[1]
                elif setting[0] == 'IMAGES':
                    images = setting[1]
                elif setting[0] == 'TOPFOLDER':
                    topfolder = setting[1]
                elif setting[0] == 'FOLDER':
                    folderManual = True
                    folder = setting[1]
                elif setting[0] == 'METHOD':
                    method = int(setting[1])
                elif setting[0] == 'NORMALISED':
                    normalised = int(setting[1])
                elif setting[0] == 'INVERTED':
                    inverted = int(setting[1])
                elif setting[0] == 'EXTRAFOLDER':
                    extrafolders.append(setting[1])
                else:
                    warn('unrecognised setting in %s (ignored): %s.' % (SettingsFile,setting[0]), SyntaxWarning)
    if (inputsource == 0 and not video) or (inputsource == 1 and not images):
        need = ('IMAGES' if inputsource else 'VIDEO')
        raise SyntaxError('please specify %s parameter in %s!' % (need,SettingsFile))
    if not folderManual:
        if inputsource:
            folder = images
        else:
            folder = video.rsplit('.',1)[0]
    return (inputsource, video, images, topfolder, folder, method, normalised, inverted, extrafolders)

def findSuffix(method, normalised, inverted):
    suffix = ''
    if method == 1:
        suffix += 'r'
    elif method == 2:
        suffix += 'g'
    elif method == 3:
        suffix += 'b'
    if normalised == 1:
        suffix += 'n'
    if inverted == 1:
        suffix += 'i'
    return suffix

def checkDependencies(filename, inputsource, video, images, topfolder, folder, method, normalised, inverted):
    framesFile = 'write_images.py'
    perseusFile = 'write_perseus.py'
    phFile = 'write_persistence.py'
    persistenceFile = 'write_PDimages.py'
    combinedimgFile = 'write_PDandpics.py'
    croppedFile = 'crop_images.py'
    normimgFile = 'norm_pictures.py'
    normpersFile = 'norm_persistence.py'
    normgradFile = 'norm_gradient.py'
    distimgFile = 'dist_pictures.py'
    distpersFile = 'dist_persistence.py'
    distgradFile = 'dist_gradient.py'
    previous = { perseusFile: framesFile, phFile: perseusFile, persistenceFile: phFile, combinedimgFile: persistenceFile, \
                 croppedFile: framesFile, normimgFile: framesFile, normpersFile: phFile, normgradFile: framesFile, \
                 distimgFile: framesFile, distpersFile: phFile, distgradFile: framesFile }
    suffix = findSuffix(method, normalised, inverted)
    try:
        param = loadtxt('%s/%s/parameters.csv' % (topfolder,folder))
        lastframe = int(param[0]) - 1
        if previous[filename] == framesFile:
            needFolder = 'frames'
            extension = 'png'
        elif previous[filename] == perseusFile:
            needFolder = 'perseus'+suffix
            extension = 'csv'
        elif previous[filename] == phFile:
            needFolder = 'ph0'+suffix
            extension = 'csv'
        elif previous[filename] == persistenceFile:
            needFolder = 'persistence'+suffix
            extension = 'png'
        with open('%s/%s/%s/frame%.5d.%s' % (topfolder,folder,needFolder,lastframe,extension)) as f:
            pass
    except:
        return (False, previous[filename])
    try:
        with open('%s/%s/%s/cropping.csv' % (topfolder,folder,needFolder)) as f:
            cropping = loadtxt(f)
        if (cropping==param[1:5]).all():
            return (True, None)
        else:
            print('Cropping values in the folder %s do not coincide with the main ones!' % needFolder)
            return (False, previous[filename])
    except:
        return (True, None)

def progressBar(done,total,width=50,s1='*',s2=' '):
    nums1 = int(done*width/total+0.5)
    string = ' [' + s1*nums1 + s2*(width-nums1) + ']%7d /%7d'%(done,total)
    print(string, end='\r')
    if done == total:
        print('\nDone!')

def tryCreatingFolder(foldername):
    try:
        mkdir(foldername)
    except OSError:
        while True:
            cont = input('Folder "%s" already exists, continue? [y/n] ' % foldername).strip().lower()
            if cont=='y' or cont=='yes':
                break
            elif cont=='n' or cont=='no':
                raise RuntimeError('process terminated by user.')
            else:
                print('Please enter y or n...')

def firstThingsToDo(filename):
    print(' - '+filename)
    inputsource, video, images, topfolder, folder, method, normalised, inverted, extrafolders = readSettings()
    depmet,previous = checkDependencies(filename, inputsource, video, images, topfolder, folder, method, normalised, inverted)
    if not depmet:
        print('Dependencies for %s not met: running %s first...' % (filename,previous))
        prev = system('python '+previous)
        if prev:
            raise RuntimeError('process terminated by user.')
    chdir(topfolder+'/'+folder)
    param = loadtxt('parameters.csv')
    return (method, normalised, inverted, param)
