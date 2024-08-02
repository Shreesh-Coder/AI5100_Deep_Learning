#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import copy
import traceback
from collections import defaultdict
from pathlib import Path

from classy_vision.generic.registry_utils import import_all_modules
from classy_vision.heads import build_head

FILE_ROOT = Path(__file__).parent


MODEL_REGISTRY = {}
MODEL_CLASS_NAMES = set()
MODEL_REGISTRY_TB = {}
MODEL_CLASS_NAMES_TB = {}


def register_model(name, bypass_checks=False):
    """Registers a :class:`ClassyModel` subclass.

    This decorator allows Classy Vision to instantiate a subclass of
    :class:`ClassyModel` from a configuration file, even if the class itself is
    not part of the Classy Vision framework. To use it, apply this decorator to
    a ClassyModel subclass, like this:

    .. code-block:: python

      @register_model('resnet')
      class ResidualNet(ClassyModel):
         ...

    To instantiate a model from a configuration file, see
    :func:`build_model`."""

    def register_model_cls(cls):
        if not bypass_checks:
            if name in MODEL_REGISTRY:
                msg = (
                    "Cannot register duplicate model ({}). Already registered at \n{}\n"
                )
                raise ValueError(msg.format(name, MODEL_REGISTRY_TB[name]))
            if not issubclass(cls, ClassyModel):
                raise ValueError(
                    "Model ({}: {}) must extend ClassyModel".format(name, cls.__name__)
                )
            if cls.__name__ in MODEL_CLASS_NAMES:
                msg = (
                    "Cannot register model with duplicate class name({})."
                    + "Previously registered at \n{}\n"
                )
                raise ValueError(
                    msg.format(cls.__name__, MODEL_CLASS_NAMES_TB[cls.__name__])
                )
        tb = "".join(traceback.format_stack())
        MODEL_REGISTRY[name] = cls
        MODEL_CLASS_NAMES.add(cls.__name__)
        MODEL_REGISTRY_TB[name] = tb
        MODEL_CLASS_NAMES_TB[cls.__name__] = tb
        return cls

    return register_model_cls


def build_model(config):
    """Builds a ClassyModel from a config.

    This assumes a 'name' key in the config which is used to determine what
    model class to instantiate. For instance, a config `{"name": "my_model",
    "foo": "bar"}` will find a class that was registered as "my_model"
    (see :func:`register_model`) and call .from_config on it."""

    assert config["name"] in MODEL_REGISTRY, f"unknown model: {config['name']}"
    model = MODEL_REGISTRY[config["name"]].from_config(config)
    if "heads" in config:
        heads = defaultdict(list)
        for head_config in config["heads"]:
            assert "fork_block" in head_config, "Expect fork_block in config"
            fork_block = head_config["fork_block"]
            updated_config = copy.deepcopy(head_config)
            del updated_config["fork_block"]

            head = build_head(updated_config)
            heads[fork_block].append(head)
        model.set_heads(heads)

    return model


# automatically import any Python files in the models/ directory
import_all_modules(FILE_ROOT, "classy_vision.models")

from .lecun_normal_init import lecun_normal_init  # isort:skip


__all__ = [
    "AnyNet",
    "ClassyBlock",
    "ClassyModel",
    "ClassyModelHeadExecutorWrapper",
    "ClassyModelWrapper",
    "DenseNet",
    "EfficientNet",
    "MLP",
    "RegNet",
    "ResNet",
    "ResNeXt",
    "ResNeXt3D",
    "SqueezeAndExcitationLayer",
    "VisionTransformer",
    "build_model",
    "lecun_normal_init",
    "register_model",
]