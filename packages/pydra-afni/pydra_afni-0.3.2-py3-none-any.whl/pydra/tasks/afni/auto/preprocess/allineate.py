from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dAllineate",
            "argstr": "-source {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "reference",
        Nifti1,
        {
            "help_string": "file to be used as reference, the first volume will be used if not given the reference will be the first volume of in_file.",
            "argstr": "-base {reference}",
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output file from 3dAllineate",
            "argstr": "-prefix {out_file}",
            "xor": ["allcostx"],
            "output_file_template": "{in_file}_allineate",
        },
    ),
    (
        "out_param_file",
        File,
        {
            "help_string": "Save the warp parameters in ASCII (.1D) format.",
            "argstr": "-1Dparam_save {out_param_file}",
            "xor": ["in_param_file", "allcostx"],
        },
    ),
    (
        "in_param_file",
        File,
        {
            "help_string": "Read warp parameters from file and apply them to the source dataset, and produce a new dataset",
            "argstr": "-1Dparam_apply {in_param_file}",
            "xor": ["out_param_file"],
        },
    ),
    (
        "out_matrix",
        File,
        {
            "help_string": "Save the transformation matrix for each volume.",
            "argstr": "-1Dmatrix_save {out_matrix}",
            "xor": ["in_matrix", "allcostx"],
        },
    ),
    (
        "in_matrix",
        TextMatrix,
        {
            "help_string": "matrix to align input file",
            "argstr": "-1Dmatrix_apply {in_matrix}",
            "position": -3,
            "xor": ["out_matrix"],
        },
    ),
    (
        "overwrite",
        bool,
        {
            "help_string": "overwrite output file if it already exists",
            "argstr": "-overwrite",
        },
    ),
    (
        "allcostx",
        TextFile,
        {
            "help_string": "Compute and print ALL available cost functionals for the un-warped inputsAND THEN QUIT. If you use this option none of the other expected outputs will be produced",
            "argstr": "-allcostx |& tee {allcostx}",
            "position": -1,
            "xor": ["out_file", "out_matrix", "out_param_file", "out_weight_file"],
        },
    ),
    (
        "cost",
        ty.Any,
        {
            "help_string": "Defines the 'cost' function that defines the matching between the source and the base",
            "argstr": "-cost {cost}",
        },
    ),
    (
        "interpolation",
        ty.Any,
        {
            "help_string": "Defines interpolation method to use during matching",
            "argstr": "-interp {interpolation}",
        },
    ),
    (
        "final_interpolation",
        ty.Any,
        {
            "help_string": "Defines interpolation method used to create the output dataset",
            "argstr": "-final {final_interpolation}",
        },
    ),
    (
        "nmatch",
        int,
        {
            "help_string": "Use at most n scattered points to match the datasets.",
            "argstr": "-nmatch {nmatch}",
        },
    ),
    (
        "no_pad",
        bool,
        {
            "help_string": "Do not use zero-padding on the base image.",
            "argstr": "-nopad",
        },
    ),
    (
        "zclip",
        bool,
        {
            "help_string": "Replace negative values in the input datasets (source & base) with zero.",
            "argstr": "-zclip",
        },
    ),
    (
        "convergence",
        float,
        {
            "help_string": "Convergence test in millimeters (default 0.05mm).",
            "argstr": "-conv {convergence}",
        },
    ),
    ("usetemp", bool, {"help_string": "temporary file use", "argstr": "-usetemp"}),
    (
        "check",
        list,
        {
            "help_string": "After cost functional optimization is done, start at the final parameters and RE-optimize using this new cost functions. If the results are too different, a warning message will be printed. However, the final parameters from the original optimization will be used to create the output dataset.",
            "argstr": "-check {check}",
        },
    ),
    (
        "one_pass",
        bool,
        {
            "help_string": "Use only the refining pass -- do not try a coarse resolution pass first.  Useful if you know that only small amounts of image alignment are needed.",
            "argstr": "-onepass",
        },
    ),
    (
        "two_pass",
        bool,
        {
            "help_string": "Use a two pass alignment strategy for all volumes, searching for a large rotation+shift and then refining the alignment.",
            "argstr": "-twopass",
        },
    ),
    (
        "two_blur",
        float,
        {
            "help_string": "Set the blurring radius for the first pass in mm.",
            "argstr": "-twoblur {two_blur}",
        },
    ),
    (
        "two_first",
        bool,
        {
            "help_string": "Use -twopass on the first image to be registered, and then on all subsequent images from the source dataset, use results from the first image's coarse pass to start the fine pass.",
            "argstr": "-twofirst",
        },
    ),
    (
        "two_best",
        int,
        {
            "help_string": "In the coarse pass, use the best 'bb' set of initialpoints to search for the starting point for the finepass.  If bb==0, then no search is made for the beststarting point, and the identity transformation isused as the starting point.  [Default=5; min=0 max=11]",
            "argstr": "-twobest {two_best}",
        },
    ),
    (
        "fine_blur",
        float,
        {
            "help_string": "Set the blurring radius to use in the fine resolution pass to 'x' mm.  A small amount (1-2 mm?) of blurring at the fine step may help with convergence, if there is some problem, especially if the base volume is very noisy. [Default == 0 mm = no blurring at the final alignment pass]",
            "argstr": "-fineblur {fine_blur}",
        },
    ),
    (
        "center_of_mass",
        str,
        {
            "help_string": "Use the center-of-mass calculation to bracket the shifts.",
            "argstr": "-cmass{center_of_mass}",
        },
    ),
    (
        "autoweight",
        str,
        {
            "help_string": "Compute a weight function using the 3dAutomask algorithm plus some blurring of the base image.",
            "argstr": "-autoweight{autoweight}",
        },
    ),
    (
        "automask",
        int,
        {
            "help_string": "Compute a mask function, set a value for dilation or 0.",
            "argstr": "-automask+{automask}",
        },
    ),
    (
        "autobox",
        bool,
        {
            "help_string": "Expand the -automask function to enclose a rectangular box that holds the irregular mask.",
            "argstr": "-autobox",
        },
    ),
    (
        "nomask",
        bool,
        {
            "help_string": "Don't compute the autoweight/mask; if -weight is not also used, then every voxel will be counted equally.",
            "argstr": "-nomask",
        },
    ),
    (
        "weight_file",
        File,
        {
            "help_string": "Set the weighting for each voxel in the base dataset; larger weights mean that voxel count more in the cost function. Must be defined on the same grid as the base dataset",
            "argstr": "-weight {weight_file}",
        },
    ),
    (
        "weight",
        ty.Any,
        {
            "help_string": "Set the weighting for each voxel in the base dataset; larger weights mean that voxel count more in the cost function. If an image file is given, the volume must be defined on the same grid as the base dataset",
            "argstr": "-weight {weight}",
        },
    ),
    (
        "out_weight_file",
        File,
        {
            "help_string": "Write the weight volume to disk as a dataset",
            "argstr": "-wtprefix {out_weight_file}",
            "xor": ["allcostx"],
        },
    ),
    (
        "source_mask",
        File,
        {
            "help_string": "mask the input dataset",
            "argstr": "-source_mask {source_mask}",
        },
    ),
    (
        "source_automask",
        int,
        {
            "help_string": "Automatically mask the source dataset with dilation or 0.",
            "argstr": "-source_automask+{source_automask}",
        },
    ),
    (
        "warp_type",
        ty.Any,
        {"help_string": "Set the warp type.", "argstr": "-warp {warp_type}"},
    ),
    (
        "warpfreeze",
        bool,
        {
            "help_string": "Freeze the non-rigid body parameters after first volume.",
            "argstr": "-warpfreeze",
        },
    ),
    (
        "replacebase",
        bool,
        {
            "help_string": "If the source has more than one volume, then after the first volume is aligned to the base.",
            "argstr": "-replacebase",
        },
    ),
    (
        "replacemeth",
        ty.Any,
        {
            "help_string": "After first volume is aligned, switch method for later volumes. For use with '-replacebase'.",
            "argstr": "-replacemeth {replacemeth}",
        },
    ),
    (
        "epi",
        bool,
        {
            "help_string": "Treat the source dataset as being composed of warped EPI slices, and the base as comprising anatomically 'true' images.  Only phase-encoding direction image shearing and scaling will be allowed with this option.",
            "argstr": "-EPI",
        },
    ),
    (
        "maxrot",
        float,
        {
            "help_string": "Maximum allowed rotation in degrees.",
            "argstr": "-maxrot {maxrot}",
        },
    ),
    (
        "maxshf",
        float,
        {"help_string": "Maximum allowed shift in mm.", "argstr": "-maxshf {maxshf}"},
    ),
    (
        "maxscl",
        float,
        {
            "help_string": "Maximum allowed scaling factor.",
            "argstr": "-maxscl {maxscl}",
        },
    ),
    (
        "maxshr",
        float,
        {
            "help_string": "Maximum allowed shearing factor.",
            "argstr": "-maxshr {maxshr}",
        },
    ),
    (
        "master",
        File,
        {
            "help_string": "Write the output dataset on the same grid as this file.",
            "argstr": "-master {master}",
        },
    ),
    (
        "newgrid",
        float,
        {
            "help_string": "Write the output dataset using isotropic grid spacing in mm.",
            "argstr": "-newgrid {newgrid}",
        },
    ),
    (
        "nwarp",
        ty.Any,
        {
            "help_string": "Experimental nonlinear warping: bilinear or legendre poly.",
            "argstr": "-nwarp {nwarp}",
        },
    ),
    (
        "nwarp_fixmot",
        list,
        {
            "help_string": "To fix motion along directions.",
            "argstr": "-nwarp_fixmot{nwarp_fixmot}...",
        },
    ),
    (
        "nwarp_fixdep",
        list,
        {
            "help_string": "To fix non-linear warp dependency along directions.",
            "argstr": "-nwarp_fixdep{nwarp_fixdep}...",
        },
    ),
    (
        "verbose",
        bool,
        {"help_string": "Print out verbose progress reports.", "argstr": "-verb"},
    ),
    (
        "quiet",
        bool,
        {
            "help_string": "Don't print out verbose progress reports.",
            "argstr": "-quiet",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Allineate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_matrix", File, {"help_string": "matrix to align input file"}),
    ("out_param_file", File, {"help_string": "warp parameters"}),
    ("out_weight_file", File, {"help_string": "weight volume"}),
    (
        "allcostx",
        TextFile,
        {
            "help_string": "Compute and print ALL available cost functionals for the un-warped inputs"
        },
    ),
]
Allineate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Allineate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.afni.auto.preprocess.allineate import Allineate

    >>> task = Allineate()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.reference = Nifti1.mock()
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.out_param_file = File.mock()
    >>> task.inputs.in_param_file = File.mock()
    >>> task.inputs.out_matrix = File.mock()
    >>> task.inputs.in_matrix = TextMatrix.mock(None)
    >>> task.inputs.allcostx = TextFile.mock()
    >>> task.inputs.weight_file = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.source_mask = File.mock()
    >>> task.inputs.master = File.mock()
    >>> task.cmdline
    '3dAllineate -source functional.nii -prefix functional_allineate.nii -1Dmatrix_apply cmatrix.mat'


    >>> task = Allineate()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.reference = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock()
    >>> task.inputs.out_param_file = File.mock()
    >>> task.inputs.in_param_file = File.mock()
    >>> task.inputs.out_matrix = File.mock()
    >>> task.inputs.in_matrix = TextMatrix.mock()
    >>> task.inputs.allcostx = TextFile.mock(None)
    >>> task.inputs.weight_file = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.source_mask = File.mock()
    >>> task.inputs.master = File.mock()
    >>> task.cmdline
    '3dAllineate -source functional.nii -base structural.nii -allcostx |& tee out.allcostX.txt'


    >>> task = Allineate()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.reference = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock()
    >>> task.inputs.out_param_file = File.mock()
    >>> task.inputs.in_param_file = File.mock()
    >>> task.inputs.out_matrix = File.mock()
    >>> task.inputs.in_matrix = TextMatrix.mock()
    >>> task.inputs.allcostx = TextFile.mock()
    >>> task.inputs.weight_file = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.source_mask = File.mock()
    >>> task.inputs.master = File.mock()
    >>> task.inputs.nwarp_fixmot = ["X", "Y"]
    >>> task.cmdline
    '3dAllineate -source functional.nii -nwarp_fixmotX -nwarp_fixmotY -prefix functional_allineate -base structural.nii'


    """

    input_spec = Allineate_input_spec
    output_spec = Allineate_output_spec
    executable = "3dAllineate"
