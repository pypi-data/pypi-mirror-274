import ants
import pandas as pd
import numpy as np
import antspymm


# Example file paths and output prefix
x='dtPC12'
statistical_file_path="/tmp/"+x+".csv"
data_dictionary_path = "~/code/ANTsPyMM/docs/antspymm_data_dictionary.csv"
output_prefix = '/tmp/vizit_'+x
edge_image_path = '~/.antspymm/PPMI_template0_edge.nii.gz'
edge_image_path = '~/.antspymm/PPMI_template0_brain.nii.gz'
brain_image = ants.image_read( edge_image_path )
brain_image_t = ants.iMath( brain_image, 'TruncateIntensity', 0.002, 0.99)
# Call the function
zz = pd.read_csv( statistical_file_path )
ocols = zz.keys()

qqq = zz.copy()
qqq['anat'] = qqq['anat'].str.replace(r'(vol_|thk_|LRAVG_|_LRAVG|Asym_|_Asym|volAsym|volLRAVG|thkAsym|thkLRAVG)', '', regex=True)
# olimg = antspymm.brainmap_figure(qqq, data_dictionary_path, output_prefix + myco, brain_image_t, nslices=21, black_bg=False, axes=[1], fixed_overlay_range=[-1.0,1.0],verbose=True )

qqq['anat'] = qqq['anat'].str.replace(r'(DTI_mean_fa_|DTI_mean_md.|DTI_mean_md_|.LRAVG.)', '', regex=True)

olimg = antspymm.brainmap_figure(qqq, data_dictionary_path, output_prefix, brain_image_t, nslices=21, black_bg=True,     crop=0,        overlay_cmap='winter', fixed_overlay_range=[0,1.],verbose=True )

ants.image_write( olimg, '/tmp/'+x+'.nii.gz' )
