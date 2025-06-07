import os

from setuptools import Distribution, Extension, setup

print(os.path.dirname(__file__))
allowed_to_fail = os.environ.get("CIBUILDWHEEL", "0") != "1"

ext_modules = []

try:
    import Cython.Compiler.Options
    from Cython.Build import cythonize

    Cython.Compiler.Options.annotate = True

    if os.name == "nt":  # Windows
        extra_compile_args = ["/O2"]
    else:  # UNIX-based systems
        extra_compile_args = ["-O3"]

    # Use relative path only
    package_path = "pyiceberg"

    extension = Extension(
        name="pyiceberg.avro.decoder_fast",
        sources=[
            os.path.join(package_path, "avro", "decoder_fast.pyx"),
        ],
        extra_compile_args=extra_compile_args,
        language="c",
    )

    ext_modules = cythonize(
        [extension],
        include_path=["pyiceberg"],
        language_level=3,
        annotate=True,
        build_dir="build",  # Specify build directory to avoid absolute paths
    )

except ImportError:
    if not allowed_to_fail:
        raise
    # Cython not available, skip extension building


class BinaryDistribution(Distribution):
    def has_ext_modules(self) -> bool:
        return True


setup(
    distclass=BinaryDistribution,
    ext_modules=ext_modules,
    include_package_data=True,
    exclude_package_data={"pyiceberg": ["*.pyc"]},
)
