from dataclasses import dataclass

from onnxruntime import InferenceSession


@dataclass(frozen=True)
class SonusAIMetaData:
    input_shape: list[int]
    output_shape: list[int]
    flattened: bool
    timestep: bool
    channel: bool
    mutex: bool
    feature: str


def add_sonusai_metadata(model,
                         is_flattened: bool = True,
                         has_timestep: bool = True,
                         has_channel: bool = False,
                         is_mutex: bool = True,
                         feature: str = ''):
    """Add SonusAI metadata to an ONNX model.

    :param model: ONNX model
    :param is_flattened: Model feature data is flattened
    :param has_timestep: Model has timestep dimension
    :param has_channel: Model has channel dimension
    :param is_mutex: Model label output is mutually exclusive
    :param feature: Model feature type
    """
    is_flattened_flag = model.metadata_props.add()
    is_flattened_flag.key = 'is_flattened'
    is_flattened_flag.value = str(is_flattened)

    has_timestep_flag = model.metadata_props.add()
    has_timestep_flag.key = 'has_timestep'
    has_timestep_flag.value = str(has_timestep)

    has_channel_flag = model.metadata_props.add()
    has_channel_flag.key = 'has_channel'
    has_channel_flag.value = str(has_channel)

    is_mutex_flag = model.metadata_props.add()
    is_mutex_flag.key = 'is_mutex'
    is_mutex_flag.value = str(is_mutex)

    feature_flag = model.metadata_props.add()
    feature_flag.key = 'feature'
    feature_flag.value = str(feature)

    return model


def get_sonusai_metadata(model: InferenceSession) -> SonusAIMetaData:
    """Get SonusAI metadata from an ONNX model.
    """
    m = model.get_modelmeta().custom_metadata_map
    return SonusAIMetaData(input_shape=model.get_inputs()[0].shape,
                           output_shape=model.get_outputs()[0].shape,
                           flattened=m['is_flattened'] == 'True',
                           timestep=m['has_timestep'] == 'True',
                           channel=m['has_channel'] == 'True',
                           mutex=m['is_mutex'] == 'True',
                           feature=m['feature'])
