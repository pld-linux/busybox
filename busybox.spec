
#
# _with_altconfig <name>  - alternative busybox config file (replaces default one)
#                           you should define cfgfile macro, i.e.
#
#       rpm --rebuild busybox.*.src.rpm --with altconfig --define "cfgfile bb-emb-config.h"
#
#
# _with_linkfl            - creates links to busybox binary and puts them into file list;
#
# Options below are useful, when you want fileutils and grep providing.
# For example, ash package requires fileutils and grep.
#
# _with_fileutl_prov      - adds fileutils providing
# _with_grep_prov         - adds grep providing
#
#
# Option below is useful, when busybox is built with shell support.
#
# _with_sh_prov           - adds /bin/sh providing
#
#
# WARNING! Shell, filetuils and grep providing may depend on config file!
# Fileutils, grep and shell provided with busybox have not such
# functionality as their GNU countenders.
#
#
# _without_static         - don't build static version
#

Summary:	Set of common unix utils for embeded systems
Summary(pl):	Zestaw narzêdzi uniksowych dla systemów wbudowanych
Summary(pt_BR):	BusyBox é um conjunto de utilitários UNIX em um único binário
Name:		busybox
Version:	0.60.2
Release:	7
License:	GPL
Group:		Applications
Source0:	ftp://ftp.lineo.com/pub/busybox/%{name}-%{version}.tar.gz
%{!?_with_altconfig:Source1:	%{name}-config.h}
%{?_with_altconfig:Source1:	%{cfgfile}}
Patch0:		%{name}-logconsole.patch
Patch1:		%{name}-tee.patch
Patch3:		%{name}-printf-gettext.patch
Patch4:		%{name}-loadfont.patch
Patch5:		%{name}-cread.patch
Patch6:		%{name}-malloc.patch
Patch7:		%{name}-pivot_root.patch
URL:		http://busybox.lineo.com/
%{?_with_fileutl_prov:Provides:	fileutils}
%{?_with_grep_prov:Provides:	grep}
%{?_with_sh_prov:Provides:	/bin/sh}
%{!?_without_static:BuildRequires:	glibc-static}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Summary(pl):	Statycznie linkowany busybox
Group:		Applications

%description static
Static busybox.

%description static -l pl
Statycznie linkowany busybox.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
cp -f %{SOURCE1} Config.h

%if %{?_without_static:0}%{!?_without_static:1}
%{__make} \
	CFLAGS_EXTRA="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags} -static"
mv -f busybox busybox.static
%{__make} clean
%endif

%{__make} \
	CFLAGS_EXTRA="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir}/busybox}

%{!?_without_static:install busybox.static $RPM_BUILD_ROOT%{_bindir}}

%{?!_with_linkfl:install busybox $RPM_BUILD_ROOT%{_bindir}}
install busybox.links $RPM_BUILD_ROOT%{_libdir}/busybox
install docs/BusyBox.1 $RPM_BUILD_ROOT%{_mandir}/man1
echo ".so BusyBox.1" > $RPM_BUILD_ROOT%{_mandir}/man1/busybox.1

# install links to busybox binary, when linkfl is defined
%{?_with_linkfl:make install PREFIX=$RPM_BUILD_ROOT}

gzip -9nf AUTHORS TODO Changelog README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz

%{?!_with_linkfl: %attr(755,root,root) %{_bindir}/busybox}

%if %{?_with_linkfl:1}%{?!_with_linkfl:0}
%attr(755,root,root) /bin/*
%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%endif

%{_libdir}/busybox
%{_mandir}/man1/*

%if %{?_without_static:0}%{!?_without_static:1}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/busybox.static
%endif
