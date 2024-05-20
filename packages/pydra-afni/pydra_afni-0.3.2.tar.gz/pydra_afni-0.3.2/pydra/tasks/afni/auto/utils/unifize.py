from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input file to 3dUnifize",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_file",
        Nifti1,
        {
            "help_string": "output image file name",
            "argstr": "-prefix {out_file}",
            "output_file_template": "{in_file}_unifized",
        },
    ),
    (
        "t2",
        bool,
        {
            "help_string": "Treat the input as if it were T2-weighted, rather than T1-weighted. This processing is done simply by inverting the image contrast, processing it as if that result were T1-weighted, and then re-inverting the results counts of voxel overlap, i.e., each voxel will contain the number of masks that it is set in.",
            "argstr": "-T2",
        },
    ),
    (
        "gm",
        bool,
        {
            "help_string": "Also scale to unifize 'gray matter' = lower intensity voxels (to aid in registering images from different scanners).",
            "argstr": "-GM",
        },
    ),
    (
        "urad",
        float,
        {
            "help_string": "Sets the radius (in voxels) of the ball used for the sneaky trick. Default value is 18.3, and should be changed proportionally if the dataset voxel size differs significantly from 1 mm.",
            "argstr": "-Urad {urad}",
        },
    ),
    (
        "scale_file",
        File,
        {
            "help_string": "output file name to save the scale factor used at each voxel ",
            "argstr": "-ssave {scale_file}",
        },
    ),
    (
        "no_duplo",
        bool,
        {
            "help_string": "Do NOT use the 'duplo down' step; this can be useful for lower resolution datasets.",
            "argstr": "-noduplo",
        },
    ),
    (
        "epi",
        bool,
        {
            "help_string": "Assume the input dataset is a T2 (or T2\\*) weighted EPI time series. After computing the scaling, apply it to ALL volumes (TRs) in the input dataset. That is, a given voxel will be scaled by the same factor at each TR. This option also implies '-noduplo' and '-T2'.This option turns off '-GM' if you turned it on.",
            "argstr": "-EPI",
            "requires": ["no_duplo", "t2"],
            "xor": ["gm"],
        },
    ),
    (
        "rbt",
        ty.Any,
        {
            "help_string": "Option for AFNI experts only.Specify the 3 parameters for the algorithm:\nR = radius; same as given by option '-Urad', [default=18.3]\nb = bottom percentile of normalizing data range, [default=70.0]\nr = top percentile of normalizing data range, [default=80.0]\n",
            "argstr": "-rbt {rbt[0]} {rbt[1]} {rbt[2]}",
        },
    ),
    (
        "t2_up",
        float,
        {
            "help_string": "Option for AFNI experts only.Set the upper percentile point used for T2-T1 inversion. Allowed to be anything between 90 and 100 (inclusive), with default to 98.5  (for no good reason).",
            "argstr": "-T2up {t2_up}",
        },
    ),
    (
        "cl_frac",
        float,
        {
            "help_string": "Option for AFNI experts only.Set the automask 'clip level fraction'. Must be between 0.1 and 0.9. A small fraction means to make the initial threshold for clipping (a la 3dClipLevel) smaller, which will tend to make the mask larger.  [default=0.1]",
            "argstr": "-clfrac {cl_frac}",
        },
    ),
    (
        "quiet",
        bool,
        {"help_string": "Don't print the progress messages.", "argstr": "-quiet"},
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Unifize_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("scale_file", File, {"help_string": "scale factor file"})]
Unifize_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Unifize(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.utils.unifize import Unifize

    >>> task = Unifize()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.out_file = Nifti1.mock(None)
    >>> task.inputs.scale_file = File.mock()
    >>> task.cmdline
    '3dUnifize -prefix structural_unifized.nii -input structural.nii'


    """

    input_spec = Unifize_input_spec
    output_spec = Unifize_output_spec
    executable = "3dUnifize"
