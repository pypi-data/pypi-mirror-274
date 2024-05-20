from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.medimage_afni import NCorr
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
from pydra.engine.specs import MultiOutputType
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input time series file (4D data set)",
            "argstr": "-inset {in_file}",
            "mandatory": True,
        },
    ),
    (
        "in_rois",
        Nifti1,
        {
            "help_string": "input set of ROIs, each labelled with distinct integers",
            "argstr": "-in_rois {in_rois}",
            "mandatory": True,
        },
    ),
    (
        "mask",
        Nifti1,
        {
            "help_string": "can include a whole brain mask within which to calculate correlation. Otherwise, data should be masked already",
            "argstr": "-mask {mask}",
        },
    ),
    (
        "weight_ts",
        File,
        {
            "help_string": "input a 1D file WTS of weights that will be applied multiplicatively to each ROI's average time series. WTS can be a column- or row-file of values, but it must have the same length as the input time series volume. If the initial average time series was A[n] for n=0,..,(N-1) time points, then applying a set of weights W[n] of the same length from WTS would produce a new time series:  B[n] = A[n] * W[n]",
            "argstr": "-weight_ts {weight_ts}",
        },
    ),
    (
        "fish_z",
        bool,
        {
            "help_string": "switch to also output a matrix of Fisher Z-transform values for the corr coefs (r): Z = atanh(r) , (with Z=4 being output along matrix diagonals where r=1, as the r-to-Z conversion is ceilinged at Z = atanh(r=0.999329) = 4, which is still *quite* a high Pearson-r value",
            "argstr": "-fish_z",
        },
    ),
    (
        "part_corr",
        bool,
        {
            "help_string": "output the partial correlation matrix",
            "argstr": "-part_corr",
        },
    ),
    (
        "ts_out",
        bool,
        {
            "help_string": "switch to output the mean time series of the ROIs that have been used to generate the correlation matrices. Output filenames mirror those of the correlation matrix files, with a '.netts' postfix",
            "argstr": "-ts_out",
        },
    ),
    (
        "ts_label",
        bool,
        {
            "help_string": "additional switch when using '-ts_out'. Using this option will insert the integer ROI label at the start of each line of the *.netts file created. Thus, for a time series of length N, each line will have N+1 numbers, where the first is the integer ROI label and the subsequent N are scientific notation values",
            "argstr": "-ts_label",
        },
    ),
    (
        "ts_indiv",
        bool,
        {
            "help_string": "switch to create a directory for each network that contains the average time series for each ROI in individual files (each file has one line). The directories are labelled PREFIX_000_INDIV/, PREFIX_001_INDIV/, etc. (one per network). Within each directory, the files are labelled ROI_001.netts, ROI_002.netts, etc., with the numbers given by the actual ROI integer labels",
            "argstr": "-ts_indiv",
        },
    ),
    (
        "ts_wb_corr",
        bool,
        {
            "help_string": "switch to create a set of whole brain correlation maps. Performs whole brain correlation for each ROI's average time series; this will automatically create a directory for each network that contains the set of whole brain correlation maps (Pearson 'r's). The directories are labelled as above for '-ts_indiv' Within each directory, the files are labelled WB_CORR_ROI_001+orig, WB_CORR_ROI_002+orig, etc., with the numbers given by the actual ROI integer labels",
            "argstr": "-ts_wb_corr",
        },
    ),
    (
        "ts_wb_Z",
        bool,
        {
            "help_string": "same as above in '-ts_wb_corr', except that the maps have been Fisher transformed to Z-scores the relation: Z=atanh(r). To avoid infinities in the transform, Pearson values are effectively capped at |r| = 0.999329 (where |Z| = 4.0). Files are labelled WB_Z_ROI_001+orig, etc",
            "argstr": "-ts_wb_Z",
        },
    ),
    (
        "ts_wb_strlabel",
        bool,
        {
            "help_string": "by default, '-ts_wb_{corr,Z}' output files are named using the int number of a given ROI, such as: WB_Z_ROI_001+orig. With this option, one can replace the int (such as '001') with the string label (such as 'L-thalamus') *if* one has a labeltable attached to the file",
            "argstr": "-ts_wb_strlabel",
        },
    ),
    (
        "nifti",
        bool,
        {
            "help_string": "output any correlation map files as NIFTI files (default is BRIK/HEAD). Only useful if using '-ts_wb_corr' and/or '-ts_wb_Z'",
            "argstr": "-nifti",
        },
    ),
    (
        "output_mask_nonnull",
        bool,
        {
            "help_string": "internally, this program checks for where there are nonnull time series, because we don't like those, in general.  With this flag, the user can output the determined mask of non-null time series.",
            "argstr": "-output_mask_nonnull",
        },
    ),
    (
        "push_thru_many_zeros",
        bool,
        {
            "help_string": "by default, this program will grind to a halt and refuse to calculate if any ROI contains >10 percent of voxels with null times series (i.e., each point is 0), as of April, 2017.  This is because it seems most likely that hidden badness is responsible. However, if the user still wants to carry on the calculation anyways, then this option will allow one to push on through.  However, if any ROI *only* has null time series, then the program will not calculate and the user will really, really, really need to address their masking",
            "argstr": "-push_thru_many_zeros",
        },
    ),
    (
        "ignore_LT",
        bool,
        {
            "help_string": "switch to ignore any label table labels in the '-in_rois' file, if there are any labels attached",
            "argstr": "-ignore_LT",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output file name part",
            "argstr": "-prefix {out_file}",
            "position": 1,
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
net_corr_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_corr_matrix",
        File,
        {
            "help_string": "output correlation matrix between ROIs written to a text file with .netcc suffix"
        },
    ),
    (
        "out_corr_maps",
        ty.Union[File, ty.List[File], MultiOutputType],
        {"help_string": "output correlation maps in Pearson and/or Z-scores"},
    ),
]
net_corr_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class net_corr(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.engine.specs import MultiOutputType
    >>> from pydra.tasks.afni.auto.preprocess.net_corr import net_corr

    >>> task = net_corr()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.in_rois = Nifti1.mock(None)
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.weight_ts = File.mock()
    >>> task.inputs.fish_z = True
    >>> task.inputs.ts_wb_corr = True
    >>> task.inputs.ts_wb_Z = True
    >>> task.inputs.out_file = None
    >>> task.cmdline
    '3dNetCorr -prefix sub0.tp1.ncorr -fish_z -inset functional.nii -in_rois maps.nii -mask mask.nii -ts_wb_Z -ts_wb_corr'


    """

    input_spec = net_corr_input_spec
    output_spec = net_corr_output_spec
    executable = "3dNetCorr"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input time series file (4D data set)",
            "argstr": "-inset {in_file}",
            "mandatory": True,
        },
    ),
    (
        "in_rois",
        Nifti1,
        {
            "help_string": "input set of ROIs, each labelled with distinct integers",
            "argstr": "-in_rois {in_rois}",
            "mandatory": True,
        },
    ),
    (
        "mask",
        Nifti1,
        {
            "help_string": "can include a whole brain mask within which to calculate correlation. Otherwise, data should be masked already",
            "argstr": "-mask {mask}",
        },
    ),
    (
        "weight_ts",
        File,
        {
            "help_string": "input a 1D file WTS of weights that will be applied multiplicatively to each ROI's average time series. WTS can be a column- or row-file of values, but it must have the same length as the input time series volume. If the initial average time series was A[n] for n=0,..,(N-1) time points, then applying a set of weights W[n] of the same length from WTS would produce a new time series:  B[n] = A[n] * W[n]",
            "argstr": "-weight_ts {weight_ts}",
        },
    ),
    (
        "fish_z",
        bool,
        {
            "help_string": "switch to also output a matrix of Fisher Z-transform values for the corr coefs (r): Z = atanh(r) , (with Z=4 being output along matrix diagonals where r=1, as the r-to-Z conversion is ceilinged at Z = atanh(r=0.999329) = 4, which is still *quite* a high Pearson-r value",
            "argstr": "-fish_z",
        },
    ),
    (
        "part_corr",
        bool,
        {
            "help_string": "output the partial correlation matrix",
            "argstr": "-part_corr",
        },
    ),
    (
        "ts_out",
        bool,
        {
            "help_string": "switch to output the mean time series of the ROIs that have been used to generate the correlation matrices. Output filenames mirror those of the correlation matrix files, with a '.netts' postfix",
            "argstr": "-ts_out",
        },
    ),
    (
        "ts_label",
        bool,
        {
            "help_string": "additional switch when using '-ts_out'. Using this option will insert the integer ROI label at the start of each line of the *.netts file created. Thus, for a time series of length N, each line will have N+1 numbers, where the first is the integer ROI label and the subsequent N are scientific notation values",
            "argstr": "-ts_label",
        },
    ),
    (
        "ts_indiv",
        bool,
        {
            "help_string": "switch to create a directory for each network that contains the average time series for each ROI in individual files (each file has one line). The directories are labelled PREFIX_000_INDIV/, PREFIX_001_INDIV/, etc. (one per network). Within each directory, the files are labelled ROI_001.netts, ROI_002.netts, etc., with the numbers given by the actual ROI integer labels",
            "argstr": "-ts_indiv",
        },
    ),
    (
        "ts_wb_corr",
        bool,
        {
            "help_string": "switch to create a set of whole brain correlation maps. Performs whole brain correlation for each ROI's average time series; this will automatically create a directory for each network that contains the set of whole brain correlation maps (Pearson 'r's). The directories are labelled as above for '-ts_indiv' Within each directory, the files are labelled WB_CORR_ROI_001+orig, WB_CORR_ROI_002+orig, etc., with the numbers given by the actual ROI integer labels",
            "argstr": "-ts_wb_corr",
        },
    ),
    (
        "ts_wb_Z",
        bool,
        {
            "help_string": "same as above in '-ts_wb_corr', except that the maps have been Fisher transformed to Z-scores the relation: Z=atanh(r). To avoid infinities in the transform, Pearson values are effectively capped at |r| = 0.999329 (where |Z| = 4.0). Files are labelled WB_Z_ROI_001+orig, etc",
            "argstr": "-ts_wb_Z",
        },
    ),
    (
        "ts_wb_strlabel",
        bool,
        {
            "help_string": "by default, '-ts_wb_{corr,Z}' output files are named using the int number of a given ROI, such as: WB_Z_ROI_001+orig. With this option, one can replace the int (such as '001') with the string label (such as 'L-thalamus') *if* one has a labeltable attached to the file",
            "argstr": "-ts_wb_strlabel",
        },
    ),
    (
        "nifti",
        bool,
        {
            "help_string": "output any correlation map files as NIFTI files (default is BRIK/HEAD). Only useful if using '-ts_wb_corr' and/or '-ts_wb_Z'",
            "argstr": "-nifti",
        },
    ),
    (
        "output_mask_nonnull",
        bool,
        {
            "help_string": "internally, this program checks for where there are nonnull time series, because we don't like those, in general.  With this flag, the user can output the determined mask of non-null time series.",
            "argstr": "-output_mask_nonnull",
        },
    ),
    (
        "push_thru_many_zeros",
        bool,
        {
            "help_string": "by default, this program will grind to a halt and refuse to calculate if any ROI contains >10 percent of voxels with null times series (i.e., each point is 0), as of April, 2017.  This is because it seems most likely that hidden badness is responsible. However, if the user still wants to carry on the calculation anyways, then this option will allow one to push on through.  However, if any ROI *only* has null time series, then the program will not calculate and the user will really, really, really need to address their masking",
            "argstr": "-push_thru_many_zeros",
        },
    ),
    (
        "ignore_LT",
        bool,
        {
            "help_string": "switch to ignore any label table labels in the '-in_rois' file, if there are any labels attached",
            "argstr": "-ignore_LT",
        },
    ),
    (
        "out_file",
        NCorr,
        {
            "help_string": "output file name part",
            "argstr": "-prefix {out_file}",
            "position": 1,
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
NetCorr_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_corr_matrix",
        File,
        {
            "help_string": "output correlation matrix between ROIs written to a text file with .netcc suffix"
        },
    ),
    (
        "out_corr_maps",
        ty.Union[File, ty.List[File], MultiOutputType],
        {"help_string": "output correlation maps in Pearson and/or Z-scores"},
    ),
]
NetCorr_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class NetCorr(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_afni import NCorr
    >>> from pydra.engine.specs import MultiOutputType
    >>> from pydra.tasks.afni.auto.preprocess.net_corr import NetCorr

    >>> task = NetCorr()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.in_rois = Nifti1.mock(None)
    >>> task.inputs.mask = Nifti1.mock(None)
    >>> task.inputs.weight_ts = File.mock()
    >>> task.inputs.fish_z = True
    >>> task.inputs.ts_wb_corr = True
    >>> task.inputs.ts_wb_Z = True
    >>> task.inputs.out_file = NCorr.mock(None)
    >>> task.cmdline
    '3dNetCorr -prefix sub0.tp1.ncorr -fish_z -inset functional.nii -in_rois maps.nii -mask mask.nii -ts_wb_Z -ts_wb_corr'


    """

    input_spec = NetCorr_input_spec
    output_spec = NetCorr_output_spec
    executable = "3dNetCorr"
