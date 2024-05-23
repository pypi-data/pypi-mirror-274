from typing import Any, Dict, List, Tuple, Union
import numpy as np


class WinMLModel:
    """
    Class representing a WinML model.

    Args:
        model_path (str): Path to the ONNX model file.
    """

    def __init__(self, model_path: str) -> None: ...

    def get_author(self) -> str: ...

    def get_name(self) -> str: ...

    def get_domain(self) -> str: ...

    def get_description(self) -> str: ...

    def get_input_names(self) -> List[str]: ...

    def get_output_names(self) -> List[str]: ...

    def get_input_details(self) -> List[Tuple[str, List[int], str]]: ...

    def get_output_details(self) -> List[Tuple[str, List[int], str]]: ...


class WinMLSession:
    """
    Class representing a WinML session for model inference.

    Args:
        model (WinMLModel): The WinML model to be used for inference.
        device_type (str): The device type to be used ('CPU' or 'GPU').

    Methods:
        set_input(name: str, value: WinMLValue) -> None:
            Set an input value for the session.

        evaluate() -> Dict[str, WinMLValue]:
            Run inference and return the output values.

        get_input_details() -> List[Tuple[str, List[int], str]]:
            Get details of model inputs.

        get_output_details() -> List[Tuple[str, List[int], str]]:
            Get details of model outputs.
    """

    def __init__(self, model: WinMLModel, device_type: str = 'CPU') -> None: ...

    def set_input(self, name: str, value: 'WinMLValue') -> None: ...

    def clear_input(self) -> None: ...

    def evaluate(self) -> Dict[str, 'WinMLValue']: ...

    def get_input_details(self) -> List[Tuple[str, List[int], str]]: ...

    def get_output_details(self) -> List[Tuple[str, List[int], str]]: ...


class WinMLValue:
    """
    Class representing a value to be used as input or output in WinML.

    Args:
        array (np.ndarray): The NumPy array representing the value.

    Methods:
        to_numpy() -> np.ndarray:
            Convert the value to a NumPy array.
    """

    def __init__(self, array: np.ndarray) -> None: ...

    def to_numpy(self) -> np.ndarray: ...


class DeviceType:
    """
    Enum representing the device type to be used for inference.
    """
    CPU: str
    GPU: str
