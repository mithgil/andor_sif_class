import pandas as pd
import numpy as np
from typing import Optional
import sif_parser

class Spectrum:
    def __init__(
        self,
        filename: str,
        data: np.ndarray,
        wavelengths: np.ndarray,
        info: Optional[dict] = None
    ) -> None:
        self.filename = filename
        self.data = data
        self.wavelengths = wavelengths
        self.ramans = np.array([])
        self.info = info or {}
        
        if not isinstance(data, np.ndarray):
            raise TypeError(f"data must be numpy.ndarray, got {type(data).__name__}")
        if not isinstance(wavelengths, np.ndarray):
            raise TypeError(f"wavelengths must be numpy.ndarray, got {type(wavelengths).__name__}")
            
    @staticmethod
    def read_sif(filename: str, verbose: bool = True) -> 'Spectrum':
        data, info = sif_parser.np_open(filename)
        wavelengths = sif_parser.utils.extract_calibration(info)
    
        if verbose:
            df = pd.DataFrame(info.items(), columns=['Key', 'Value'])
            print(df.to_string(index=False, justify='left'))
            
        return Spectrum(filename, data, wavelengths, info)

    def convert_xaxis_unit(self):

        self.ramans = ((1/self.info['RamanExWavelength']) - 1/(self.wavelengths))*1e7
    
    def plot_sif(self, axis) -> None: 
        
        fig, ax = plt.subplots(1,1,figsize = (11,6))
        counts = self.data[0,0,:] # eliminate unity dimensions
        
        wvs_allowed_keywords = {'wavelengths', 'lambda', 'wvl'}
        rams_allowed_keywords = {'raman', 'ramans','rams'}
        
        if axis.lower() in wvs_allowed_keywords:
            ax.plot(self.wavelengths, counts)
            ax.set_xlabel("Wavelength (nm)", fontsize = 22)
            
        elif axis.lower() in rams_allowed_keywords:

            if self.ramans.size == 0: 
                try:
                    self.convert_xaxis_unit()
                except KeyError:
                    raise ValueError(
                        "Cannot convert to Raman shift. 'RamanExWavelength' key "
                        "not found in the spectrum's info dictionary."
                    )
            if self.ramans.size == 0:
                raise ValueError("Raman conversion failed - empty array")
        
            if self.ramans.shape != counts.shape:
                raise ValueError(
                    f"Shape mismatch: ramans {self.ramans.shape} vs counts {counts.shape}"
                )
            ax.plot(self.ramans, counts)
            ax.set_xlabel(r'Raman shift (cm$^{-1}$)', fontsize = 22)
            
        else:
            raise ValueError(f"Invalid axis keyword: '{axis}'. Allowed keywords are: {wvs_allowed_keywords}, {rams_allowed_keywords}")
                
        ax.tick_params(axis='both', labelsize=14) 
        ax.set_ylabel('Counts', fontsize = 22)

        plt.savefig("{}_.png".format(self.filename[:-4]), dpi=500, bbox_inches = 'tight')
        
        plt.show()