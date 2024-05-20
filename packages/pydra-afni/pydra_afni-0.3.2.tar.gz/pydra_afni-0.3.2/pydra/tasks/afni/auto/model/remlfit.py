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
            "help_string": "Read time series dataset",
            "argstr": '-input "{in_files}"',
            "copyfile": False,
            "mandatory": True,
            "sep": " ",
        },
    ),
    (
        "matrix",
        OneD,
        {
            "help_string": "the design matrix file, which should have been output from Deconvolve via the 'x1D' option",
            "argstr": "-matrix {matrix}",
            "mandatory": True,
        },
    ),
    (
        "polort",
        int,
        {
            "help_string": "if no 'matrix' option is given, AND no 'matim' option, create a matrix with Legendre polynomial regressorsup to the specified order. The default value is 0, whichproduces a matrix with a single column of all ones",
            "argstr": "-polort {polort}",
            "xor": ["matrix"],
        },
    ),
    (
        "matim",
        File,
        {
            "help_string": "read a standard file as the matrix. You can use only Col as a name in GLTs with these nonstandard matrix input methods, since the other names come from the 'matrix' file. These mutually exclusive options are ignored if 'matrix' is used.",
            "argstr": "-matim {matim}",
            "xor": ["matrix"],
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
        False,
        {
            "help_string": "build a mask automatically from input data (will be slow for long time series datasets)",
            "argstr": "-automask",
        },
    ),
    (
        "STATmask",
        File,
        {
            "help_string": "filename of 3D mask dataset to be used for the purpose of reporting truncation-to float issues AND for computing the FDR curves. The actual results ARE not masked with this option (only with 'mask' or 'automask' options).",
            "argstr": "-STATmask {STATmask}",
        },
    ),
    (
        "addbase",
        ty.List[File],
        {
            "help_string": "file(s) to add baseline model columns to the matrix with this option. Each column in the specified file(s) will be appended to the matrix. File(s) must have at least as many rows as the matrix does.",
            "argstr": "-addbase {addbase}",
            "copyfile": False,
            "sep": " ",
        },
    ),
    (
        "slibase",
        ty.List[File],
        {
            "help_string": "similar to 'addbase' in concept, BUT each specified file must have an integer multiple of the number of slices in the input dataset(s); then, separate regression matrices are generated for each slice, with the first column of the file appended to the matrix for the first slice of the dataset, the second column of the file appended to the matrix for the first slice of the dataset, and so on. Intended to help model physiological noise in FMRI, or other effects you want to regress out that might change significantly in the inter-slice time intervals. This will slow the program down, and make it use a lot more memory (to hold all the matrix stuff).",
            "argstr": "-slibase {slibase}",
        },
    ),
    (
        "slibase_sm",
        ty.List[File],
        {
            "help_string": "similar to 'slibase', BUT each file much be in slice major order (i.e. all slice0 columns come first, then all slice1 columns, etc).",
            "argstr": "-slibase_sm {slibase_sm}",
        },
    ),
    (
        "usetemp",
        bool,
        {
            "help_string": "write intermediate stuff to disk, to economize on RAM. Using this option might be necessary to run with 'slibase' and with 'Grid' values above the default, since the program has to store a large number of matrices for such a problem: two for every slice and for every (a,b) pair in the ARMA parameter grid. Temporary files are written to the directory given in environment variable TMPDIR, or in /tmp, or in ./ (preference is in that order)",
            "argstr": "-usetemp",
        },
    ),
    (
        "nodmbase",
        bool,
        {
            "help_string": "by default, baseline columns added to the matrix via 'addbase' or 'slibase' or 'dsort' will each have their mean removed (as is done in Deconvolve); this option turns this centering off",
            "argstr": "-nodmbase",
            "requires": ["addbase", "dsort"],
        },
    ),
    (
        "dsort",
        File,
        {
            "help_string": "4D dataset to be used as voxelwise baseline regressor",
            "argstr": "-dsort {dsort}",
            "copyfile": False,
        },
    ),
    (
        "dsort_nods",
        bool,
        {
            "help_string": "if 'dsort' option is used, this command will output additional results files excluding the 'dsort' file",
            "argstr": "-dsort_nods",
            "requires": ["dsort"],
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
        {
            "help_string": "output the T-statistic for each stimulus; if you use 'out_file' and do not give any of 'fout', 'tout',or 'rout', then the program assumes 'fout' is activated.",
            "argstr": "-tout",
        },
    ),
    (
        "nofdr",
        bool,
        {
            "help_string": "do NOT add FDR curve data to bucket datasets; FDR curves can take a long time if 'tout' is used",
            "argstr": "-noFDR",
        },
    ),
    (
        "nobout",
        bool,
        {
            "help_string": "do NOT add baseline (null hypothesis) regressor betas to the 'rbeta_file' and/or 'obeta_file' output datasets.",
            "argstr": "-nobout",
        },
    ),
    (
        "gltsym",
        list,
        {
            "help_string": "read a symbolic GLT from input file and associate it with a label. As in Deconvolve, you can also use the 'SYM:' method to provide the definition of the GLT directly as a string (e.g., with 'SYM: +Label1 -Label2'). Unlike Deconvolve, you MUST specify 'SYM: ' if providing the GLT directly as a string instead of from a file",
            "argstr": '-gltsym "{gltsym[0]}" {gltsym[1]}...',
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output dataset for beta + statistics from the REML estimation; also contains the results of any GLT analysis requested in the Deconvolve setup, similar to the 'bucket' output from Deconvolve. This dataset does NOT get the betas (or statistics) of those regressors marked as 'baseline' in the matrix file.",
            "argstr": "-Rbuck {out_file}",
        },
    ),
    (
        "var_file",
        File,
        {
            "help_string": "output dataset for REML variance parameters",
            "argstr": "-Rvar {var_file}",
        },
    ),
    (
        "rbeta_file",
        File,
        {
            "help_string": "output dataset for beta weights from the REML estimation, similar to the 'cbucket' output from Deconvolve. This dataset will contain all the beta weights, for baseline and stimulus regressors alike, unless the '-nobout' option is given -- in that case, this dataset will only get the betas for the stimulus regressors.",
            "argstr": "-Rbeta {rbeta_file}",
        },
    ),
    (
        "glt_file",
        File,
        {
            "help_string": "output dataset for beta + statistics from the REML estimation, but ONLY for the GLTs added on the REMLfit command line itself via 'gltsym'; GLTs from Deconvolve's command line will NOT be included.",
            "argstr": "-Rglt {glt_file}",
        },
    ),
    (
        "fitts_file",
        File,
        {
            "help_string": "output dataset for REML fitted model",
            "argstr": "-Rfitts {fitts_file}",
        },
    ),
    (
        "errts_file",
        File,
        {
            "help_string": "output dataset for REML residuals = data - fitted model",
            "argstr": "-Rerrts {errts_file}",
        },
    ),
    (
        "wherr_file",
        File,
        {
            "help_string": "dataset for REML residual, whitened using the estimated ARMA(1,1) correlation matrix of the noise",
            "argstr": "-Rwherr {wherr_file}",
        },
    ),
    (
        "quiet",
        bool,
        {"help_string": "turn off most progress messages", "argstr": "-quiet"},
    ),
    (
        "verb",
        bool,
        {
            "help_string": "turns on more progress messages, including memory usage progress reports at various stages",
            "argstr": "-verb",
        },
    ),
    (
        "goforit",
        bool,
        {
            "help_string": "With potential issues flagged in the design matrix, an attempt will nevertheless be made to fit the model",
            "argstr": "-GOFORIT",
        },
    ),
    (
        "ovar",
        File,
        {
            "help_string": "dataset for OLSQ st.dev. parameter (kind of boring)",
            "argstr": "-Ovar {ovar}",
        },
    ),
    (
        "obeta",
        File,
        {
            "help_string": "dataset for beta weights from the OLSQ estimation",
            "argstr": "-Obeta {obeta}",
        },
    ),
    (
        "obuck",
        File,
        {
            "help_string": "dataset for beta + statistics from the OLSQ estimation",
            "argstr": "-Obuck {obuck}",
        },
    ),
    (
        "oglt",
        File,
        {
            "help_string": "dataset for beta + statistics from 'gltsym' options",
            "argstr": "-Oglt {oglt}",
        },
    ),
    (
        "ofitts",
        File,
        {"help_string": "dataset for OLSQ fitted model", "argstr": "-Ofitts {ofitts}"},
    ),
    (
        "oerrts",
        File,
        {
            "help_string": "dataset for OLSQ residuals (data - fitted model)",
            "argstr": "-Oerrts {oerrts}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Remlfit_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_file",
        Nifti1,
        {
            "help_string": "dataset for beta + statistics from the REML estimation (if generated"
        },
    ),
    (
        "var_file",
        File,
        {"help_string": "dataset for REML variance parameters (if generated)"},
    ),
    (
        "rbeta_file",
        File,
        {
            "help_string": "output dataset for beta weights from the REML estimation (if generated"
        },
    ),
    (
        "glt_file",
        File,
        {
            "help_string": "output dataset for beta + statistics from the REML estimation, but ONLY for the GLTs added on the REMLfit command line itself via 'gltsym' (if generated)"
        },
    ),
    (
        "fitts_file",
        File,
        {"help_string": "output dataset for REML fitted model (if generated)"},
    ),
    (
        "errts_file",
        File,
        {
            "help_string": "output dataset for REML residuals = data - fitted model (if generated"
        },
    ),
    (
        "wherr_file",
        File,
        {
            "help_string": "dataset for REML residual, whitened using the estimated ARMA(1,1) correlation matrix of the noise (if generated)"
        },
    ),
    (
        "ovar",
        File,
        {"help_string": "dataset for OLSQ st.dev. parameter (if generated)"},
    ),
    (
        "obeta",
        File,
        {
            "help_string": "dataset for beta weights from the OLSQ estimation (if generated)"
        },
    ),
    (
        "obuck",
        File,
        {
            "help_string": "dataset for beta + statistics from the OLSQ estimation (if generated)"
        },
    ),
    (
        "oglt",
        File,
        {
            "help_string": "dataset for beta + statistics from 'gltsym' options (if generated"
        },
    ),
    ("ofitts", File, {"help_string": "dataset for OLSQ fitted model (if generated)"}),
    (
        "oerrts",
        File,
        {
            "help_string": "dataset for OLSQ residuals = data - fitted model (if generated"
        },
    ),
]
Remlfit_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Remlfit(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_afni import OneD
    >>> from pydra.tasks.afni.auto.model.remlfit import Remlfit

    >>> task = Remlfit()
    >>> task.inputs.in_files = None
    >>> task.inputs.matrix = OneD.mock(None)
    >>> task.inputs.matim = File.mock()
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.STATmask = File.mock()
    >>> task.inputs.dsort = File.mock()
    >>> task.inputs.gltsym = [("SYM: +Lab1 -Lab2", "TestSYM"), ("timeseries.txt", "TestFile")]
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.var_file = File.mock()
    >>> task.inputs.rbeta_file = File.mock()
    >>> task.inputs.glt_file = File.mock()
    >>> task.inputs.fitts_file = File.mock()
    >>> task.inputs.errts_file = File.mock()
    >>> task.inputs.wherr_file = File.mock()
    >>> task.inputs.ovar = File.mock()
    >>> task.inputs.obeta = File.mock()
    >>> task.inputs.obuck = File.mock()
    >>> task.inputs.oglt = File.mock()
    >>> task.inputs.ofitts = File.mock()
    >>> task.inputs.oerrts = File.mock()
    >>> task.cmdline
    '3dREMLfit -gltsym "SYM: +Lab1 -Lab2" TestSYM -gltsym "timeseries.txt" TestFile -input "functional.nii functional2.nii" -matrix output.1D -Rbuck output.nii'


    """

    input_spec = Remlfit_input_spec
    output_spec = Remlfit_output_spec
    executable = "3dREMLfit"
