from conans import ConanFile, CMake, tools
import os


class GameNetworkingSocketsConan(ConanFile):
    name = "GameNetworkingSockets"
    version = "0.0.0"
    license = "BSD 3-Clause"
    url = "https://github.com/elizagamedev/conan-GameNetworkingSockets"
    description = "Reliable & unreliable messages over UDP. Message fragmentation & reassembly, bandwidth estimation, encryption."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = (
        "OpenSSL/1.0.2o@conan/stable",
        "protobuf/3.5.2@bincrafters/stable",
    )
    build_requires = "cmake_installer/3.11.1@conan/stable"
    exports = "*.patch"

    def configure(self):
        self.options["protobuf"].shared = True

    def source(self):
        self.run("git clone https://github.com/ValveSoftware/GameNetworkingSockets.git")
        tools.patch("GameNetworkingSockets", patch_file="conan.patch")

    def build(self):
        with tools.environment_append({"LD_LIBRARY_PATH": self.deps_cpp_info["protobuf"].lib_paths}):
            cmake = CMake(self)
            cmake.configure(source_folder="GameNetworkingSockets")
            cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join("GameNetworkingSockets", "include"))
        self.copy("*.pdb", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
        # Copy correct lib
        if self.options.shared:
            libname = "GameNetworkingSockets"
        else:
            libname = "GameNetworkingSockets_s"
        if self.settings.compiler == "Visual Studio":
            self.copy("*{}{}.lib".format(os.sep, libname), dst="lib", keep_path=False)
        else:
            self.copy("*{}lib{}.so".format(os.sep, libname), dst="lib", keep_path=False, symlinks=True)
            self.copy("*{}lib{}.a".format(os.sep, libname), dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if not self.options.shared:
            self.cpp_info.defines = ["STEAMDATAGRAMLIB_STATIC_LINK"]
