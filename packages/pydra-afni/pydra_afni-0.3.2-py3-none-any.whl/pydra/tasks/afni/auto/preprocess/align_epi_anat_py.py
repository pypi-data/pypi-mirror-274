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
            "help_string": "EPI dataset to align",
            "argstr": "-epi {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "anat",
        Nifti1,
        {
            "help_string": "name of structural dataset",
            "argstr": "-anat {anat}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "epi_base",
        ty.Any,
        {
            "help_string": "the epi base used in alignmentshould be one of (0/mean/median/max/subbrick#)",
            "argstr": "-epi_base {epi_base}",
            "mandatory": True,
        },
    ),
    (
        "anat2epi",
        bool,
        {
            "help_string": "align anatomical to EPI dataset (default)",
            "argstr": "-anat2epi",
        },
    ),
    (
        "epi2anat",
        bool,
        {"help_string": "align EPI to anatomical dataset", "argstr": "-epi2anat"},
    ),
    (
        "save_skullstrip",
        bool,
        {
            "help_string": "save skull-stripped (not aligned)",
            "argstr": "-save_skullstrip",
        },
    ),
    (
        "suffix",
        str,
        "_al",
        {
            "help_string": 'append suffix to the original anat/epi dataset to usein the resulting dataset names (default is "_al")',
            "argstr": "-suffix {suffix}",
        },
    ),
    (
        "epi_strip",
        ty.Any,
        {
            "help_string": "method to mask brain in EPI datashould be one of[3dSkullStrip]/3dAutomask/None)",
            "argstr": "-epi_strip {epi_strip}",
        },
    ),
    (
        "volreg",
        ty.Any,
        "on",
        {
            "help_string": "do volume registration on EPI dataset before alignmentshould be 'on' or 'off', defaults to 'on'",
            "argstr": "-volreg {volreg}",
        },
    ),
    (
        "tshift",
        ty.Any,
        "on",
        {
            "help_string": "do time shifting of EPI dataset before alignmentshould be 'on' or 'off', defaults to 'on'",
            "argstr": "-tshift {tshift}",
        },
    ),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    ("py27_path", ty.Any, "python2", {"help_string": ""}),
]
AlignEpiAnatPy_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "anat_al_orig",
        File,
        {"help_string": "A version of the anatomy that is aligned to the EPI"},
    ),
    (
        "epi_al_orig",
        File,
        {"help_string": "A version of the EPI dataset aligned to the anatomy"},
    ),
    (
        "epi_tlrc_al",
        File,
        {"help_string": "A version of the EPI dataset aligned to a standard template"},
    ),
    ("anat_al_mat", File, {"help_string": "matrix to align anatomy to the EPI"}),
    ("epi_al_mat", File, {"help_string": "matrix to align EPI to anatomy"}),
    ("epi_vr_al_mat", File, {"help_string": "matrix to volume register EPI"}),
    (
        "epi_reg_al_mat",
        File,
        {"help_string": "matrix to volume register and align epi to anatomy"},
    ),
    (
        "epi_al_tlrc_mat",
        File,
        {
            "help_string": "matrix to volume register and align epito anatomy and put into standard space"
        },
    ),
    (
        "epi_vr_motion",
        File,
        {
            "help_string": "motion parameters from EPI time-seriesregistration (tsh included in name if slicetiming correction is also included)."
        },
    ),
    ("skullstrip", File, {"help_string": "skull-stripped (not aligned) volume"}),
]
AlignEpiAnatPy_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AlignEpiAnatPy(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.align_epi_anat_py import AlignEpiAnatPy

    >>> task = AlignEpiAnatPy()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.anat = Nifti1.mock(None)
    >>> task.inputs.epi_base = 0
    >>> task.inputs.save_skullstrip = True
    >>> task.inputs.epi_strip = "3dAutomask"
    >>> task.inputs.volreg = "off"
    >>> task.inputs.tshift = "off"
    >>> task.cmdline
    'python2 ...align_epi_anat.py -anat structural.nii -epi_base 0 -epi_strip 3dAutomask -epi functional.nii -save_skullstrip -suffix _al -tshift off -volreg off'


    """

    input_spec = AlignEpiAnatPy_input_spec
    output_spec = AlignEpiAnatPy_output_spec
    executable = "align_epi_anat.py"


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "EPI dataset to align",
            "argstr": "-epi {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "anat",
        Nifti1,
        {
            "help_string": "name of structural dataset",
            "argstr": "-anat {anat}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "epi_base",
        ty.Any,
        {
            "help_string": "the epi base used in alignmentshould be one of (0/mean/median/max/subbrick#)",
            "argstr": "-epi_base {epi_base}",
            "mandatory": True,
        },
    ),
    (
        "anat2epi",
        bool,
        {
            "help_string": "align anatomical to EPI dataset (default)",
            "argstr": "-anat2epi",
        },
    ),
    (
        "epi2anat",
        bool,
        {"help_string": "align EPI to anatomical dataset", "argstr": "-epi2anat"},
    ),
    (
        "save_skullstrip",
        bool,
        {
            "help_string": "save skull-stripped (not aligned)",
            "argstr": "-save_skullstrip",
        },
    ),
    (
        "suffix",
        str,
        "_al",
        {
            "help_string": 'append suffix to the original anat/epi dataset to usein the resulting dataset names (default is "_al")',
            "argstr": "-suffix {suffix}",
        },
    ),
    (
        "epi_strip",
        ty.Any,
        {
            "help_string": "method to mask brain in EPI datashould be one of[3dSkullStrip]/3dAutomask/None)",
            "argstr": "-epi_strip {epi_strip}",
        },
    ),
    (
        "volreg",
        ty.Any,
        "on",
        {
            "help_string": "do volume registration on EPI dataset before alignmentshould be 'on' or 'off', defaults to 'on'",
            "argstr": "-volreg {volreg}",
        },
    ),
    (
        "tshift",
        ty.Any,
        "on",
        {
            "help_string": "do time shifting of EPI dataset before alignmentshould be 'on' or 'off', defaults to 'on'",
            "argstr": "-tshift {tshift}",
        },
    ),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    ("py27_path", ty.Any, "python2", {"help_string": ""}),
]
align_epi_anat_py_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "anat_al_orig",
        File,
        {"help_string": "A version of the anatomy that is aligned to the EPI"},
    ),
    (
        "epi_al_orig",
        File,
        {"help_string": "A version of the EPI dataset aligned to the anatomy"},
    ),
    (
        "epi_tlrc_al",
        File,
        {"help_string": "A version of the EPI dataset aligned to a standard template"},
    ),
    ("anat_al_mat", File, {"help_string": "matrix to align anatomy to the EPI"}),
    ("epi_al_mat", File, {"help_string": "matrix to align EPI to anatomy"}),
    ("epi_vr_al_mat", File, {"help_string": "matrix to volume register EPI"}),
    (
        "epi_reg_al_mat",
        File,
        {"help_string": "matrix to volume register and align epi to anatomy"},
    ),
    (
        "epi_al_tlrc_mat",
        File,
        {
            "help_string": "matrix to volume register and align epito anatomy and put into standard space"
        },
    ),
    (
        "epi_vr_motion",
        File,
        {
            "help_string": "motion parameters from EPI time-seriesregistration (tsh included in name if slicetiming correction is also included)."
        },
    ),
    ("skullstrip", File, {"help_string": "skull-stripped (not aligned) volume"}),
]
align_epi_anat_py_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class align_epi_anat_py(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.align_epi_anat_py import align_epi_anat_py

    >>> task = align_epi_anat_py()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.anat = Nifti1.mock(None)
    >>> task.inputs.epi_base = 0
    >>> task.inputs.save_skullstrip = True
    >>> task.inputs.epi_strip = "3dAutomask"
    >>> task.inputs.volreg = "off"
    >>> task.inputs.tshift = "off"
    >>> task.cmdline
    'python2 ...align_epi_anat.py -anat structural.nii -epi_base 0 -epi_strip 3dAutomask -epi functional.nii -save_skullstrip -suffix _al -tshift off -volreg off'


    """

    input_spec = align_epi_anat_py_input_spec
    output_spec = align_epi_anat_py_output_spec
    executable = "align_epi_anat.py"
