from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input dataset",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "neighborhood",
        ty.Any,
        {
            "help_string": "The region around each voxel that will be extracted for the statistics calculation. Possible regions are: 'SPHERE', 'RHDD' (rhombic dodecahedron), 'TOHD' (truncated octahedron) with a given radius in mm or 'RECT' (rectangular block) with dimensions to specify in mm.",
            "argstr": "-nbhd '{neighborhood[0]}({neighborhood[1]})'",
            "mandatory": True,
        },
    ),
    (
        "stat",
        ty.List[File],
        {
            "help_string": "statistics to compute. Possible names are:\n\n * mean   = average of the values\n * stdev  = standard deviation\n * var    = variance (stdev\\*stdev)\n * cvar   = coefficient of variation = stdev/fabs(mean)\n * median = median of the values\n * MAD    = median absolute deviation\n * min    = minimum\n * max    = maximum\n * absmax = maximum of the absolute values\n * num    = number of the values in the region:\n            with the use of -mask or -automask,\n            the size of the region around any given\n            voxel will vary; this option lets you\n            map that size.  It may be useful if you\n            plan to compute a t-statistic (say) from\n            the mean and stdev outputs.\n * sum    = sum of the values in the region\n * FWHM   = compute (like 3dFWHM) image smoothness\n            inside each voxel's neighborhood.  Results\n            are in 3 sub-bricks: FWHMx, FHWMy, and FWHMz.\n            Places where an output is -1 are locations\n            where the FWHM value could not be computed\n            (e.g., outside the mask).\n * FWHMbar= Compute just the average of the 3 FWHM values\n            (normally would NOT do this with FWHM also).\n * perc:P0:P1:Pstep =\n            Compute percentiles between P0 and P1 with a\n            step of Pstep.\n            Default P1 is equal to P0 and default P2 = 1\n * rank   = rank of the voxel's intensity\n * frank  = rank / number of voxels in neighborhood\n * P2skew = Pearson's second skewness coefficient\n             3 \\* (mean - median) / stdev\n * ALL    = all of the above, in that order\n            (except for FWHMbar and perc).\n * mMP2s  = Exactly the same output as:\n            median, MAD, P2skew,\n            but a little faster\n * mmMP2s = Exactly the same output as:\n            mean, median, MAD, P2skew\n\nMore than one option can be used.",
            "argstr": "-stat {stat}...",
            "mandatory": True,
        },
    ),
    (
        "mask_file",
        NiftiGz,
        {
            "help_string": "Mask image file name. Voxels NOT in the mask will not be used in the neighborhood of any voxel. Also, a voxel NOT in the mask will have its statistic(s) computed as zero (0) unless the parameter 'nonmask' is set to true.",
            "argstr": "-mask {mask_file}",
        },
    ),
    (
        "automask",
        bool,
        {
            "help_string": "Compute the mask as in program 3dAutomask.",
            "argstr": "-automask",
        },
    ),
    (
        "nonmask",
        bool,
        {
            "help_string": "Voxels not in the mask WILL have their local statistics\ncomputed from all voxels in their neighborhood that ARE in\nthe mask. For instance, this option can be used to compute the\naverage local white matter time series, even at non-WM\nvoxels.",
            "argstr": "-use_nonmask",
        },
    ),
    (
        "reduce_grid",
        ty.Any,
        {
            "help_string": "Compute output on a grid that is reduced by the specified factors. If a single value is passed, output is resampled to the specified isotropic grid. Otherwise, the 3 inputs describe the reduction in the X, Y, and Z directions. This option speeds up computations at the expense of resolution. It should only be used when the nbhd is quite large with respect to the input's resolution, and the resultant stats are expected to be smooth.",
            "argstr": "-reduce_grid {reduce_grid}",
            "xor": ["reduce_restore_grid", "reduce_max_vox"],
        },
    ),
    (
        "reduce_restore_grid",
        ty.Any,
        {
            "help_string": "Like reduce_grid, but also resample output back to inputgrid.",
            "argstr": "-reduce_restore_grid {reduce_restore_grid}",
            "xor": ["reduce_max_vox", "reduce_grid"],
        },
    ),
    (
        "reduce_max_vox",
        float,
        {
            "help_string": "Like reduce_restore_grid, but automatically set Rx Ry Rz sothat the computation grid is at a resolution of nbhd/MAX_VOXvoxels.",
            "argstr": "-reduce_max_vox {reduce_max_vox}",
            "xor": ["reduce_restore_grid", "reduce_grid"],
        },
    ),
    (
        "grid_rmode",
        ty.Any,
        {
            "help_string": "Interpolant to use when resampling the output with thereduce_restore_grid option. The resampling method string RESAM should come from the set {'NN', 'Li', 'Cu', 'Bk'}. These stand for 'Nearest Neighbor', 'Linear', 'Cubic', and 'Blocky' interpolation, respectively.",
            "argstr": "-grid_rmode {grid_rmode}",
            "requires": ["reduce_restore_grid"],
        },
    ),
    (
        "quiet",
        bool,
        {
            "help_string": "Stop the highly informative progress reports.",
            "argstr": "-quiet",
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
        "out_file",
        Path,
        {
            "help_string": "Output dataset.",
            "argstr": "-prefix {out_file}",
            "position": 0,
            "output_file_template": "{in_file}_localstat",
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Localstat_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Localstat_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Localstat(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from pydra.tasks.afni.auto.utils.localstat import Localstat

    >>> task = Localstat()
    >>> task.inputs.in_file = Nifti1.mock(None)
    >>> task.inputs.neighborhood = ("SPHERE", 45)
    >>> task.inputs.stat = None
    >>> task.inputs.mask_file = NiftiGz.mock(None)
    >>> task.inputs.nonmask = True
    >>> task.inputs.outputtype = "NIFTI_GZ"
    >>> task.cmdline
    '3dLocalstat -prefix functional_localstat.nii -mask skeleton_mask.nii.gz -nbhd "SPHERE(45.0)" -use_nonmask -stat mean functional.nii'


    """

    input_spec = Localstat_input_spec
    output_spec = Localstat_output_spec
    executable = "3dLocalstat"
