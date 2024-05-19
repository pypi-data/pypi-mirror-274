# Copyright (C) 2021-2024, Mindee.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

from fast_text_detect import detection
from typing import Any, List

from fast_text_detect.utils.file_utils import is_tf_available, is_torch_available
from fast_text_detect.detection.fast import reparameterize
from fast_text_detect.preprocessor import PreProcessor
from fast_text_detect.predictor import DetectionPredictor


__all__ = ["detection_predictor"]

ARCHS: List[str]

ARCHS = [
    "fast_tiny",
    "fast_small",
    "fast_base",
]


def _predictor(arch: Any, pretrained: bool, assume_straight_pages: bool = True, **kwargs: Any) -> DetectionPredictor:
    if isinstance(arch, str):
        if arch not in ARCHS:
            raise ValueError(f"unknown architecture '{arch}'")

        _model = detection.__dict__[arch](
            pretrained=pretrained,
            pretrained_backbone=kwargs.get("pretrained_backbone", True),
            assume_straight_pages=assume_straight_pages,
        )
        # Reparameterize FAST models by default to lower inference latency and memory usage
        _model = reparameterize(_model)
    else:
        _model = arch
        _model.assume_straight_pages = assume_straight_pages
        
        raise ValueError(f"unknown architecture: {type(arch)}")

        
    kwargs.pop("pretrained_backbone", None)

    kwargs["mean"] = kwargs.get("mean", _model.cfg["mean"])
    kwargs["std"] = kwargs.get("std", _model.cfg["std"])
    kwargs["batch_size"] = kwargs.get("batch_size", 2)
    predictor = DetectionPredictor(
        PreProcessor(_model.cfg["input_shape"][:-1] if is_tf_available() else _model.cfg["input_shape"][1:], **kwargs),
        _model,
    )
    return predictor


def detection_predictor(
    arch: Any = "fast_base",
    pretrained: bool = False,
    assume_straight_pages: bool = True,
    **kwargs: Any,
) -> DetectionPredictor:
    """Text detection architecture.

    >>> import numpy as np
    >>> from doctr.models import detection_predictor
    >>> model = detection_predictor(arch='db_resnet50', pretrained=True)
    >>> input_page = (255 * np.random.rand(600, 800, 3)).astype(np.uint8)
    >>> out = model([input_page])

    Args:
    ----
        arch: name of the architecture or model itself to use (e.g. 'db_resnet50')
        pretrained: If True, returns a model pre-trained on our text detection dataset
        assume_straight_pages: If True, fit straight boxes to the page
        **kwargs: optional keyword arguments passed to the architecture

    Returns:
    -------
        Detection predictor
    """
    return _predictor(arch, pretrained, assume_straight_pages, **kwargs)
