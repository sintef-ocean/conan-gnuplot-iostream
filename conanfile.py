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

    def requirements(self):
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
        self.info.header_only()
        self.cpp_info.cxxflags.append("-std=c++17")
