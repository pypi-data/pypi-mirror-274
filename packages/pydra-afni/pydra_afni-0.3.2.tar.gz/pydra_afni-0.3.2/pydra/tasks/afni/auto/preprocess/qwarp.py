from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
from fileformats.medimage_afni import Head
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        ty.Union[Nifti1, NiftiGz],
        {
            "help_string": "Source image (opposite phase encoding direction than base image).",
            "argstr": "-source {in_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "base_file",
        ty.Union[Nifti1, NiftiGz],
        {
            "help_string": "Base image (opposite phase encoding direction than source image).",
            "argstr": "-base {base_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "out_file",
        NiftiGz,
        {
            "help_string": "Sets the prefix/suffix for the output datasets.\n\n* The source dataset is warped to match the base\n  and gets prefix 'ppp'. (Except if '-plusminus' is used\n* The final interpolation to this output dataset is\n  done using the 'wsinc5' method.  See the output of\n  3dAllineate -HELP\n  (in the \"Modifying '-final wsinc5'\" section) for\n  the lengthy technical details.\n* The 3D warp used is saved in a dataset with\n  prefix 'ppp_WARP' -- this dataset can be used\n  with 3dNwarpApply and 3dNwarpCat, for example.\n* To be clear, this is the warp from source dataset\n  coordinates to base dataset coordinates, where the\n  values at each base grid point are the xyz displacements\n  needed to move that grid point's xyz values to the\n  corresponding xyz values in the source dataset:\n  base( (x,y,z) + WARP(x,y,z) ) matches source(x,y,z)\n  Another way to think of this warp is that it 'pulls'\n  values back from source space to base space.\n* 3dNwarpApply would use 'ppp_WARP' to transform datasets\n  aligned with the source dataset to be aligned with the\n  base dataset.\n\n**If you do NOT want this warp saved, use the option '-nowarp'**.\n(However, this warp is usually the most valuable possible output!)\n\n* If you want to calculate and save the inverse 3D warp,\n  use the option '-iwarp'.  This inverse warp will then be\n  saved in a dataset with prefix 'ppp_WARPINV'.\n* This inverse warp could be used to transform data from base\n  space to source space, if you need to do such an operation.\n* You can easily compute the inverse later, say by a command like\n  3dNwarpCat -prefix Z_WARPINV 'INV(Z_WARP+tlrc)'\n  or the inverse can be computed as needed in 3dNwarpApply, like\n  3dNwarpApply -nwarp 'INV(Z_WARP+tlrc)' -source Dataset.nii ...\n\n",
            "argstr": "-prefix {out_file}",
        },
    ),
    (
        "resample",
        bool,
        {
            "help_string": "This option simply resamples the source dataset to match the\nbase dataset grid.  You can use this if the two datasets\noverlap well (as seen in the AFNI GUI), but are not on the\nsame 3D grid.\n\n* If they don't overlap well, allineate them first\n* The reampling here is done with the\n  'wsinc5' method, which has very little blurring artifact.\n* If the base and source datasets ARE on the same 3D grid,\n  then the -resample option will be ignored.\n* You CAN use -resample with these 3dQwarp options:\n  -plusminus  -inilev  -iniwarp  -duplo\n\n",
            "argstr": "-resample",
        },
    ),
    (
        "allineate",
        bool,
        {
            "help_string": "This option will make 3dQwarp run 3dAllineate first, to align the source dataset to the base with an affine transformation. It will then use that alignment as a starting point for the nonlinear warping.",
            "argstr": "-allineate",
        },
    ),
    (
        "allineate_opts",
        str,
        {
            "help_string": "add extra options to the 3dAllineate command to be run by 3dQwarp.",
            "argstr": "-allineate_opts {allineate_opts}",
            "requires": ["allineate"],
        },
    ),
    (
        "nowarp",
        bool,
        {"help_string": "Do not save the _WARP file.", "argstr": "-nowarp"},
    ),
    (
        "iwarp",
        bool,
        {
            "help_string": "Do compute and save the _WARPINV file.",
            "argstr": "-iwarp",
            "xor": ["plusminus"],
        },
    ),
    (
        "pear",
        bool,
        {
            "help_string": "Use strict Pearson correlation for matching.Not usually recommended, since the 'clipped Pearson' methodused by default will reduce the impact of outlier values.",
            "argstr": "-pear",
        },
    ),
    (
        "noneg",
        bool,
        {
            "help_string": "Replace negative values in either input volume with 0.\n\n* If there ARE negative input values, and you do NOT use -noneg,\n  then strict Pearson correlation will be used, since the 'clipped'\n  method only is implemented for non-negative volumes.\n* '-noneg' is not the default, since there might be situations where\n  you want to align datasets with positive and negative values mixed.\n* But, in many cases, the negative values in a dataset are just the\n  result of interpolation artifacts (or other peculiarities), and so\n  they should be ignored.  That is what '-noneg' is for.\n\n",
            "argstr": "-noneg",
        },
    ),
    (
        "nopenalty",
        bool,
        {
            "help_string": "Replace negative values in either input volume with 0.\n\n* If there ARE negative input values, and you do NOT use -noneg,\n  then strict Pearson correlation will be used, since the 'clipped'\n  method only is implemented for non-negative volumes.\n* '-noneg' is not the default, since there might be situations where\n  you want to align datasets with positive and negative values mixed.\n* But, in many cases, the negative values in a dataset are just the\n  result of interpolation artifacts (or other peculiarities), and so\n  they should be ignored. That is what '-noneg' is for.\n\n",
            "argstr": "-nopenalty",
        },
    ),
    (
        "penfac",
        float,
        {
            "help_string": "Use this value to weight the penalty.\nThe default value is 1. Larger values mean the\npenalty counts more, reducing grid distortions,\ninsha'Allah; '-nopenalty' is the same as '-penfac 0'.\nIn 23 Sep 2013 Zhark increased the default value of\nthe penalty by a factor of 5, and also made it get\nprogressively larger with each level of refinement.\nThus, warping results will vary from earlier instances\nof 3dQwarp.\n\n* The progressive increase in the penalty at higher levels\n  means that the 'cost function' can actually look like the\n  alignment is getting worse when the levels change.\n* IF you wish to turn off this progression, for whatever\n  reason (e.g., to keep compatibility with older results),\n  use the option '-penold'.To be completely compatible with\n  the older 3dQwarp, you'll also have to use '-penfac 0.2'.\n\n",
            "argstr": "-penfac {penfac}",
        },
    ),
    (
        "noweight",
        bool,
        {
            "help_string": "If you want a binary weight (the old default), use this option.That is, each voxel in the base volume automask will beweighted the same in the computation of the cost functional.",
            "argstr": "-noweight",
        },
    ),
    (
        "weight",
        File,
        {
            "help_string": "Instead of computing the weight from the base dataset,directly input the weight volume from dataset 'www'.Useful if you know what over parts of the base image youwant to emphasize or de-emphasize the matching functional.",
            "argstr": "-weight {weight}",
        },
    ),
    (
        "wball",
        list,
        {
            "help_string": "\"``-wball x y z r f``\nEnhance automatic weight from '-useweight' by a factor\nof 1+f\\*Gaussian(FWHM=r) centered in the base image at\nDICOM coordinates (x,y,z) and with radius 'r'. The\ngoal of this option is to try and make the alignment\nbetter in a specific part of the brain.\nExample:  -wball 0 14 6 30 40\nto emphasize the thalamic area (in MNI/Talairach space).\n\n* The 'r' parameter must be positive!\n* The 'f' parameter must be between 1 and 100 (inclusive).\n* '-wball' does nothing if you input your own weight\n  with the '-weight' option.\n* '-wball' does change the binary weight created by\n  the '-noweight' option.\n* You can only use '-wball' once in a run of 3dQwarp.\n\n**The effect of '-wball' is not dramatic.** The example\nabove makes the average brain image across a collection\nof subjects a little sharper in the thalamic area, which\nmight have some small value.  If you care enough about\nalignment to use '-wball', then you should examine the\nresults from 3dQwarp for each subject, to see if the\nalignments are good enough for your purposes.",
            "argstr": "-wball {wball}",
            "xor": ["wmask"],
        },
    ),
    (
        "wmask",
        ty.Any,
        {
            "help_string": "Similar to '-wball', but here, you provide a dataset 'ws'\nthat indicates where to increase the weight.\n\n* The 'ws' dataset must be on the same 3D grid as the base dataset.\n* 'ws' is treated as a mask -- it only matters where it\n  is nonzero -- otherwise, the values inside are not used.\n* After 'ws' comes the factor 'f' by which to increase the\n  automatically computed weight.  Where 'ws' is nonzero,\n  the weighting will be multiplied by (1+f).\n* As with '-wball', the factor 'f' should be between 1 and 100.\n\n",
            "argstr": "-wpass {wmask[0]} {wmask[1]}",
            "xor": ["wball"],
        },
    ),
    (
        "out_weight_file",
        File,
        {
            "help_string": "Write the weight volume to disk as a dataset",
            "argstr": "-wtprefix {out_weight_file}",
        },
    ),
    (
        "blur",
        list,
        {
            "help_string": "Gaussian blur the input images by 'bb' (FWHM) voxels before\ndoing the alignment (the output dataset will not be blurred).\nThe default is 2.345 (for no good reason).\n\n* Optionally, you can provide 2 values for 'bb', and then\n  the first one is applied to the base volume, the second\n  to the source volume.\n  e.g., '-blur 0 3' to skip blurring the base image\n  (if the base is a blurry template, for example).\n* A negative blur radius means to use 3D median filtering,\n  rather than Gaussian blurring.  This type of filtering will\n  better preserve edges, which can be important in alignment.\n* If the base is a template volume that is already blurry,\n  you probably don't want to blur it again, but blurring\n  the source volume a little is probably a good idea, to\n  help the program avoid trying to match tiny features.\n* Note that -duplo will blur the volumes some extra\n  amount for the initial small-scale warping, to make\n  that phase of the program converge more rapidly.\n\n",
            "argstr": "-blur {blur}",
        },
    ),
    (
        "pblur",
        list,
        {
            "help_string": "Use progressive blurring; that is, for larger patch sizes,\nthe amount of blurring is larger.  The general idea is to\navoid trying to match finer details when the patch size\nand incremental warps are coarse.  When '-blur' is used\nas well, it sets a minimum amount of blurring that will\nbe used. [06 Aug 2014 -- '-pblur' may become the default someday].\n\n* You can optionally give the fraction of the patch size that\n  is used for the progressive blur by providing a value between\n  0 and 0.25 after '-pblur'.  If you provide TWO values, the\n  the first fraction is used for progressively blurring the\n  base image and the second for the source image.  The default\n  parameters when just '-pblur' is given is the same as giving\n  the options as '-pblur 0.09 0.09'.\n* '-pblur' is useful when trying to match 2 volumes with high\n  amounts of detail; e.g, warping one subject's brain image to\n  match another's, or trying to warp to match a detailed template.\n* Note that using negative values with '-blur' means that the\n  progressive blurring will be done with median filters, rather\n  than Gaussian linear blurring.\n\nNote: The combination of the -allineate and -pblur options will make\nthe results of using 3dQwarp to align to a template somewhat\nless sensitive to initial head position and scaling.",
            "argstr": "-pblur {pblur}",
        },
    ),
    (
        "emask",
        File,
        {
            "help_string": "Here, 'ee' is a dataset to specify a mask of voxelsto EXCLUDE from the analysis -- all voxels in 'ee'that are NONZERO will not be used in the alignment.The base image always automasked -- the emask isextra, to indicate voxels you definitely DON'T wantincluded in the matching process, even if they areinside the brain.",
            "argstr": "-emask {emask}",
            "copyfile": False,
        },
    ),
    (
        "noXdis",
        bool,
        {"help_string": "Warp will not displace in x direction", "argstr": "-noXdis"},
    ),
    (
        "noYdis",
        bool,
        {"help_string": "Warp will not displace in y direction", "argstr": "-noYdis"},
    ),
    (
        "noZdis",
        bool,
        {"help_string": "Warp will not displace in z direction", "argstr": "-noZdis"},
    ),
    (
        "iniwarp",
        ty.List[Head],
        {
            "help_string": 'A dataset with an initial nonlinear warp to use.\n\n* If this option is not used, the initial warp is the identity.\n* You can specify a catenation of warps (in quotes) here, as in\n  program 3dNwarpApply.\n* As a special case, if you just input an affine matrix in a .1D\n  file, that will work also -- it is treated as giving the initial\n  warp via the string "IDENT(base_dataset) matrix_file.aff12.1D".\n* You CANNOT use this option with -duplo !!\n* -iniwarp is usually used with -inilev to re-start 3dQwarp from\n  a previous stopping point.\n\n',
            "argstr": "-iniwarp {iniwarp}",
            "xor": ["duplo"],
        },
    ),
    (
        "inilev",
        int,
        {
            "help_string": "The initial refinement 'level' at which to start.\n\n* Usually used with -iniwarp; CANNOT be used with -duplo.\n* The combination of -inilev and -iniwarp lets you take the\n  results of a previous 3dQwarp run and refine them further:\n  Note that the source dataset in the second run is the SAME as\n  in the first run.  If you don't see why this is necessary,\n  then you probably need to seek help from an AFNI guru.\n\n",
            "argstr": "-inilev {inilev}",
            "xor": ["duplo"],
        },
    ),
    (
        "minpatch",
        int,
        {
            "help_string": "The value of mm should be an odd integer.\n\n* The default value of mm is 25.\n* For more accurate results than mm=25, try 19 or 13.\n* The smallest allowed patch size is 5.\n* You may want stop at a larger patch size (say 7 or 9) and use\n  the -Qfinal option to run that final level with quintic warps,\n  which might run faster and provide the same degree of warp detail.\n* Trying to make two different brain volumes match in fine detail\n  is usually a waste of time, especially in humans.  There is too\n  much variability in anatomy to match gyrus to gyrus accurately.\n  For this reason, the default minimum patch size is 25 voxels.\n  Using a smaller '-minpatch' might try to force the warp to\n  match features that do not match, and the result can be useless\n  image distortions -- another reason to LOOK AT THE RESULTS.\n\n",
            "argstr": "-minpatch {minpatch}",
        },
    ),
    (
        "maxlev",
        int,
        {
            "help_string": "The initial refinement 'level' at which to start.\n\n* Usually used with -iniwarp; CANNOT be used with -duplo.\n* The combination of -inilev and -iniwarp lets you take the\n  results of a previous 3dQwarp run and refine them further:\n  Note that the source dataset in the second run is the SAME as\n  in the first run.  If you don't see why this is necessary,\n  then you probably need to seek help from an AFNI guru.\n\n",
            "argstr": "-maxlev {maxlev}",
            "position": -1,
            "xor": ["duplo"],
        },
    ),
    (
        "gridlist",
        File,
        {
            "help_string": "This option provides an alternate way to specify the patch\ngrid sizes used in the warp optimization process. 'gl' is\na 1D file with a list of patches to use -- in most cases,\nyou will want to use it in the following form:\n``-gridlist '1D: 0 151 101 75 51'``\n\n* Here, a 0 patch size means the global domain. Patch sizes\n  otherwise should be odd integers >= 5.\n* If you use the '0' patch size again after the first position,\n  you will actually get an iteration at the size of the\n  default patch level 1, where the patch sizes are 75% of\n  the volume dimension.  There is no way to force the program\n  to literally repeat the sui generis step of lev=0.\n\n",
            "argstr": "-gridlist {gridlist}",
            "copyfile": False,
            "xor": ["duplo", "plusminus"],
        },
    ),
    (
        "allsave",
        bool,
        {
            "help_string": '\nThis option lets you save the output warps from each level"\nof the refinement process.  Mostly used for experimenting."\nWill only save all the outputs if the program terminates"\nnormally -- if it crashes, or freezes, then all these"\nwarps are lost.',
            "argstr": "-allsave",
            "xor": ["nopadWARP", "duplo", "plusminus"],
        },
    ),
    (
        "duplo",
        bool,
        {
            "help_string": 'Start off with 1/2 scale versions of the volumes,"\nfor getting a speedy coarse first alignment."\n\n* Then scales back up to register the full volumes."\n  The goal is greater speed, and it seems to help this"\n  positively piggish program to be more expeditious."\n* However, accuracy is somewhat lower with \'-duplo\',"\n  for reasons that currently elude Zhark; for this reason,"\n  the Emperor does not usually use \'-duplo\'.\n\n',
            "argstr": "-duplo",
            "xor": ["gridlist", "maxlev", "inilev", "iniwarp", "plusminus", "allsave"],
        },
    ),
    (
        "workhard",
        bool,
        {
            "help_string": "Iterate more times, which can help when the volumes are\nhard to align at all, or when you hope to get a more precise\nalignment.\n\n* Slows the program down (possibly a lot), of course.\n* When you combine '-workhard'  with '-duplo', only the\n  full size volumes get the extra iterations.\n* For finer control over which refinement levels work hard,\n  you can use this option in the form (for example) ``-workhard:4:7``\n  which implies the extra iterations will be done at levels\n  4, 5, 6, and 7, but not otherwise.\n* You can also use '-superhard' to iterate even more, but\n  this extra option will REALLY slow things down.\n\n  * Under most circumstances, you should not need to use either\n    ``-workhard`` or ``-superhard``.\n  * The fastest way to register to a template image is via the\n    ``-duplo`` option, and without the ``-workhard`` or ``-superhard`` options.\n  * If you use this option in the form '-Workhard' (first letter\n    in upper case), then the second iteration at each level is\n    done with quintic polynomial warps.\n\n",
            "argstr": "-workhard",
            "xor": ["boxopt", "ballopt"],
        },
    ),
    (
        "Qfinal",
        bool,
        {
            "help_string": "At the finest patch size (the final level), use Hermite\nquintic polynomials for the warp instead of cubic polynomials.\n\n* In a 3D 'patch', there are 2x2x2x3=24 cubic polynomial basis\n  function parameters over which to optimize (2 polynomials\n  dependent on each of the x,y,z directions, and 3 different\n  directions of displacement).\n* There are 3x3x3x3=81 quintic polynomial parameters per patch.\n* With -Qfinal, the final level will have more detail in\n  the allowed warps, at the cost of yet more CPU time.\n* However, no patch below 7x7x7 in size will be done with quintic\n  polynomials.\n* This option is also not usually needed, and is experimental.\n\n",
            "argstr": "-Qfinal",
        },
    ),
    (
        "Qonly",
        bool,
        {
            "help_string": "Use Hermite quintic polynomials at all levels.\n\n* Very slow (about 4 times longer).  Also experimental.\n* Will produce a (discrete representation of a) C2 warp.\n\n",
            "argstr": "-Qonly",
        },
    ),
    (
        "plusminus",
        bool,
        {
            "help_string": "Normally, the warp displacements dis(x) are defined to match\nbase(x) to source(x+dis(x)).  With this option, the match\nis between base(x-dis(x)) and source(x+dis(x)) -- the two\nimages 'meet in the middle'.\n\n* One goal is to mimic the warping done to MRI EPI data by\n  field inhomogeneities, when registering between a 'blip up'\n  and a 'blip down' down volume, which will have opposite\n  distortions.\n* Define Wp(x) = x+dis(x) and Wm(x) = x-dis(x).  Then since\n  base(Wm(x)) matches source(Wp(x)), by substituting INV(Wm(x))\n  wherever we see x, we have base(x) matches source(Wp(INV(Wm(x))));\n  that is, the warp V(x) that one would get from the 'usual' way\n  of running 3dQwarp is V(x) = Wp(INV(Wm(x))).\n* Conversely, we can calculate Wp(x) in terms of V(x) as follows:\n  If V(x) = x + dv(x), define Vh(x) = x + dv(x)/2;\n  then Wp(x) = V(INV(Vh(x)))\n* With the above formulas, it is possible to compute Wp(x) from\n  V(x) and vice-versa, using program 3dNwarpCalc.  The requisite\n  commands are left as an exercise for the aspiring AFNI Jedi Master.\n* You can use the semi-secret '-pmBASE' option to get the V(x)\n  warp and the source dataset warped to base space, in addition to\n  the Wp(x) '_PLUS' and Wm(x) '_MINUS' warps.\n\n  * Alas: -plusminus does not work with -duplo or -allineate :-(\n  * However, you can use -iniwarp with -plusminus :-)\n  * The outputs have _PLUS (from the source dataset) and _MINUS\n    (from the base dataset) in their filenames, in addition to\n    the prefix.  The -iwarp option, if present, will be ignored.\n\n",
            "argstr": "-plusminus",
            "xor": ["duplo", "allsave", "iwarp"],
        },
    ),
    (
        "nopad",
        bool,
        {
            "help_string": "Do NOT use zero-padding on the 3D base and source images.\n[Default == zero-pad, if needed]\n\n* The underlying model for deformations goes to zero at the\n  edge of the volume being warped.  However, if there is\n  significant data near an edge of the volume, then it won't\n  get displaced much, and so the results might not be good.\n* Zero padding is designed as a way to work around this potential\n  problem.  You should NOT need the '-nopad' option for any\n  reason that Zhark can think of, but it is here to be symmetrical\n  with 3dAllineate.\n* Note that the output (warped from source) dataset will be on the\n  base dataset grid whether or not zero-padding is allowed.  However,\n  unless you use the following option, allowing zero-padding (i.e.,\n  the default operation) will make the output WARP dataset(s) be\n  on a larger grid (also see '-expad' below).\n\n",
            "argstr": "-nopad",
        },
    ),
    (
        "nopadWARP",
        bool,
        {
            "help_string": "If for some reason you require the warp volume tomatch the base volume, then use this option to have the outputWARP dataset(s) truncated.",
            "argstr": "-nopadWARP",
            "xor": ["allsave", "expad"],
        },
    ),
    (
        "expad",
        int,
        {
            "help_string": "This option instructs the program to pad the warp by an extra'EE' voxels (and then 3dQwarp starts optimizing it).This option is seldom needed, but can be useful if youmight later catenate the nonlinear warp -- via 3dNwarpCat --with an affine transformation that contains a large shift.Under that circumstance, the nonlinear warp might be shiftedpartially outside its original grid, so expanding that gridcan avoid this problem.Note that this option perforce turns off '-nopadWARP'.",
            "argstr": "-expad {expad}",
            "xor": ["nopadWARP"],
        },
    ),
    (
        "ballopt",
        bool,
        {
            "help_string": "Normally, the incremental warp parameters are optimized insidea rectangular 'box' (24 dimensional for cubic patches, 81 forquintic patches), whose limits define the amount of distortionallowed at each step.  Using '-ballopt' switches these limitsto be applied to a 'ball' (interior of a hypersphere), whichcan allow for larger incremental displacements.  Use thisoption if you think things need to be able to move farther.",
            "argstr": "-ballopt",
            "xor": ["workhard", "boxopt"],
        },
    ),
    (
        "baxopt",
        bool,
        {
            "help_string": "Use the 'box' optimization limits instead of the 'ball'[this is the default at present].Note that if '-workhard' is used, then ball and box optimizationare alternated in the different iterations at each level, sothese two options have no effect in that case.",
            "argstr": "-boxopt",
            "xor": ["workhard", "ballopt"],
        },
    ),
    (
        "verb",
        bool,
        {
            "help_string": "more detailed description of the process",
            "argstr": "-verb",
            "xor": ["quiet"],
        },
    ),
    (
        "quiet",
        bool,
        {
            "help_string": "Cut out most of the fun fun fun progress messages :-(",
            "argstr": "-quiet",
            "xor": ["verb"],
        },
    ),
    ("overwrite", bool, {"help_string": "Overwrite outputs", "argstr": "-overwrite"}),
    (
        "lpc",
        bool,
        {
            "help_string": "Local Pearson minimization (i.e., EPI-T1 registration)This option has not be extensively testedIf you use '-lpc', then '-maxlev 0' is automatically set.If you want to go to more refined levels, you can set '-maxlev'This should be set up to have lpc as the second to last argumentand maxlev as the second to last argument, as needed by AFNIUsing maxlev > 1 is not recommended for EPI-T1 alignment.",
            "argstr": "-lpc",
            "position": -2,
            "xor": ["nmi", "mi", "hel", "lpa", "pear"],
        },
    ),
    (
        "lpa",
        bool,
        {
            "help_string": "Local Pearson maximization. This option has not be extensively tested",
            "argstr": "-lpa",
            "xor": ["nmi", "mi", "lpc", "hel", "pear"],
        },
    ),
    (
        "hel",
        bool,
        {
            "help_string": "Hellinger distance: a matching function for the adventurousThis option has NOT be extensively tested for usefulnessand should be considered experimental at this infundibulum.",
            "argstr": "-hel",
            "xor": ["nmi", "mi", "lpc", "lpa", "pear"],
        },
    ),
    (
        "mi",
        bool,
        {
            "help_string": "Mutual Information: a matching function for the adventurousThis option has NOT be extensively tested for usefulnessand should be considered experimental at this infundibulum.",
            "argstr": "-mi",
            "xor": ["mi", "hel", "lpc", "lpa", "pear"],
        },
    ),
    (
        "nmi",
        bool,
        {
            "help_string": "Normalized Mutual Information: a matching function for the adventurousThis option has NOT been extensively tested for usefulnessand should be considered experimental at this infundibulum.",
            "argstr": "-nmi",
            "xor": ["nmi", "hel", "lpc", "lpa", "pear"],
        },
    ),
    ("num_threads", int, 1, {"help_string": "set number of threads"}),
    ("outputtype", ty.Any, {"help_string": "AFNI output filetype"}),
]
Qwarp_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "warped_source",
        File,
        {
            "help_string": "Warped source file. If plusminus is used, this is the undistortedsource file."
        },
    ),
    ("warped_base", File, {"help_string": "Undistorted base file."}),
    (
        "source_warp",
        File,
        {
            "help_string": "Displacement in mm for the source image.If plusminus is used this is the field suceptibility correctionwarp (in 'mm') for source image."
        },
    ),
    (
        "base_warp",
        File,
        {
            "help_string": "Displacement in mm for the base image.If plus minus is used, this is the field suceptibility correctionwarp (in 'mm') for base image. This is only output if plusminusor iwarp options are passed"
        },
    ),
    ("weights", File, {"help_string": "Auto-computed weight volume."}),
]
Qwarp_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Qwarp(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from fileformats.medimage_afni import Head
    >>> from pydra.tasks.afni.auto.preprocess.qwarp import Qwarp

    >>> task = Qwarp()
    >>> task.inputs.in_file = None
    >>> task.inputs.base_file = None
    >>> task.inputs.out_file = NiftiGz.mock()
    >>> task.inputs.weight = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.emask = File.mock()
    >>> task.inputs.gridlist = File.mock()
    >>> task.inputs.plusminus = True
    >>> task.inputs.nopadWARP = True
    >>> task.cmdline
    '3dQwarp -base sub-01_dir-RL_epi.nii.gz -source sub-01_dir-LR_epi.nii.gz -nopadWARP -prefix ppp_sub-01_dir-LR_epi -plusminus'


    >>> task = Qwarp()
    >>> task.inputs.in_file = None
    >>> task.inputs.base_file = None
    >>> task.inputs.out_file = NiftiGz.mock()
    >>> task.inputs.resample = True
    >>> task.inputs.weight = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.emask = File.mock()
    >>> task.inputs.gridlist = File.mock()
    >>> task.cmdline
    '3dQwarp -base mni.nii -source structural.nii -prefix ppp_structural -resample'


    >>> task = Qwarp()
    >>> task.inputs.in_file = None
    >>> task.inputs.base_file = None
    >>> task.inputs.out_file = NiftiGz.mock(None)
    >>> task.inputs.resample = True
    >>> task.inputs.iwarp = True
    >>> task.inputs.weight = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.blur = [0,3]
    >>> task.inputs.emask = File.mock()
    >>> task.inputs.gridlist = File.mock()
    >>> task.inputs.verb = True
    >>> task.inputs.lpc = True
    >>> task.cmdline
    '3dQwarp -base epi.nii -blur 0.0 3.0 -source structural.nii -iwarp -prefix anatSSQ.nii.gz -resample -verb -lpc'


    >>> task = Qwarp()
    >>> task.inputs.in_file = None
    >>> task.inputs.base_file = None
    >>> task.inputs.out_file = NiftiGz.mock()
    >>> task.inputs.weight = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.blur = [0,3]
    >>> task.inputs.emask = File.mock()
    >>> task.inputs.gridlist = File.mock()
    >>> task.inputs.duplo = True
    >>> task.cmdline
    '3dQwarp -base mni.nii -blur 0.0 3.0 -duplo -source structural.nii -prefix ppp_structural'


    >>> task = Qwarp()
    >>> task.inputs.in_file = None
    >>> task.inputs.base_file = None
    >>> task.inputs.out_file = NiftiGz.mock(None)
    >>> task.inputs.weight = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.blur = [0,3]
    >>> task.inputs.emask = File.mock()
    >>> task.inputs.minpatch = 25
    >>> task.inputs.gridlist = File.mock()
    >>> task.inputs.duplo = True
    >>> task.cmdline
    '3dQwarp -base mni.nii -blur 0.0 3.0 -duplo -source structural.nii -minpatch 25 -prefix Q25'


    >>> task = Qwarp()
    >>> task.inputs.in_file = None
    >>> task.inputs.base_file = None
    >>> task.inputs.out_file = NiftiGz.mock(None)
    >>> task.inputs.weight = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.blur = [0,2]
    >>> task.inputs.emask = File.mock()
    >>> task.inputs.iniwarp = None
    >>> task.inputs.inilev = 7
    >>> task.inputs.gridlist = File.mock()
    >>> task.cmdline
    '3dQwarp -base mni.nii -blur 0.0 2.0 -source structural.nii -inilev 7 -iniwarp Q25_warp+tlrc.HEAD -prefix Q11'


    >>> task = Qwarp()
    >>> task.inputs.in_file = None
    >>> task.inputs.base_file = None
    >>> task.inputs.out_file = NiftiGz.mock()
    >>> task.inputs.allineate = True
    >>> task.inputs.allineate_opts = "-cose lpa -verb"
    >>> task.inputs.weight = File.mock()
    >>> task.inputs.out_weight_file = File.mock()
    >>> task.inputs.emask = File.mock()
    >>> task.inputs.gridlist = File.mock()
    >>> task.cmdline
    '3dQwarp -allineate -allineate_opts "-cose lpa -verb" -base mni.nii -source structural.nii -prefix ppp_structural'


    """

    input_spec = Qwarp_input_spec
    output_spec = Qwarp_output_spec
    executable = "3dQwarp"
