import os
import platform

# import torch to load in directml
import torch

# Load the directml dll into the process
platform = 'win' if platform.system() == 'Windows' else 'linux'
if platform == 'win':
    directml_dll = os.path.join(os.path.dirname(__file__), 'DirectML.dll')
else:
    directml_dll = os.path.join(os.path.dirname(__file__), 'libdirectml.so')
torch.ops.load_library(directml_dll)

# import native apis
import torch_directml_native

from .device import *
from .functions import *

# Register backend to support AMP
class EmptyPrivateUse1Module:
    @staticmethod
    def is_available():
        return True

    @staticmethod
    def is_autocast_enabled():
        return False

    @staticmethod
    def get_autocast_dtype():
        return torch.float16

    @staticmethod
    def set_autocast_enabled(enable):
        pass

    @staticmethod
    def set_autocast_dtype(dtype):
        pass

    @staticmethod
    def get_amp_supported_dtype():
        return [torch.float16]

torch._register_device_module('privateuseone', EmptyPrivateUse1Module)