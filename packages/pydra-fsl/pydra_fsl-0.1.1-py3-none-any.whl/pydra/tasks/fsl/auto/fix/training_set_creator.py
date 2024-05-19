from fileformats.generic import Directory
import logging
import os
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"mel_icas_out": ty.List[Directory]}})
def TrainingSetCreator(mel_icas_in: ty.List[Directory]) -> ty.List[Directory]:
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from pydra.tasks.fsl.auto.fix.training_set_creator import TrainingSetCreator

    """
    mel_icas = []
    for item in mel_icas_in:
        if os.path.exists(os.path.join(item, "hand_labels_noise.txt")):
            mel_icas.append(item)

    if len(mel_icas) == 0:
        raise Exception(
            "%s did not find any hand_labels_noise.txt files in the following directories: %s"
            % (self.__class__.__name__, mel_icas)
        )

    mel_icas = []
    for item in mel_icas_in:
        if os.path.exists(os.path.join(item, "hand_labels_noise.txt")):
            mel_icas.append(item)
    outputs = _outputs().get()
    mel_icas_out = mel_icas

    return mel_icas_out


# Nipype methods converted into functions


def _outputs():
    """Returns a bunch containing output fields for the class"""
    outputs = None
    if self.output_spec:
        outputs = {}

    return outputs
