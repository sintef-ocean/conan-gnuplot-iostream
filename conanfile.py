from conans import ConanFile, tools


class GnuplotIostreamConan(ConanFile):
    name = "gnuplot-iostream"
    version = "2020.06.20"
    license = "MIT"
    author = "Joakim Haugen joakim.haugen@sintef.no"
    url = "https://gitlab.kluster.no/sintef/fkin/conan-gnuplot-iostream.git"
    homepage = "https://github.com/dstahlke/gnuplot-iostream"
    description = "Iostream pipe to gnuplot with some extra functions " \
        "for pushing data arrays and getting mouse clicks"
    topics = ("gnuplot", "plotting")
    no_copy_source = True
    settings = "compiler"
    options = {"with_boost": [True, False]}
    default_options = ("with_boost=True")

    def configure(self):
        if not tools.valid_min_cppstd(self, "17"):
            self.output.warn(
                "C++17 is required, setting settings.compiler.cppstd=17")
            self.settings.compiler.cppstd = 17

    def requirements(self):

        if self.options.with_boost:
            self.requires("boost_iostreams/[>=1.69.0]@bincrafters/stable")
            self.requires("boost_filesystem/[>=1.69.0]@bincrafters/stable")
            self.requires("boost_system/[>=1.69.0]@bincrafters/stable")

    def source(self):
        _git = tools.Git()
        _git.clone("https://github.com/dstahlke/gnuplot-iostream.git",
                   branch="3a8c001a38304d7bfebb9edf91df5be8e3deaa57",
                   shallow=True)

    def build(self):
        pass

    def system_requirements(self):
        if tools.os_info.is_windows:
            if not tools.which("gnuplot"):
                if tools.which("choco"):
                    installer = tools.SystemPackageTool(
                        tool=tools.ChocolateyTool())
                    installer.install("gnuplot")
                else:
                    self.output.warn(
                        "Make sure to install gnuplot and that it is on PATH")
        else:
            installer = tools.SystemPackageTool()
            installer.install("gnuplot")

    def package(self):
        self.copy("gnuplot-iostream.h", dst="include")
        self.copy("LICENSE", dst="licenses")

    def package_info(self):

        if self.options.with_boost:
            self.cpp_info.cxxflags.append(tools.cppstd_flag(self.settings))
        else:
            self.info.header_only()

    def package_id(self):

        if self.options.with_boost:
            del self.info.settings.compiler.version
            del self.info.settings.compiler.libcxx
            del self.info.settings.compiler.threads
            del self.info.settings.compiler.runtime
            del self.info.settings.compiler.runtime_type
            del self.info.settings.compiler.exception
