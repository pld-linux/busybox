#
# Conditional build:
# alternative busybox config file (replaces default one) you should
# define cfgfile macro, i.e.
#
#       rpm --rebuild busybox.*.src.rpm --with altconfig --define "cfgfile bb-emb-config.h"
%bcond_with	altconfig	# use alternative config (defined by cfgfile)
%bcond_with	linkfl		# creates links to busybox binary and puts them into file list
# Options below are useful, when you want fileutils and grep providing.
# For example, ash package requires fileutils and grep.
%bcond_with	fileutl_prov	# adds fileutils providing
%bcond_with	grep_prov	# adds grep providing
# Option below is useful, when busybox is built with shell support.
%bcond_with	sh_prov		# adds /bin/sh providing
# WARNING! Shell, filetuils and grep providing may depend on config file!
# Fileutils, grep and shell provided with busybox have not such
# functionality as their GNU countenders.
#
%bcond_without	static		# don't build static version
%bcond_without	initrd		# don't build initrd version
%bcond_with	dietlibc	# build dietlibc-based initrd version
%bcond_with	glibc		# build glibc-based initrd version
#
%ifnarch %{ix86}
%define with_glibc 1
%endif
Summary:	Set of common unix utils for embeded systems
Summary(pl):	Zestaw narzêdzi uniksowych dla systemów wbudowanych
Summary(pt_BR):	BusyBox é um conjunto de utilitários UNIX em um único binário
Name:		busybox
Version:	1.00
%define	pre	pre10
Release:	0.%{pre}.1
License:	GPL
Group:		Applications
Source0:	http://www.busybox.net/downloads/%{name}-%{version}-%{pre}.tar.bz2
# Source0-md5:	e64c855f4b9e5e8c0645422c34499753
Source1:	%{name}.config
Source2:	%{name}-initrd.config
%{?with_altconfig:Source3:	%{cfgfile}}
Patch0:		%{name}-logconsole.patch
Patch1:		%{name}-print_ascii.patch
Patch2:		%{name}-printf-gettext.patch
Patch3:		%{name}-loadfont.patch
Patch4:		%{name}-pivot_root.patch
Patch5:		%{name}-malloc.patch
Patch6:		%{name}-raid_start.patch
Patch8:		%{name}-force-dietlibc.patch
Patch9:		%{name}-ash_exec.patch
Patch10:	%{name}-amd64.patch
Patch11:	%{name}-kernel_headers.patch
Patch12:	%{name}-insmod-morearchs.patch
URL:		http://www.busybox.net/
BuildRequires:	gcc >= 3.2
%{?with_static:BuildRequires:	glibc-static}
%if %{with initrd}
  %if %{with dietlibc}
BuildRequires:	dietlibc-static
  %else
    %if %{with glibc}
BuildRequires:	glibc-static
    %else
BuildRequires:	uClibc-static >= 0.9.21
    %endif
  %endif
%endif
%{?with_fileutl_prov:Provides:	fileutils}
%{?with_grep_prov:Provides:	grep}
%{?with_sh_prov:Provides:	/bin/sh}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_initrd_bindir	/bin

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

%description -l pl
BusyBox sk³ada ma³e wersje wielu narzêdzi uniksowych w jeden ma³y plik
wykonywalny. Zapewnia minimalne zastêpniki wiêkszo¶ci narzêdzi
zawartych w pakietach fileutils, shellutils, findutils, grep, gzip,
tar itp. BusyBox daje w miarê kompletne ¶rodowisko POSIX dla ma³ych
lub wbudowanych systemów. Narzêdzia maj± mniej opcji ni¿ ich pe³ne
odpowiedniki GNU, ale maj± podstawow± funkcjonalno¶æ. Do dzia³aj±cego
systemu potrzeba jeszcze tylko kernela, shella (np. ash) oraz edytora
(np. elvis-tiny albo ae).

%description -l pt_BR
BusyBox combina versões reduzidas de muitos utilitários UNIX num único
executável, fornecendo substitutos minimalistas para muitos dos
executáveis encontrados em pacotes como fileutils, shellutils,
findutils, textutils, grep, gzip, tar, etc. Os utilitários do BusyBox
em geral têm menos opções que os utilitários GNU, mas as opções
implementadas comportam-se de maneira similar aos equivalentes GNU.

%package static
Summary:	Static busybox
Summary(pl):	Statycznie skonsolidowany busybox
Group:		Applications

%description static
Static busybox.

%description static -l pl
Statycznie skonsolidowany busybox.

%package initrd
Summary:	Static busybox for initrd
Summary(pl):	Statycznie skonsolidowany busybox dla initrd
Group:		Applications
Conflicts:	geninitrd < 3075

%description initrd
Static busybox for initrd.

%description initrd -l pl
Statycznie skonsolidowany busybox dla initrd.

%prep
%setup -q -n %{name}-%{version}-%{pre}
%patch0 -p1
#X %patch2 -p1 // UPDATE ME
%patch3 -p1
%patch4 -p1
#%patch5 -p1 // not needed
%patch6 -p1
%patch8 -p1
%patch9 -p1
#%patch10 -p1
%patch11 -p1
#%patch12 -p1

%build
install %{SOURCE1} .config

%if %{with initrd}
install %{SOURCE2} .config
%{__make} oldconfig
%{__make} \
	CFLAGS_EXTRA="%{rpmcflags} -D_BSD_SOURCE" \
	LDFLAGS="%{rpmldflags} -static" \
%if %{with dietlibc}
	LIBRARIES="-lrpc" \
	CC="diet gcc"
%else
%if %{with glibc}
	CC="%{__cc}"
%else
	CC="%{_target_cpu}-uclibc-gcc"
%endif
%endif

mv -f busybox busybox.initrd
%{__make} clean
install %{SOURCE1} .config
%endif

%if %{with altconfig}
install %{SOURCE3} .config
%endif

%if %{with static}
%{__make} oldconfig
%{__make}  \
	CFLAGS_EXTRA="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags} -static" \
	CC="%{__cc}"
mv -f busybox busybox.static
%{__make} clean
%endif

%{__make} oldconfig
%{__make} \
	CFLAGS_EXTRA="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_initrd_bindir},%{_bindir},%{_mandir}/man1,%{_libdir}/busybox}

%{?with_static:install busybox.static $RPM_BUILD_ROOT%{_bindir}}
%{?with_initrd:install busybox.initrd $RPM_BUILD_ROOT%{_initrd_bindir}/initrd-busybox}

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
%doc AUTHORS Changelog README .config

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
