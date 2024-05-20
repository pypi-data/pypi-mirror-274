from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
    (
        "in_file",
        Nifti1,
        {
            "help_string": "Original anatomical volume (+orig).The skull is removed by this scriptunless instructed otherwise (-no_ss).",
            "argstr": "-input {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "base",
        str,
        {
            "help_string": "Reference anatomical volume.\nUsually this volume is in some standard space like\nTLRC or MNI space and with afni dataset view of\n(+tlrc).\nPreferably, this reference volume should have had\nthe skull removed but that is not mandatory.\nAFNI's distribution contains several templates.\nFor a longer list, use \"whereami -show_templates\"\nTT_N27+tlrc --> Single subject, skull stripped volume.\nThis volume is also known as\nN27_SurfVol_NoSkull+tlrc elsewhere in\nAFNI and SUMA land.\n(www.loni.ucla.edu, www.bic.mni.mcgill.ca)\nThis template has a full set of FreeSurfer\n(surfer.nmr.mgh.harvard.edu)\nsurface models that can be used in SUMA.\nFor details, see Talairach-related link:\nhttps://afni.nimh.nih.gov/afni/suma\nTT_icbm452+tlrc --> Average volume of 452 normal brains.\nSkull Stripped. (www.loni.ucla.edu)\nTT_avg152T1+tlrc --> Average volume of 152 normal brains.\nSkull Stripped.(www.bic.mni.mcgill.ca)\nTT_EPI+tlrc --> EPI template from spm2, masked as TT_avg152T1\nTT_avg152 and TT_EPI volume sources are from\nSPM's distribution. (www.fil.ion.ucl.ac.uk/spm/)\nIf you do not specify a path for the template, the script\nwill attempt to locate the template AFNI's binaries directory.\nNOTE: These datasets have been slightly modified from\ntheir original size to match the standard TLRC\ndimensions (Jean Talairach and Pierre Tournoux\nCo-Planar Stereotaxic Atlas of the Human Brain\nThieme Medical Publishers, New York, 1988).\nThat was done for internal consistency in AFNI.\nYou may use the original form of these\nvolumes if you choose but your TLRC coordinates\nwill not be consistent with AFNI's TLRC database\n(San Antonio Talairach Daemon database), for example.",
            "argstr": "-base {base}",
            "mandatory": True,
        },
    ),
    (
        "no_ss",
        bool,
        {
            "help_string": "Do not strip skull of input data set\n(because skull has already been removed\nor because template still has the skull)\nNOTE: The ``-no_ss`` option is not all that optional.\nHere is a table of when you should and should not use ``-no_ss``\n\n  +------------------+------------+---------------+\n  | Dataset          | Template                   |\n  +==================+============+===============+\n  |                  | w/ skull   | wo/ skull     |\n  +------------------+------------+---------------+\n  | WITH skull       | ``-no_ss`` | xxx           |\n  +------------------+------------+---------------+\n  | WITHOUT skull    | No Cigar   | ``-no_ss``    |\n  +------------------+------------+---------------+\n\nTemplate means: Your template of choice\nDset. means: Your anatomical dataset\n``-no_ss`` means: Skull stripping should not be attempted on Dset\nxxx means: Don't put anything, the script will strip Dset\nNo Cigar means: Don't try that combination, it makes no sense.",
            "argstr": "-no_ss",
        },
    ),
]
AutoTLRC_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "output file"})]
AutoTLRC_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AutoTLRC(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.afni.auto.preprocess.auto_tlrc import AutoTLRC

    >>> task = AutoTLRC()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.base = "TT_N27+tlrc"
    >>> task.inputs.no_ss = True
    >>> task.cmdline
    '@auto_tlrc -base TT_N27+tlrc -input structural.nii -no_ss'


    """

    input_spec = AutoTLRC_input_spec
    output_spec = AutoTLRC_output_spec
    executable = "@auto_tlrc"
