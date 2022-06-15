# TODO:
# - RPC/NFS with uClibc doesn't build (due to tirpc linking), so it's currently disabled
# - review patch 3. Updated to 1.17.3, but the code changed so much it's unclear
#   if it still serves a purpose
# - sparc64 modules support in sparc(32), x86_64 modules support in i386 version
# - make internal commands work even if busybox is not in /bin/busybox (initrd)
#   or when /proc is not mounted (static / normal)
#
# Conditional build:
# alternative busybox config file (replaces default one) you should
# define cfgfile macro, i.e.
#
#	rpm --rebuild busybox.*.src.rpm --with altconfig --define "cfgfile bb-emb-config.h"
#
%bcond_with	altconfig	# use alternative config (defined by cfgfile)
%bcond_with	linkfl		# creates links to busybox binary and puts them into file list
%bcond_without	dynamic		# don't build dynamic (base) version
%bcond_without	static		# don't build static version
%bcond_without	initrd		# don't build initrd version
%bcond_with	dietlibc	# build dietlibc-based initrd and static versions
%bcond_with	glibc		# build glibc-based initrd and static versions
%bcond_without	verbose		# verbose build
# Options below are useful, when you want fileutils and grep providing.
# For example, ash package requires fileutils and grep.
%bcond_with	fileutl_prov	# adds fileutils providing
%bcond_with	grep_prov	# adds grep providing
# Option below is useful, when busybox is built with shell support.
%bcond_with	sh_prov		# adds /bin/sh providing
# WARNING! Shell, fileutils and grep providing may depend on config file!
# Fileutils, grep and shell provided with busybox have not such
# functionality as their GNU countenders.
#
%ifnarch %{ix86} %{x8664} ppc
%define		with_glibc	1
%endif
%ifarch x32
# until uClibc builds on x32
%undefine	with_static
%endif
Summary:	Set of common Unix utilities for embeded systems
Summary(pl.UTF-8):	Zestaw narzędzi uniksowych dla systemów wbudowanych
Summary(pt_BR.UTF-8):	BusyBox é um conjunto de utilitários UNIX em um único binário
Name:		busybox
# stable line only
Version:	1.35.0
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	585949b1dd4292b604b7d199866e9913
Source1:	%{name}.config
Source2:	%{name}-initrd.config
%{?with_altconfig:Source3:	%{cfgfile}}
Patch0:		x32.patch
Patch1:		%{name}-logconsole.patch
Patch2:		%{name}-printf-gettext.patch
Patch3:		%{name}-loadfont.patch
Patch4:		%{name}-kernel_headers.patch
Patch5:		%{name}-insmod-morearchs.patch
Patch6:		%{name}-dhcp.patch
Patch7:		%{name}-fix_64_archs.patch
Patch8:		busybox-1.31.1-stime-fix.patch
Patch9:		%{name}-ash-export-PATH.patch
Patch10:	0001-modutils-check-ELF-header-before-calling-finit_module.patch
URL:		http://www.busybox.net/
BuildRequires:	gcc >= 3.2
BuildRequires:	perl-tools-pod
BuildRequires:	rpmbuild(macros) >= 1.652
%if %{with glibc}
BuildRequires:	libtirpc-devel
BuildRequires:	pkgconfig
%endif
%if %{with initrd} || %{with static}
	%if %{with dietlibc}
BuildRequires:	dietlibc-static
	%else
		%if %{with glibc}
BuildRequires:	glibc-static
BuildRequires:	libtirpc-static
		%else
%if "%{_target_base_arch}" != "%{_host_base_arch}"
BuildRequires:	cross%{_target_base_arch}-uClibc-static
%else
	%ifarch ppc %{x8664}
BuildRequires:	uClibc-static >= 3:0.9.30.1
	%else
BuildRequires:	uClibc-static >= 3:0.9.30.1
	%endif
%endif
		%endif
	%endif
%endif
%{?with_sh_prov:Provides:	/bin/sh}
%{?with_fileutl_prov:Provides:	fileutils}
%{?with_grep_prov:Provides:	grep}
Provides:	busybox-implementation = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0

%define		_bindir		/bin

%if "%{_target_base_arch}" != "%{_host_base_arch}"
	%define CrossOpts CROSS="%{_target_cpu}-pld-linux-"
%else
	%define CrossOpts %{nil}
%endif

%define		filterout_ld	-Wl,-z,(combreloc|relro)

