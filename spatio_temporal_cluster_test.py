# import dependencies
import os
import numpy as np
import mne
import eelbrain.lab as e

# define lobe and time window 
hemi = 'left hemisphere'

tstart = 0.13 # in seconds
tstop = 0.18

tstart_msec = tstart*1000 # in milliseconds
tstop_msec = tstop*1000

# set subjects directory
subjects_dir = '/Volumes/LEG_2TB/Documents/Experiments/Tark_Rep/Data/MRIs'

# template for all stc files
fname = '/Volumes/LEG_2TB/Documents/Experiments/Tark_Rep/Data/stc_timeFixed/free_signed_lite/%s%s/%s%s_%s-lh.stc'


# prepare containers to collect data and condition labels
subjects = []
others = []
stims = []
stcs = []


# load all stcs and put into containers
for subject in ['A0003', 'A0005', 'A0008', 'A0014', 'A0032', 'A0051', 'A0054', 'A0056', 'A0058', 'A0059', 'A0068', 'A0078', 'A0085', 'A0100', 'A0103', 'A0104']:
    for other in ['1','4']:
        for stim in ['word']:
            # load the stc
            stc_fname = fname % (stim, other, stim, other, subject,)
            stc = mne.read_source_estimate(stc_fname, subject=subject)
            print stc_fname
            subjects.append(subject)
            others.append(other)
            stims.append(stim)
            stcs.append(stc)


# make eelbrain dataset
ds = e.Dataset()
ds['subject'] = e.Factor(subjects, random=True)
ds['other'] = e.Factor(others)
ds['stim'] = e.Factor(stims)
ds['src'] = e.load.fiff.stc_ndvar(stcs, 'fsaverage', 'ico-4', subjects_dir)
src = ds['src']



### s e t t i n g     u p     s p a t i o     r e g i o n      to      t e s t ###

#-
## from a set of labels
label_dir = '/Volumes/LEG_2TB/Documents/Experiments/Tark_Rep/Data/MRIs/'

### single label
fusiform = mne.read_label(label_dir + 'lh.fusiform.label')

src_fus = src.sub(source=fusiform)

### group of labels together
ba17_lh = mne.read_label(label_dir + 'leftba17-lh.label')
ba17_rh = mne.read_label(label_dir + 'rightba17-rh.label')
ba18_lh = mne.read_label(label_dir + 'leftba18-lh.label')
ba18_rh = mne.read_label(label_dir + 'rightba18-rh.label')
ba19_lh = mne.read_label(label_dir + 'leftba19-lh.label')
ba19_rh = mne.read_label(label_dir + 'rightba19-rh.label')

occipital = src.sub( source=ba17_lh + ba17_rh + ba18_lh + ba18_rh + ba19_lh + ba19_rh )

#-
## to whole left hemisphere
src_lh = src.sub(source='lh')

#-
## from the fsaverage annot parcelation

annot_fusiform = mne.read_labels_from_annot(subject='fsaverage',parc='aparc',hemi='lh',surf_name='inflated',regexp='fusiform',subjects_dir=subjects_dir)
idx_fus = [src.source.index_for_label(l) for l in annot_fusiform]
idx_fus = np.any([i.x for i in idx_fus], 0)

annot_lat = mne.read_labels_from_annot(subject='fsaverage',parc='aparc',hemi='lh',surf_name='inflated',regexp='lateralocc',subjects_dir=subjects_dir)
idx_lat = [src.source.index_for_label(l) for l in annot_lat]
idx_lat = np.any([i.x for i in idx_lat], 0)

annot_inf = mne.read_labels_from_annot(subject='fsaverage',parc='aparc',hemi='lh',surf_name='inflated',regexp='inferiortem',subjects_dir=subjects_dir)
idx_inf = [src.source.index_for_label(l) for l in annot_inf]
idx_inf = np.any([i.x for i in idx_inf], 0)

src_lat_fus = src.sub(source=idx_lat + idx_fus + idx_inf)

