import os
from flexidata.models.detectron2 import DetectronModel
import logging

DEFAULT_MODEL = "detectron2"

models = {}

def get_model(model_name=None):
    if model_name is None:
        default_model = os.environ.get("DEFAULT_MODEL_NAME")
        model_name = default_model if default_model is not None else DEFAULT_MODEL

    if model_name in models:
        return models[model_name]
    if model_name == "detectron2":
        model = DetectronModel()
        model.initialize()
        models[model_name] = model
        return model