%if %{with glibc}
%define		tirpccflags	%(pkg-config --cflags libtirpc)
%if %{with initrd} || %{with static}
%define		tirpcslibs	%(pkg-config --libs --static libtirpc|sed s/-l//g)
%endif
%if %{with dynamic}
%define		tirpcdlibs	%(pkg-config --libs libtirpc|sed s/-l//g)
%endif
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

%description -l pl.UTF-8
BusyBox składa małe wersje wielu narzędzi uniksowych w jeden mały plik
wykonywalny. Zapewnia minimalne zastępniki większości narzędzi
zawartych w pakietach fileutils, shellutils, findutils, grep, gzip,
tar itp. BusyBox daje w miarę kompletne środowisko POSIX dla małych
lub wbudowanych systemów. Narzędzia mają mniej opcji niż ich pełne
odpowiedniki GNU, ale mają podstawową funkcjonalność. Do działającego
systemu potrzeba jeszcze tylko kernela, shella (np. ash) oraz edytora
(np. elvis-tiny albo ae).

%description -l pt_BR.UTF-8
BusyBox combina versões reduzidas de muitos utilitários UNIX num único
executável, fornecendo substitutos minimalistas para muitos dos
executáveis encontrados em pacotes como fileutils, shellutils,
findutils, textutils, grep, gzip, tar, etc. Os utilitários do BusyBox
em geral têm menos opções que os utilitários GNU, mas as opções
implementadas comportam-se de maneira similar aos equivalentes GNU.

%package static
Summary:	Static busybox
Summary(pl.UTF-8):	Statycznie skonsolidowany busybox
Group:		Applications

%description static
Static busybox.

%description static -l pl.UTF-8
Statycznie skonsolidowany busybox.

%package initrd
Summary:	Static busybox for initrd
Summary(pl.UTF-8):	Statycznie skonsolidowany busybox dla initrd
Group:		Base
Conflicts:	geninitrd < 10000.20
Provides:	busybox-implementation = %{version}-%{release}

%description initrd
Static busybox for initrd.

%description initrd -l pl.UTF-8
Statycznie skonsolidowany busybox dla initrd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
install -d built
%if %{with initrd}
install %{SOURCE2} .config
echo 'CONFIG_EXTRA_LDLIBS="%{?with_glibc:%{tirpcslibs}}"' >> .config
%{__make} oldconfig
%{__make} \
	%{?with_verbose:V=1} \
	EXTRA_CFLAGS="%{rpmcflags} %{?with_glibc:%{tirpccflags}} -Os -D_GNU_SOURCE %{!?with_glibc:-fno-stack-protector}" \
	EXTRA_LDFLAGS="%{rpmldflags} -static -Wl,-z,noexecstack" \
%if %{with dietlibc}
	LIBRARIES="-lrpc" \
	CC="diet %{__cc}"
%else
%if %{with glibc}
	%{CrossOpts} \
	CC="%{__cc}"
%else
	%if "%{_target_base_arch}" != "%{_host_base_arch}"
	CROSS="%{_target_cpu}-uclibc-" \
	%endif
	CC="%{_target_cpu}-uclibc-gcc"
%endif
%endif

mv -f busybox built/busybox.initrd
%{__make} clean
%endif

%if %{with static}
%if %{with altconfig}
install %{SOURCE3} .config
%else
install %{SOURCE1} .config
echo 'CONFIG_EXTRA_LDLIBS="%{?with_glibc:%{tirpcslibs}}"' >> .config
%endif
%{__make} oldconfig
%{__make} \
	%{?with_verbose:V=1} \
	EXTRA_CFLAGS="%{rpmcflags} %{?with_glibc:%{tirpccflags}} -Os -D_GNU_SOURCE %{!?with_glibc:-fno-stack-protector}" \
	EXTRA_LDFLAGS="%{rpmldflags} -static -Wl,-z,noexecstack" \
%if %{with dietlibc}
	LIBRARIES="-lrpc" \
	CC="diet %{__cc}"
%else
%if %{with glibc}
	%{CrossOpts} \
	CC="%{__cc}"
%else
	%if "%{_target_base_arch}" != "%{_host_base_arch}"
	CROSS="%{_target_cpu}-uclibc-" \
	%endif
	CC="%{_target_cpu}-uclibc-gcc"
%endif
%endif

mv -f busybox built/busybox.static
%{__make} clean
%endif

%if %{with dynamic}
%if %{with altconfig}
install %{SOURCE3} .config
%else
install %{SOURCE1} .config
echo 'CONFIG_EXTRA_LDLIBS="%{?with_glibc:%{tirpcdlibs}}"' >> .config
%endif
%{__make} oldconfig
%{__make} \
	%{?with_verbose:V=1} \
	%{CrossOpts} \
	EXTRA_CFLAGS="%{rpmcflags} %{?with_glibc:%{tirpccflags}} %{!?with_glibc:-fno-stack-protector}" \
	EXTRA_LDFLAGS="%{rpmldflags} -Wl,-z,noexecstack" \
	CC="%{__cc}"
%{__make} busybox.links docs/busybox.1
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static}
install -d $RPM_BUILD_ROOT%{_bindir}
install built/busybox.static $RPM_BUILD_ROOT%{_bindir}
%endif

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd
install built/busybox.initrd $RPM_BUILD_ROOT%{_libdir}/initrd/busybox
%endif

%if %{with dynamic}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir}/busybox}
install busybox.links $RPM_BUILD_ROOT%{_libdir}/busybox
install docs/busybox.1 $RPM_BUILD_ROOT%{_mandir}/man1

# install links to busybox binary, when linkfl is defined
%if %{with linkfl}
%{__make} install \
	PREFIX=$RPM_BUILD_ROOT
%else
install busybox $RPM_BUILD_ROOT%{_bindir}
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with dynamic}
%files
%defattr(644,root,root,755)
%doc AUTHORS README .config

%if %{with linkfl}
%attr(755,root,root) /bin/*
%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%else
%attr(755,root,root) %{_bindir}/busybox
%endif

%{_libdir}/busybox
%{_mandir}/man1/busybox.1*
%endif

%if %{with static}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/busybox.static
%endif

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/initrd/busybox
%endif
