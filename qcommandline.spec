#
# Conditional build:
%bcond_without	qt4		# build Qt4
%bcond_without	qt5		# build Qt5

Summary:	Command line parser for Qt programs
Name:		qcommandline
Version:	0.3.0
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://xf.iksaif.net/dev/qcommandline/%{name}-%{version}.tar.bz2
# Source0-md5:	89cb472a54306c7399c55285e142a84c
Patch0:		%{name}-fix-pkg-config-paths.patch
Patch1:		0001-qt5.patch
Patch101:	0001-new-ParameterFence-flag.patch
Patch102:	0002-new-NoShortName-flag-to-allow-options-with-no-short-.patch
Patch103:	0003-new-SuppressHelp-flag.patch
URL:		http://xf.iksaif.net/dev/qcommandline.html
%if %{with qt4}
BuildRequires:	QtCore-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-qmake
%endif
BuildRequires:	cmake
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#    File(s) packaged into both qcommandline-devel-0.3.0-1.i686 and qcommandline-qt5-devel-0.3.0-1.i686:
#        /usr/include/qcommandline/QCommandLine
#        /usr/include/qcommandline/qcommandline.h
#        /usr/share/cmake/Modules/FindQCommandLine.cmake
%define	_duplicate_files_terminate_build	0

%description
QCommandLine is a command line parser for Qt programs (like getopt).

Features include options, switches, parameters and automatic
'--version' and '--help' generation.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for building against %{name}.

%package qt5
Summary:	Command line parser for Qt5 programs

%description qt5
QCommandLine is a command line parsing library for Qt5 programs (like
getopt).

Features include options, switches, parameters and automatic
'--version' and '--help' generation.

%package qt5-devel
Summary:	Development files for %{name}-qt5
Requires:	%{name}-qt5 = %{version}-%{release}

%description qt5-devel
Development files for building against %{name}.

%prep
%setup -q
%patch0 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1

%if %{with qt5}
set -- *
install -d qt5
cp -al "$@" qt5
cd qt5
%patch1 -p1
# rename the library to libqcommandline-qt5 to distinguish it from the Qt4 build
echo "set_target_properties(qcommandline PROPERTIES OUTPUT_NAME qcommandline-qt5)" >>CMakeLists.txt
sed -i -e 's/-lqcommandline/-lqcommandline-qt5/' QCommandLine.pc.in
sed -i -e 's/QCommandLine\.pc$/QCommandLine-qt5.pc/' CMakeLists.txt
%endif

%build
%if %{with qt4}
install -d build-qt4
cd build-qt4
%cmake .. \
	-DCMAKE_MODULES_INSTALL_DIR=%{_datadir}/cmake/Modules
%{__make}
cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
%cmake ../qt5 \
	-DCMAKE_MODULES_INSTALL_DIR=%{_datadir}/cmake/Modules
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with qt4}
%{__make} -C build-qt4 install \
	DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif

%if %{with qt5}
%{__make} -C build-qt5 install \
	DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-qt5-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-qt5-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}.so
%{_includedir}/%{name}
%{_pkgconfigdir}/QCommandLine.pc
%{_datadir}/cmake/Modules/FindQCommandLine.cmake
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with qt5}
%files qt5
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}-qt5.so.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}-qt5.so.0

%files qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}-qt5.so
%{_includedir}/%{name}
%{_pkgconfigdir}/QCommandLine-qt5.pc
%{_datadir}/cmake/Modules/FindQCommandLine.cmake
%{_examplesdir}/%{name}-qt5-%{version}
%endif
