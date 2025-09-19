# andorSif class
An easy, clear python class for sif reading and data visualization 

Based on [`sif_parser`](https://github.com/fujiisoup/sif_parser), and build a simple python class for better enjoyment in data visualization.

## Usage

Download the script and put `spectrum.py` in the root directory of your python project

```python
import os 

path = '/home/username/path/to/your_sifs'

#os.scandir returns DirEntry -> .path will extract string
sif_files = [f.path for f in os.scandir(path) if f.name.endswith('.sif')]

import spectrum as spe 

spec_list = [spe.Spectrum.read_sif(sif_files[i]) for i in range(len(sif_files))]
```
this will print useful metadata as 

```python

Key                  Value                                                                               
          SifVersion                                                                                65567
      ExperimentTime                                                                           1753840979
 DetectorTemperature                                                                                -65.0
        ExposureTime                                                                                 30.0
           CycleTime                                                                              30.0447
AccumulatedCycleTime                                                                              30.0447
   AccumulatedCycles                                                                                    1
      StackCycleTime                                                                               901.34
    PixelReadoutTime                                                                              0.00001
             GainDAC                                                                                  2.0
           GateWidth                                                                                  0.0
        GratingBlaze                                                                             0.000008
        DetectorType                                                                           DU420_BEX2
  DetectorDimensions                                                                          (1024, 256)
    OriginalFilename                                b'C:\\yt\\20250730\\mos2_gr_0OD_0.56mW_30s_ram_2.sif'
         ShutterTime                                                                           (0.0, 0.0)
...

```

```python
spec_list[0].plot_sif('lambda') # will plot Counts to wavelengths

spec_list[0].plot_sif('raman') # will plot Counts to ramans

```

you can also retrieve data and plot your data by
```python
xdata = spec_list[1].ramans
ydata = spec_list[1].data[0,0,:]
```
and throw them to the plotting framework you are comfortable with.

Have fun!
