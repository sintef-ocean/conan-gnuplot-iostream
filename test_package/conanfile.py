from conans import ConanFile, CMake, tools, RunEnvironment


class GnuplotIostreamTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake", "cmake_find_package", "virtualrunenv")

    options = {"shared": [True, False]}
    default_options = ("shared=False")
    _cmake = None

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure()
        return self._cmake

    def configure(self):
        self.options["boost_filesystem"].shared = self.options.shared
        self.options["boost_system"].shared = self.options.shared
        self.options["boost_iostreams"].shared = self.options.shared
        self.options["zstd"].shared = self.options.shared

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def test(self):
        if tools.cross_building(self.settings):
            print("NOT RUN (cross-building)")
            return

        cmake = self._configure_cmake()
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            cmake.test()
