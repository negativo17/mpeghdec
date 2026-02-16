Name:           mpeghdec
Version:        3.0.2
Release:        1%{?dist}
Summary:        C/C++ implementation of the MPEG-H Audio standard
License:        asd
URL:            https://github.com/Fraunhofer-IIS/mpeghdec

Source0:        %{url}/archive/r%{version}/%{name}-r%{version}.tar.gz
Patch0:         %{name}-shared.patch
Patch1:         %{name}-path.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
The Fraunhofer MPEG-H decoder (mpeghdec) is a C/C++ implementation of the MPEG-H
Audio standard as defined in ISO/IEC 23008-3:2022. MPEG-H Audio is the Next
Generation Audio (NGA) codec for personalized and immersive sound.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}-r%{version}

%build
%cmake \
    -Dmpeghdec_BUILD_BINARIES=OFF \
    -Dmpeghdec_BUILD_DOC=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSE.txt
%doc README.md CHANGELOG.md AUTHORS.md
%{_libdir}/*.so.*

%files devel
%{_datadir}/pkgconfig/mpeghdec.pc
%{_includedir}/%{name}
%{_libdir}/*.so

%changelog
* Sun Feb 15 2026 Simone Caronni <negativo17@gmail.com> - 3.0.2-1
- First build.

