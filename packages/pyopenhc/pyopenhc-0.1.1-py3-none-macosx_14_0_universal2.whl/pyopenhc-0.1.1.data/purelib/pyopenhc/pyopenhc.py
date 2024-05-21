# Copyright (c) 2024, Zhendong Peng (pzd17@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ctypes
import os
import platform


if platform.system() == "Darwin":
    LIBOPENCC = os.path.join(os.path.dirname(__file__), "libopencc.dylib")
elif platform.system() == "Windows":
    LIBOPENCC = os.path.join(os.path.dirname(__file__), "opencc.dll")
elif platform.system() == "Linux":
    LIBOPENCC = os.path.join(os.path.dirname(__file__), "libopencc.so")
else:
    raise OSError("Unsupported operating system")
if not os.path.exists(LIBOPENCC):
    raise OSError(f"OpenCC library not found: {LIBOPENCC}")
lib = ctypes.CDLL(LIBOPENCC)

lib.opencc_open.restype = ctypes.c_void_p
lib.opencc_convert_utf8.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
lib.opencc_convert_utf8.restype = ctypes.c_void_p
lib.opencc_close.argtypes = [ctypes.c_void_p]
lib.opencc_convert_utf8_free.argtypes = [ctypes.c_void_p]


class OpenHC:
    def __init__(self, config="t2s"):
        if not config.endswith(".json"):
            config += ".json"
        if not os.path.isfile(config):
            config = os.path.join(os.path.dirname(__file__), "data", config)
        self._od = lib.opencc_open(ctypes.c_char_p(config.encode("utf-8")))

    def convert(self, text):
        text = text.encode("utf-8")
        retv_i = lib.opencc_convert_utf8(self._od, text, len(text))
        if retv_i == -1:
            raise Exception("OpenHC Convert Error")
        retv_c = ctypes.cast(retv_i, ctypes.c_char_p)
        value = retv_c.value
        lib.opencc_convert_utf8_free(retv_c)
        return value.decode("utf-8")
