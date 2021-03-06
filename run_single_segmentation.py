import time
import futils.util as futil
import segmentor as v_seg
import keras.backend as K
import tensorflow as tf

# TensorFlow wizardry
config = tf.ConfigProto()

# Don't pre-allocate memory; allocate as-needed
config.gpu_options.allow_growth = True

# Only allow a total of half the GPU memory to be allocated
config.gpu_options.per_process_gpu_memory_fraction = 0.5

# Create a session with the above options specified.
K.tensorflow_backend.set_session(tf.Session(config=config))
K.set_learning_phase(1)

#LOAD THE MODEL
segment = v_seg.v_segmentor(batch_size=1, model='/content/LungLobeSegmentation/models/final.h5', ptch_sz=128, z_sz=64)



#LOAD THE CT_SCAN
scan_file = 'test.mhd'
ct_scan, origin, spacing, orientation = futil.load_itk("/content/LungLobeSegmentation/data/"+scan_file, get_orientation=True)
if (orientation[-1] == -1):
    ct_scan = ct_scan[::-1]
print 'Origem: '
print origin
print 'Spacing: '
print spacing
print 'Orientation: '
print orientation



#NORMALIZATION
ct_scan = futil.normalize(ct_scan)
print 'succesfully normalized'


#PREDICT the segmentation
t1 = time.time()
print 't1: '
print t1
lobe_mask = segment.predict(ct_scan)
t2 = time.time()
print t2-t1


#Save the segmentation
futil.save_itk('/content/LungLobeSegmentation/results/'+scan_file, lobe_mask, origin, spacing)
