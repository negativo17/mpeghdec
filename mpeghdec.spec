# The NEON routines are emitted as top level asm() without .globl, which LTO
# does not see; the references are then undefined in the shared library.
%ifarch %{arm} aarch64
%global _lto_cflags %{nil}
%endif

Name:           mpeghdec
Version:        4.0.1
Release:        2%{?dist}
Summary:        Fraunhofer MPEG-H decoder
License:        Software License for The Fraunhofer FDK MPEG-H Software
URL:            https://github.com/Fraunhofer-IIS/mpeghdec

Source0:        %{url}/archive/r%{version}/%{name}-%{version}.tar.gz
# Upstream sets no SOVERSION, and includes GNUInstallDirs after the install()
# calls so the library lands in %%{_prefix}/lib:
Patch0:         %{name}-cmake.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
The Fraunhofer MPEG-H decoder is a C/C++ implementation of the MPEG-H Audio
standard as defined in ISO/IEC 23008-3:2022. It decodes MPEG-H Audio streams
and provides the UI manager used to apply interactivity and scene settings.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}-r%{version}

# The project version is not bumped with the release tag, and it ends up in the
# pkg-config file and in the SOVERSION:
sed -i -E 's/^(\s*VERSION\s+)[0-9.]+$/\1%{version}/' CMakeLists.txt

%build
# The demo binaries pull ilo and mmtisobmff in over the network with
# FetchContent; nothing else needs them.
%cmake \
    -DBUILD_SHARED_LIBS=ON \
    -Dmpeghdec_BUILD_BINARIES=OFF
%cmake_build

%install
%cmake_install

# Installed into %%{_datadir} by upstream, but it carries %%{_libdir} in it:
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{_datadir}/pkgconfig/%{name}.pc %{buildroot}%{_libdir}/pkgconfig/

%files
%license LICENSE.txt
%doc AUTHORS.md CHANGELOG.md README.md
%{_libdir}/lib%{name}.so.4
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Sep 18 2026 Simone Caronni <negativo17@gmail.com> - 4.0.1-2
- Disable LTO on ARM, it drops the NEON routines.

* Fri Sep 18 2026 Simone Caronni <negativo17@gmail.com> - 4.0.1-1
- Clean up SPEC file and update to 4.0.1.

* Sun Feb 15 2026 Simone Caronni <negativo17@gmail.com> - 3.0.2-1
- First build.
