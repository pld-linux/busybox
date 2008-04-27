# TODO:
#	- sparc64 modules support in sparc(32), x86_64 modules support in i386 version
#	- make internal commands work even if busybox is not in /bin/busybox (initrd)
#	  or when /proc is not mounted (static / normal)
#
# Conditional build:
# alternative busybox config file (replaces default one) you should
# define cfgfile macro, i.e.
#
#	rpm --rebuild busybox.*.src.rpm --with altconfig --define "cfgfile bb-emb-config.h"
%bcond_with	altconfig	# use alternative config (defined by cfgfile)
%bcond_with	linkfl		# creates links to busybox binary and puts them into file list
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
%bcond_without	static		# don't build static version
%bcond_without	initrd		# don't build initrd version
%bcond_with	dietlibc	# build dietlibc-based initrd version
%bcond_with	glibc		# build glibc-based initrd version
#
%ifnarch %{ix86} %{x8664} ppc
%define with_glibc 1
%endif
Summary:	Set of common Unix utilities for embeded systems
Summary(pl.UTF-8):	Zestaw narzędzi uniksowych dla systemów wbudowanych
Summary(pt_BR.UTF-8):	BusyBox é um conjunto de utilitários UNIX em um único binário
Name:		busybox
Version:	1.10.1
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	953c5d829a3ff11014f41c6c1b446eb8
Source1:	%{name}.config
Source2:	%{name}-initrd.config
%{?with_altconfig:Source3:	%{cfgfile}}
Patch1:		%{name}-logconsole.patch
Patch2:		%{name}-printf-gettext.patch
Patch3:		%{name}-loadfont.patch
Patch4:		%{name}-ash_exec.patch
Patch5:		%{name}-kernel_headers.patch
Patch6:		%{name}-insmod-morearchs.patch
Patch7:		%{name}-dhcp.patch
Patch8:		%{name}-fix_64_archs.patch
URL:		http://www.busybox.net/
BuildRequires:	gcc >= 3.2
BuildRequires:	perl-tools-pod
BuildRequires:	rpmbuild(macros) >= 1.333
%{?with_static:BuildRequires:	glibc-static}
%if %{with initrd}
	%if %{with dietlibc}
BuildRequires:	dietlibc-static
	%else
		%if %{with glibc}
BuildRequires:	glibc-static
		%else
%if "%{_target_base_arch}" != "%{_arch}"
BuildRequires:	cross%{_target_base_arch}-uClibc-static
%else
	%ifarch ppc %{x8664}
BuildRequires:	uClibc-static >= 2:0.9.29
	%else
BuildRequires:	uClibc-static >= 2:0.9.21
	%endif
%endif
		%endif
	%endif
%endif
%{?with_fileutl_prov:Provides:	fileutils}
%{?with_grep_prov:Provides:	grep}
%{?with_sh_prov:Provides:	/bin/sh}
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
Group:		Applications
Conflicts:	geninitrd < 3075

%description initrd
Static busybox for initrd.

%description initrd -l pl.UTF-8
Statycznie skonsolidowany busybox dla initrd.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
install -d built
%if %{with initrd}
install %{SOURCE2} .config
%{__make} oldconfig
%{__make} \
	CROSS_CFLAGS="%{rpmcflags} -Os -D_BSD_SOURCE" \
	LDFLAGS="%{ld_rpmldflags} -static" \
%if %{with dietlibc}
	LIBRARIES="-lrpc" \
	CC="diet gcc"
%else
%if %{with glibc}
	%{CrossOpts} \
	CC="%{__cc}"
%else
    %if "%{_target_base_arch}" != "%{_arch}"
	CROSS="%{_target_cpu}-uclibc-" \
    %endif
	CC="%{_target_cpu}-uclibc-gcc"
%endif
%endif

mv -f busybox built/busybox.initrd
%{__make} clean
%endif


%if %{with altconfig}
install %{SOURCE3} .config
%else
install %{SOURCE1} .config
%endif

%if %{with static}
%{__make} oldconfig
%{__make} \
	%{CrossOpts} \
	CFLAGS_EXTRA="%{rpmcflags}" \
	LDFLAGS="%{ld_rpmldflags} -static" \
	CC="%{__cc}"
mv -f busybox built/busybox.static
%{__make} clean
%endif

%{__make} oldconfig
%{__make} \
	%{CrossOpts} \
	CFLAGS_EXTRA="%{rpmcflags}" \
	LDFLAGS="%{ld_rpmldflags}" \
	CC="%{__cc}"
%{__make} busybox.links docs/BusyBox.1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_initrd_bindir},%{_bindir},%{_mandir}/man1,%{_libdir}/busybox}

%{?with_static:install built/busybox.static $RPM_BUILD_ROOT%{_bindir}}
%{?with_initrd:install built/busybox.initrd $RPM_BUILD_ROOT%{_initrd_bindir}/initrd-busybox}

install busybox.links $RPM_BUILD_ROOT%{_libdir}/busybox
install docs/BusyBox.1 $RPM_BUILD_ROOT%{_mandir}/man1
echo ".so BusyBox.1" > $RPM_BUILD_ROOT%{_mandir}/man1/busybox.1

# install links to busybox binary, when linkfl is defined
%if %{with linkfl}
%{__make} install \
	PREFIX=$RPM_BUILD_ROOT
%else
install busybox $RPM_BUILD_ROOT%{_bindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_mandir}/man1/*

%if %{with static}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/busybox.static
%endif

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_initrd_bindir}/initrd-busybox
%endif
