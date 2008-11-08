#
Summary:	Set of common unix utils for embeded systems
Name:		busybox
Version:	1.12.1
Release:	1
License:	GPL
Group:		Applications
Source0:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	dc2e5e00d6fee8229ae92884c68733a7
Source1:	%{name}-initrd.config
Source2:	%{name}-system.config
Patch0:		%{name}-grep.patch
Patch1:		%{name}-modprobe.patch
Patch2:		%{name}-standalone.patch
Patch3:		%{name}-vi.patch
Patch4:		%{name}-lineedit.patch
Patch5:		%{name}-basename.patch
Patch6:		%{name}-login.patch
URL:		http://www.busybox.net/
BuildRequires:	gcc >= 3.2
BuildRequires:	perl-tools-pod
BuildRequires:	rpmbuild(macros) >= 1.333
BuildRequires:	uClibc-static >= 2:0.9.21
#ExclusiveArch:	i586
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin
%define		_initrd_bindir	/bin

%if "%{_target_base_arch}" != "%{_arch}"
	%define CrossOpts CROSS="%{_target_cpu}-pld-linux-"
%else
	%define CrossOpts %{nil}
%endif

%description
BusyBox combines tiny versions of many common UNIX utilities into a
single small executable. It provides minimalist replacements for most
of the utilities you usually find in fileutils, shellutils, findutils,
textutils, grep, gzip, tar, etc. BusyBox provides a fairly complete
POSIX environment for any small or embedded system. The utilities in
BusyBox generally have fewer options than their full-featured GNU
cousins; however, the options that are included provide the expected
functionality and behave very much like their GNU counterparts.

BusyBox has been written with size-optimization and limited resources
in mind. It is also extremely modular so you can easily include or
exclude commands (or features) at compile time. This makes it easy to
customize your embedded systems. To create a working system, just add
a kernel, a shell (such as ash), and an editor (such as elvis-tiny or
ae).

%package CRI-initrd
Summary:	Busybox for CRI initrd images
Group:		Applications
Conflicts:	geninitrd < 3075

%description CRI-initrd
Busybox for CRI initrd images.

%package CRI-system
Summary:	Busybox for CRI system images
Group:		Applications
Conflicts:	geninitrd < 3075

%description CRI-system
Busybox for CRI system images.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
install -d built
install %{SOURCE1} .config
%{__make} oldconfig
%{__make} \
	CROSS_CFLAGS="%{rpmcflags} -Os -D_BSD_SOURCE" \
	LDFLAGS="%{ld_rpmldflags} -static" \
%if "%{_target_base_arch}" != "%{_arch}"
	CROSS="%{_target_cpu}-uclibc-" \
%endif
	CC="%{_target_cpu}-uclibc-gcc"

mv -f busybox built/busybox.initrd
%{__make} clean

install %{SOURCE2} .config
%{__make} oldconfig
%{__make} \
	CROSS_CFLAGS="%{rpmcflags} -Os -D_BSD_SOURCE" \
	LDFLAGS="%{ld_rpmldflags} -static" \
%if "%{_target_base_arch}" != "%{_arch}"
	CROSS="%{_target_cpu}-uclibc-" \
%endif
	CC="%{_target_cpu}-uclibc-gcc"

mv -f busybox built/busybox.system
%{__make} clean


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install built/busybox.initrd $RPM_BUILD_ROOT%{_bindir}
install built/busybox.system $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files CRI-initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/busybox.initrd

%files CRI-system
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/busybox.system