#-
## to a region from a user-made annot file (built from the sources of a significant cluster)

symbol_cluster = mne.read_labels_from_annot(subject='fsaverage',parc='symbol_cluster_label',hemi='lh',surf_name='inflated',subjects_dir=subjects_dir)
ant_cluster = symbol_cluster[0]
ant_source = src.sub( source=ant_cluster)





### s t a t i s t i c a l   t e s t s ###

testing = occipital # allocate object to the region you want to test so that this can be used throughout

# T-TEST:

res = e.testnd.ttest_rel(testing, ds['other'], ds=ds, tstart=0.08, tstop=0.15, samples=1000, pmin=0.05, mintime=0.01, minsource = 10, match='subject')

# threshold free:
res = e.testnd.ttest_rel(testing, ds['other'], ds=ds, tstart=0.08, tstop=0.15, samples=1000, match='subject',tfce=True)


# ANOVA:

res = e.testnd.anova(testing, ds['other'], ds=ds,
	samples=100,  # number of permutations
	pmin=0.1,  # threshold for clusters (uncorrected p-value)
	tstart=0.08,  # start of the time window of interest
	tstop=0.13,  # stop of the time window of interest
	mintime=0.02,  # minimum duration for clusters
	minsource=10,  # minimum number of sources for clusters
	match='subject')  # needs to be specified in a by-subject design
	
# threshold free
res = e.testnd.anova(testing, ds['symbol']*ds['stim'], ds=ds,
	samples=10,  # number of permutations,
	tstart=0.2,  # start of the time window of interest
	tstop=0.3,  # stop of the time window of interest
	match='subject',
	tfce = True)  # needs to be specified in a b
      



# v i e w    r e s u l t s #

# sort clusters according to their p-value
res.clusters.sort("p")
    
# print table of all clusters sorted by time
table = res.clusters.as_table()
print table
    
# loop through and add plots for each cluster, using x as the index for which cluster out of the results table to use
x = 0
# retrieve cluster
c_0 = res.clusters[x, 'cluster']
cstart = res.clusters[x, 'tstart'] * 1000
cstop = res.clusters[x, 'tstop'] * 1000
hemi = res.clusters[x, 'hemi'].encode('utf-8')

# average over time and plot the cluster extent
c_extent = c_0.sum('time')
plt_extent = e.plot.brain.cluster(c_extent, views = ['ve','lat'], surf = 'inflated')
            
# do not average over time, and view the cluster at a user-define time-point            
p_time = e.plot.brain.cluster(c_0, views = ['ve','lat'], surf = 'inflated')
p_time.set_time(0.13)

#-
# extract and analyze the time course in the cluster
index = c_extent != 0
c_timecourse = testing.mean(index)

# c_extent is a boolean NDVar over space only, so here we are summing over the
# spatial extent of the cluster for every time point but keep the time dimension

# plot waveforms for the cluster. If you want to see different condition averages, change the model (here 'other', could be 'other%stim')
plt_tc = e.plot.UTSStat(c_timecourse, 'other', ds=ds, clusters=res.clusters[x:(x+1)], title = "", ylabel = "dSPM") # to plot just 0-500 xlim=[0,0.5]
ax = plt_tc.figure.axes[0]
ax.axvspan(cstart,cstop, zorder=-1, color='r', alpha=0.2) # adds when the sig cluster occurred
ax.axvline(tstart, zorder=-1, color='b') # adds the window that was tested
ax.axvline(tstop, zorder=-1, color='b')


# -
## to save sources of the cluster to a label
labels = e.labels_from_clusters(c_extent)
mne_fixes.write_labels_to_annot(labels,'fsaverage','noise_cluster_label',subjects_dir=subjects_dir, overwrite = True)

# plot waveform without the cluster test
timecourse = testing.mean('source')
plt_tc = e.plot.UTSStat(timecourse, 'other', ds=ds, title = "")