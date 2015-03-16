import sys
import os
import surfer
import mne
import numpy as np
import pdb
from mayavi import mlab
from eelbrain import *

from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from tvtk.pyface.scene_model import SceneModel
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.core.ui.mayavi_scene import MayaviScene
#import IPython.core.ipapi
#ipython = IPython.core.ipapi.get()
#ipython.magic('gui wx')

#setup the mne stuff and the freesurfer stuff
exec('''
import os
import mne
os.environ["SUBJECTS_DIR"]="/Applications/freesurfer/subjects/"
os.environ["FREESURFER_HOME"]="/Applications/Freesurfer"
os.environ["MNE_ROOT"]="/Applications/MNE-2.7.0-3106-MacOSX-i386"
os.environ["PATH"] = os.environ["PATH"] + os.environ["MNE_ROOT"] + "/bin"
''')

subjects_dir = '/Applications/freesurfer/subjects/'
   
def plot_all(hemi,parc_list):

    #set the hemisphere
    if hemi.lower() == 'right': hemi = 'Right'
    elif hemi.lower() == 'left': hemi = 'Left'
    else: raise

    # initiate the brain
    b = surfer.Brain('fsaverage', 'lh', 'inflated', config_opts={'cortex':'bone'})

    # loop through each of the desired annotations in the list given by the user, and add them to the brain defined above
    colors=[];
    
    for parc in parc_list:
         
        annot = mne.read_labels_from_annot(subject='fsaverage',parc='aparc',hemi='lh',surf_name='inflated',regexp=parc,subjects_dir=subjects_dir)
        lbl = annot[0]
        print lbl

        color = (np.random.random(), np.random.random(), np.random.random())
        b.add_label(lbl,  color=color, alpha=1) 
        colors.append(color)
        
    b.save_image("brain_left.tiff")
  
    c = surfer.Brain('fsaverage', 'lh', 'inflated', config_opts={'cortex':'bone'}, views=['ven'])

    loop_count = 0
    for parc in parc_list:
      
        annot = mne.read_labels_from_annot(subject='fsaverage',parc='aparc',hemi='lh',surf_name='inflated',regexp=parc,subjects_dir=subjects_dir)
        lbl = annot[0]
        print lbl

        color = colors[loop_count]
        c.add_label(lbl,  color=color, alpha=1) 
        
        loop_count += 1  
    
    c.save_image("brain_ven.tiff")
    

###################

###Change this to right or left depending on which hemisphere BAs you are plotting###
plot_all('left',['occipital','fusiform','inferiortem','superiortem','middletem'])
#mlab.show()