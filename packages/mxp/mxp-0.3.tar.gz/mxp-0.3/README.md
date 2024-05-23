# mxp
Support code to read qPCR machine file formats,
such as the .mxp file format created by MxPro.

Currently reads files from 300 and 305 machines.


## Example usage to convert to excel
 ```python
 import mxp
 from pathlib import Path

 def convert_mxp_to_excel(filename):
     filename = Path(filename)
     output_filename = filename.parent / (filename.name + '.xlxs')
     df = mxp.read_mxp(filename)
     df.to_excel(output_filename)

 # convert all mxp files in the current folder
 for filename in Path('.').glob("*.mxp"):
     convert_mxp_to_excel(filename)
 ```    

