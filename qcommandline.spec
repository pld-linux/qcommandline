Summary:	Command line parser for Qt programs
Name:		qcommandline
Version:	0.3.0
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://xf.iksaif.net/dev/qcommandline/%{name}-%{version}.tar.bz2
# Source0-md5:	89cb472a54306c7399c55285e142a84c
# http://dev.iksaif.net/issues/253
Patch0:		%{name}-fix-pkg-config-paths.patch
# http://dev.iksaif.net/issues/252 -- enhancements for PhantomJS
Patch101:	0001-new-ParameterFence-flag.patch
Patch102:	0002-new-NoShortName-flag-to-allow-options-with-no-short-.patch
Patch103:	0003-new-SuppressHelp-flag.patch
URL:		http://xf.iksaif.net/dev/qcommandline.html
BuildRequires:	QtCore-devel
BuildRequires:	cmake
BuildRequires:	pkgconfig
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QCommandLine is a command line parser for Qt programs (like getopt).

Features include options, switches, parameters and automatic
'--version' and '--help' generation.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for building against %{name}.

%prep
%setup -q
%patch0 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_MODULES_INSTALL_DIR=%{_datadir}/cmake/Modules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

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
