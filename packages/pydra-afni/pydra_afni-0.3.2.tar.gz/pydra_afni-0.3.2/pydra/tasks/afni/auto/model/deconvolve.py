from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.medimage_afni import OneD
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_files",
        ty.List[Nifti1],
        {
            "help_string": "filenames of 3D+time input datasets. More than one filename can be given and the datasets will be auto-catenated in time. You can input a 1D time series file here, but the time axis should run along the ROW direction, not the COLUMN direction as in the 'input1D' option.",
            "argstr": "-input {in_files}",
            "copyfile": False,
            "position": 1,
            "sep": " ",
        },
    ),
    (
        "sat",
        bool,
        {
            "help_string": "check the dataset time series for initial saturation transients, which should normally have been excised before data analysis.",
            "argstr": "-sat",
            "xor": ["trans"],
        },
    ),
    (
        "trans",
        bool,
        {
            "help_string": "check the dataset time series for initial saturation transients, which should normally have been excised before data analysis.",
            "argstr": "-trans",
            "xor": ["sat"],
        },
    ),
    (
        "noblock",
        bool,
        {
            "help_string": "normally, if you input multiple datasets with 'input', then the separate datasets are taken to be separate image runs that get separate baseline models. Use this options if you want to have the program consider these to be all one big run.* If any of the input dataset has only 1 sub-brick, then this option is automatically invoked!* If the auto-catenation feature isn't used, then this option has no effect, no how, no way.",
            "argstr": "-noblock",
        },
    ),
    (
        "force_TR",
        float,
        {
            "help_string": "use this value instead of the TR in the 'input' dataset. (It's better to fix the input using Refit.)",
            "argstr": "-force_TR {force_TR}",
            "position": 0,
        },
    ),
    (
        "input1D",
        File,
        {
            "help_string": "filename of single (fMRI) .1D time series where time runs down the column.",
            "argstr": "-input1D {input1D}",
        },
    ),
    (
        "TR_1D",
        float,
        {
            "help_string": "TR to use with 'input1D'. This option has no effect if you do not also use 'input1D'.",
            "argstr": "-TR_1D {TR_1D}",
        },
    ),
    (
        "legendre",
        bool,
        {
            "help_string": "use Legendre polynomials for null hypothesis (baseline model)",
            "argstr": "-legendre",
        },
    ),
    (
        "nolegendre",
        bool,
        {
            "help_string": "use power polynomials for null hypotheses. Don't do this unless you are crazy!",
            "argstr": "-nolegendre",
        },
    ),
    (
        "nodmbase",
        bool,
        {"help_string": "don't de-mean baseline time series", "argstr": "-nodmbase"},
    ),
    (
        "dmbase",
        bool,
        {
            "help_string": "de-mean baseline time series (default if 'polort' >= 0)",
            "argstr": "-dmbase",
        },
    ),
    (
        "svd",
        bool,
        {
            "help_string": "use SVD instead of Gaussian elimination (default)",
            "argstr": "-svd",
        },
    ),
    (
        "nosvd",
        bool,
        {"help_string": "use Gaussian elimination instead of SVD", "argstr": "-nosvd"},
    ),
    (
        "rmsmin",
        float,
        {
            "help_string": "minimum rms error to reject reduced model (default = 0; don't use this option normally!)",
            "argstr": "-rmsmin {rmsmin}",
        },
    ),
    (
        "nocond",
        bool,
        {"help_string": "DON'T calculate matrix condition number", "argstr": "-nocond"},
    ),
    (
        "singvals",
        bool,
        {"help_string": "print out the matrix singular values", "argstr": "-singvals"},
    ),
    (
        "goforit",
        int,
        {
            "help_string": "use this to proceed even if the matrix has bad problems (e.g., duplicate columns, large condition number, etc.).",
            "argstr": "-GOFORIT {goforit}",
        },
    ),
    (
        "allzero_OK",
        bool,
        {
            "help_string": "don't consider all zero matrix columns to be the type of error that 'gotforit' is needed to ignore.",
            "argstr": "-allzero_OK",
        },
    ),
    (
        "dname",
        ty.Any,
        {
            "help_string": "set environmental variable to provided value",
            "argstr": "-D{dname[0]}={dname[1]}",
        },
    ),
    (
        "mask",
        File,
        {
            "help_string": "filename of 3D mask dataset; only data time series from within the mask will be analyzed; results for voxels outside the mask will be set to zero.",
            "argstr": "-mask {mask}",
        },
    ),
    (
        "automask",
        bool,
        {
            "help_string": "build a mask automatically from input data (will be slow for long time series datasets)",
            "argstr": "-automask",
        },
    ),
    (
        "STATmask",
        File,
        {
            "help_string": "build a mask from provided file, and use this mask for the purpose of reporting truncation-to float issues AND for computing the FDR curves. The actual results ARE not masked with this option (only with 'mask' or 'automask' options).",
            "argstr": "-STATmask {STATmask}",
        },
    ),
    (
        "censor",
        File,
        {
            "help_string": "filename of censor .1D time series. This is a file of 1s and 0s, indicating which time points are to be included (1) and which are to be excluded (0).",
            "argstr": "-censor {censor}",
        },
    ),
    (
        "polort",
        int,
        {
            "help_string": "degree of polynomial corresponding to the null hypothesis [default: 1]",
            "argstr": "-polort {polort}",
        },
    ),
    (
        "ortvec",
        ty.Any,
        {
            "help_string": "this option lets you input a rectangular array of 1 or more baseline vectors from a file. This method is a fast way to include a lot of baseline regressors in one step. ",
            "argstr": "-ortvec {ortvec[0]} {ortvec[1]}",
        },
    ),
    (
        "x1D",
        OneD,
        {"help_string": "specify name for saved X matrix", "argstr": "-x1D {x1D}"},
    ),
    (
        "x1D_stop",
        bool,
        {
            "help_string": "stop running after writing .xmat.1D file",
            "argstr": "-x1D_stop",
        },
    ),
    (
        "cbucket",
        str,
        {
            "help_string": "Name for dataset in which to save the regression coefficients (no statistics). This dataset will be used in a -xrestore run [not yet implemented] instead of the bucket dataset, if possible.",
            "argstr": "-cbucket {cbucket}",
        },
    ),
    (
        "out_file",
        Nifti1,
        {"help_string": "output statistics file", "argstr": "-bucket {out_file}"},
    ),
    (
        "num_threads",
        int,
        {
            "help_string": "run the program with provided number of sub-processes",
            "argstr": "-jobs {num_threads}",
        },
    ),
    (
        "fout",
        bool,
        {"help_string": "output F-statistic for each stimulus", "argstr": "-fout"},
    ),
    (
        "rout",
        bool,
        {
            "help_string": "output the R^2 statistic for each stimulus",
            "argstr": "-rout",
        },
    ),
    (
        "tout",
        bool,
        {"help_string": "output the T-statistic for each stimulus", "argstr": "-tout"},
    ),
    (
        "vout",
        bool,
        {
            "help_string": "output the sample variance (MSE) for each stimulus",
            "argstr": "-vout",
        },
    ),
    (
        "nofdr",
        bool,
        {
            "help_string": "Don't compute the statistic-vs-FDR curves for the bucket dataset.",
            "argstr": "-noFDR",
        },
    ),
    (
        "global_times",
        bool,
        {
            "help_string": "use global timing for stimulus timing files",
            "argstr": "-global_times",
            "xor": ["local_times"],
        },
    ),
    (
        "local_times",
        bool,
        {
            "help_string": "use local timing for stimulus timing files",
            "argstr": "-local_times",
            "xor": ["global_times"],
        },
    ),
    (
        "num_stimts",
        int,
        {
            "help_string": "number of stimulus timing files",
            "argstr": "-num_stimts {num_stimts}",
            "position": -6,
        },
    ),
    (
        "stim_times",
        list,
        {
            "help_string": "generate a response model from a set of stimulus times given in file.",
            "argstr": "-stim_times {stim_times[0]} {stim_times[1]} '{stim_times[2]}'...",
            "position": -5,
        },
    ),
    (
        "stim_label",
        list,
        {
            "help_string": "label for kth input stimulus (e.g., Label1)",
            "argstr": "-stim_label {stim_label[0]} {stim_label[1]}...",
            "position": -4,
            "requires": ["stim_times"],
        },
    ),
    (
        "stim_times_subtract",
        float,
        {
            "help_string": "this option means to subtract specified seconds from each time encountered in any 'stim_times' option. The purpose of this option is to make it simple to adjust timing files for the removal of images from the start of each imaging run.",
            "argstr": "-stim_times_subtract {stim_times_subtract}",
        },
    ),
    (
        "num_glt",
        int,
        {
            "help_string": "number of general linear tests (i.e., contrasts)",
            "argstr": "-num_glt {num_glt}",
            "position": -3,
        },
    ),
    (
        "gltsym",
        list,
        {
            "help_string": "general linear tests (i.e., contrasts) using symbolic conventions (e.g., '+Label1 -Label2')",
            "argstr": "-gltsym 'SYM: {gltsym}'...",
            "position": -2,
        },
    ),
    (
        "glt_label",
        list,
        {
            "help_string": "general linear test (i.e., contrast) labels",
            "argstr": "-glt_label {glt_label[0]} {glt_label[1]}...",
            "position": -1,
            "requires": ["gltsym"],
        },
    ),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Deconvolve_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_file", Nifti1, {"help_string": "output statistics file"}),
    (
        "reml_script",
        File,
        {"help_string": "automatically generated script to run 3dREMLfit"},
    ),
    ("x1D", OneD, {"help_string": "save out X matrix"}),
    (
        "cbucket",
        File,
        {"help_string": "output regression coefficients file (if generated)"},
    ),
]
Deconvolve_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Deconvolve(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_afni import OneD
    >>> from pydra.tasks.afni.auto.model.deconvolve import Deconvolve

    >>> task = Deconvolve()
    >>> task.inputs.in_files = None
    >>> task.inputs.input1D = File.mock()
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.STATmask = File.mock()
    >>> task.inputs.censor = File.mock()
    >>> task.inputs.x1D = OneD.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.stim_times = stim_times
    >>> task.inputs.stim_label = [(1, "Houses")]
    >>> task.inputs.gltsym = ["SYM: +Houses"]
    >>> task.inputs.glt_label = [(1, "Houses")]
    >>> task.cmdline
    '3dDeconvolve -input functional.nii functional2.nii -bucket output.nii -x1D output.1D -num_stimts 1 -stim_times 1 timeseries.txt "SPMG1(4)" -stim_label 1 Houses -num_glt 1 -gltsym "SYM: +Houses" -glt_label 1 Houses'


    """

    input_spec = Deconvolve_input_spec
    output_spec = Deconvolve_output_spec
    executable = "3dDeconvolve"
