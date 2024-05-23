import sys, os
os.environ["TF_NUM_INTEROP_THREADS"] = "8"
os.environ["TF_NUM_INTRAOP_THREADS"] = "8"
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "8"
import tempfile
import shutil
import tensorflow as tf
import antspymm
import antspyt1w
import antspynet
import ants
import numpy as np
from scipy.stats import median_abs_deviation
import math
import statsmodels.api as sm
t1fn = "/Users/stnava/data/PTBP/images/PEDS049/20110217//Anatomy/PEDS049_20110217_mprage_t1.nii.gz"
idpfn = "/Users/stnava/data/PTBP/images/PEDS049/20110217//PCASL/PEDS049_20110217_pcasl_1.nii.gz"
if not 'dkt' in globals():
  t1head = ants.image_read( t1fn ).n3_bias_field_correction( 8 ).n3_bias_field_correction( 4 )
  t1bxt = antspynet.brain_extraction( t1head, 't1' ).threshold_image( 0.3, 1.0 )
  t1 = t1bxt * t1head
  t1seg = antspynet.deep_atropos( t1head )
  t1segmentation = t1seg['segmentation_image']
  dkt = antspynet.desikan_killiany_tourville_labeling( t1head )
#################
type_of_transform='Rigid'
tc='alternating'
fmri = ants.image_read( idpfn )
print("do perf")
perf = antspymm.bold_perfusion( fmri, t1head, t1, 
  t1segmentation, dkt, robust=True, verbose=True )
##################
ants.plot( perf['cbf'], axis=2, crop=True )
# ants.image_write( ants.iMath( perf['perfusion'], "Normalize" ), '/tmp/temp.nii.gz' )
# ants.image_write( perf['motion_corrected'], '/tmp/temp2.nii.gz' )
# ants.image_write( perf['cbf'], '/tmp/temp3ptb.nii.gz' )
