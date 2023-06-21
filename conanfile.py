from os import path
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy, replace_in_file
from conan.tools.system.package_manager import Apt, Yum, PacMan, Zypper, Chocolatey
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.scm import Git, Version

required_conan_version = ">=1.52.0"


class PackageConan(ConanFile):
    version = "cci.20220124"
    name = "gnuplot-iostream"
    description = "Iostream pipe to gnuplot with some extra functions " \
        "for pushing data arrays and getting mouse clicks"
    license = "MIT"
    homepage = "https://github.com/dstahlke/gnuplot-iostream"
    topics = ("gnuplot", "plotting", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = False # True if no patch

    @property
    def _min_cppstd(self):
        return 17

    @property
    def _compilers_minimum_version(self):
        return {
            "Visual Studio": "15.7",
            "msvc": "14.1",
            "gcc": "7",
            "clang": "6",
            "apple-clang": "10"
        }

    @property
    def _build_tests(self):
        return not self.conf.get("tools.build:skip_test", default=True)

    def export_sources(self):
        pass

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("boost/[>=1.69.0]", transitive_headers=True)

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C++{self._min_cppstd}, which your compiler does not support."
            )

    def system_requirements(self):
        Apt(self).install(["gnuplot"])
        Yum(self).install(["gnuplot"])
        PacMan(self).install(["gnuplot"])
        Zypper(self).install(["gnuplot"])
        Chocolatey(self).install(["gnuplot"])

    def source(self):
        git = Git(self)
        git.clone(self.conan_data["sources"][self.version]["url"], target=".")
        git.checkout(self.conan_data["sources"][self.version]["commit"])

    def generate(self):

        if not self._build_tests:
            return

        tc = CMakeToolchain(self)
        tc.variables["GnuPlotIostream_BuildTests"] = True
        tc.variables["GnuPlotIostream_BuildExamples"] = False
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):

        if not self._build_tests:
            return

        replace_in_file(self, path.join(self.source_folder, "test-assert-depth.cc"), "gp.sendBinary2d(pts);", "")
        replace_in_file(self, path.join(self.source_folder, "test-assert-depth-colmajor.cc"), "gp.sendBinary2d_colmajor(pts);", "")

        cmake_lists_patches = [
            ("test-noncopyable", ""), # Gets ambiguous call
            ("test-outputs", ""), # Gets ambiguous call
            ("test-empty", ""), # Gnuplot upstream bug
            ("#options.", "include(CTest)"),
            ("add_executable(${atest} ${atest}.cc)",
             "add_executable(${atest} ${atest}.cc)\n add_test(NAME ${atest} COMMAND ${atest})"),
            ("boost_iostreams", "Boost::iostreams"),
            ("boost_system", "Boost::system"),
            ("boost_filesystem", "Boost::filesystem")]

        if self.settings.os == "Windows":
            cmake_lists_patches.append(("target_compile_options(${atest} PRIVATE -Wall -Wextra)", ""))

        for item in cmake_lists_patches:
            replace_in_file(self, path.join(self.source_folder, "CMakeLists.txt"), item[0], item[1])

        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.test()


    # Copy all files to the package folder
    def package(self):
        copy(self, pattern="gnuplot-iostream.h",
             dst=path.join(self.package_folder, "include"),
             src=self.source_folder)
        copy(self, pattern="LICENSE",
             dst=path.join(self.package_folder, "licenses"),
             src=self.source_folder)

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
