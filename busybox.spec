Summary:	Set of common unix utils for embeded systems
Summary(pl):	Zestaw narzêdzi uniksowych dla systemów wbudowanych
Name:		busybox
Version:	0.60.1
Release:	15
License:	GPL
Group:		Applications
Group(de):	Applikationen
Group(es):	Aplicaciones
Group(pl):	Aplikacje
Group(pt):	Aplicações
Group(pt_BR):	Aplicações
Source0:	ftp://ftp.lineo.com/pub/busybox/%{name}-%{version}.tar.gz
Source1:	%{name}-config.h
Patch0:		%{name}-logconsole.patch
Patch1:		%{name}-tee.patch
Patch3:		%{name}-printf-gettext.patch
Patch4:		%{name}-loadfont.patch
Patch5:		%{name}-cread.patch
Patch6:		%{name}-malloc.patch
Patch7:		%{name}-pivot_root.patch
URL:		http://busybox.lineo.com/
%{?BOOT:BuildRequires:	uClibc-devel-BOOT >= 20010521-3}
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

%package static
Summary:	Static busybox
Summary(pl):	Statycznie linkowany busybox
Group:		Applications
Group(de):	Applikationen
Group(es):	Aplicaciones
Group(pl):	Aplikacje
Group(pt):	Aplicações
Group(pt_BR):	Aplicações

%description static
Static busybox.

%description static -l pl
Statycznie linkowany busybox.

%package BOOT
Summary:	busybox for PLD bootdisk
Summary(pl):	busybox dla bootkietki PLD
Group:		Applications
Group(de):	Applikationen
Group(es):	Aplicaciones
Group(pl):	Aplikacje
Group(pt):	Aplicações
Group(pt_BR):	Aplicações

%description BOOT
busybox for PLD bootdisk.

%description BOOT -l pl
busybox dla bootkietki PLD.

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
# BOOT
%if %{?BOOT:1}%{!?BOOT:0}
%{__make} \
	CFLAGS_EXTRA="-I%{_libdir}/bootdisk%{_includedir}" \
	LDFLAGS="-nostdlib" \
	LIBRARIES="%{_libdir}/bootdisk%{_libdir}/crt0.o %{_libdir}/bootdisk%{_libdir}/libc.a -lgcc"
mv -f busybox busybox-BOOT
%{__make} clean
%endif

%if %{?_without_static:0}%{!?_without_static:1}
%{__make} \
	CFLAGS_EXTRA="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags} -static"
mv -f busybox busybox.static
%{__make} clean
%endif

%{__make} \
	CFLAGS_EXTRA="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"
	
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir}/busybox}

%if %{?BOOT:1}%{!?BOOT:0}
install -d $RPM_BUILD_ROOT%{_libdir}/bootdisk/{bin,%{_libdir}}

install busybox-BOOT $RPM_BUILD_ROOT%{_libdir}/bootdisk/bin/busybox

for i in `cat busybox.links`; do
	ln -sfn busybox "$RPM_BUILD_ROOT%{_libdir}/bootdisk/bin/`basename $i`"
done
install busybox.links $RPM_BUILD_ROOT%{_libdir}/bootdisk%{_libdir}/busybox
%endif

%{!?_without_static:install busybox.static $RPM_BUILD_ROOT%{_bindir}}

install busybox $RPM_BUILD_ROOT%{_bindir}
install busybox.links $RPM_BUILD_ROOT%{_libdir}/busybox
install docs/BusyBox.1 $RPM_BUILD_ROOT%{_mandir}/man1
echo ".so BusyBox.1" > $RPM_BUILD_ROOT%{_mandir}/man1/busybox.1

gzip -9nf AUTHORS TODO Changelog README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/busybox
%{_libdir}/busybox
%{_mandir}/man1/*

%if %{?_without_static:0}%{!?_without_static:1}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/busybox.static
%endif

%if %{?BOOT:1}%{!?BOOT:0}
%files BOOT
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bootdisk/bin/*
%{_libdir}/bootdisk%{_libdir}/*
%endif
