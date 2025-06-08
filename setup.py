# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os

from setuptools import Distribution, Extension, setup

allowed_to_fail = os.environ.get("CIBUILDWHEEL", "0") != "1"


def get_ext_modules():
    """Build Cython extensions if available."""
    try:
        import Cython.Compiler.Options
        from Cython.Build import cythonize

        Cython.Compiler.Options.annotate = True

        if os.name == "nt":  # Windows
            extra_compile_args = [
                "/O2",
            ]
        else:  # UNIX-based systems
            extra_compile_args = [
                "-O3",
            ]

        package_path = "pyiceberg"

        extension = Extension(
            # Your .pyx file will be available to cpython at this location.
            name="pyiceberg.avro.decoder_fast",
            sources=[
                os.path.join(package_path, "avro", "decoder_fast.pyx"),
            ],
            extra_compile_args=extra_compile_args,
            language="c",
        )

        return cythonize([extension], include_path=[package_path], language_level=3, annotate=True)
    except Exception:
        if not allowed_to_fail:
            raise
        return []


class BinaryDistribution(Distribution):
    def has_ext_modules(self) -> bool:
        return True


setup(
    distclass=BinaryDistribution,
    ext_modules=get_ext_modules(),
    include_package_data=True,
    exclude_package_data={"pyiceberg": ["*.pyc"]},
)
