from fileformats.generic import File
import logging
import os
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate(
    {"return": {"design_mat": File, "design_con": File, "design_grp": File}}
)
def L2Model(num_copes: ty.Any) -> ty.Tuple[File, File, File]:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.auto.model.l2_model import L2Model

    """
    cwd = os.getcwd()
    mat_txt = [
        "/NumWaves   1",
        "/NumPoints  {:d}".format(num_copes),
        "/PPheights  1",
        "",
        "/Matrix",
    ]
    for i in range(num_copes):
        mat_txt += ["1"]
    mat_txt = "\n".join(mat_txt)

    con_txt = [
        "/ContrastName1  group mean",
        "/NumWaves   1",
        "/NumContrasts   1",
        "/PPheights  1",
        "/RequiredEffect     100",  # XX where does this
        # number come from
        "",
        "/Matrix",
        "1",
    ]
    con_txt = "\n".join(con_txt)

    grp_txt = [
        "/NumWaves   1",
        "/NumPoints  {:d}".format(num_copes),
        "",
        "/Matrix",
    ]
    for i in range(num_copes):
        grp_txt += ["1"]
    grp_txt = "\n".join(grp_txt)

    txt = {"design.mat": mat_txt, "design.con": con_txt, "design.grp": grp_txt}

    # write design files
    for i, name in enumerate(["design.mat", "design.con", "design.grp"]):
        f = open(os.path.join(cwd, name), "wt")
        f.write(txt[name])
        f.close()

    outputs = _outputs().get()
    for field in list(outputs.keys()):
        outputs[field] = os.path.join(os.getcwd(), field.replace("_", "."))

    return design_mat, design_con, design_grp


# Nipype methods converted into functions


def _outputs():
    """Returns a bunch containing output fields for the class"""
    outputs = None
    if self.output_spec:
        outputs = {}

    return outputs
