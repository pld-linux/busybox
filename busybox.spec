Summary:	Set of common unix utils for embeded systems
Name:		busybox
Version:	0.51
Release:	3
License:	GPL
Group:		Applications
Group(de):	Applikationen
Group(pl):	Aplikacje
Source0:	ftp://ftp.lineo.com/pub/busybox/%{name}-%{version}.tar.gz
Source1:	%{name}-config.h
Patch0:		%{name}-logconsole.patch
Patch1:		%{name}-tee.patch
Patch2:		%{name}-sh-name.patch
URL:		http://busybox.lineo.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	uClibc-devel-BOOT

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

%package BOOT
Summary:	busybox for PLD bootdisk
Group:		Applications
Group(de):	Applikationen
Group(pl):	Aplikacje

%description BOOT
busybox for PLD bootdisk.

%prep
%setup -q
%patch0
%patch1
%patch2 -p1

%build
# BOOT
cp %{SOURCE1} Config.h
%{__make} \
	CFLAGS_EXTRA="-I%{_libdir}/bootdisk%{_includedir}" \
	LDFLAGS="-nostdlib -s" \
	LIBRARIES="%{_libdir}/bootdisk%{_libdir}/crt0.o %{_libdir}/bootdisk%{_libdir}/libc.a -lgcc"

# TODO make main package dynamically linked

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
%{__install} -d $RPM_BUILD_ROOT%{_libdir}/bootdisk/{bin,%{_libdir}/busybox}

%{__install} busybox $RPM_BUILD_ROOT%{_libdir}/bootdisk/bin/

for i in `cat busybox.links`; do
	ln -sfn busybox "$RPM_BUILD_ROOT%{_libdir}/bootdisk/bin/`basename $i`"
done
%{__install} busybox.links $RPM_BUILD_ROOT%{_libdir}/bootdisk%{_libdir}/busybox
# change sh to lash (see sh_name patch)
mv -f $RPM_BUILD_ROOT%{_libdir}/bootdisk/bin/{sh,lash}

%{__install} busybox $RPM_BUILD_ROOT%{_bindir}
%{__install} busybox.links $RPM_BUILD_ROOT%{_libdir}/busybox
%{__install} docs/BusyBox.1 $RPM_BUILD_ROOT%{_mandir}/man1
echo ".so BusyBox.1" > $RPM_BUILD_ROOT%{_mandir}/man1/busybox.1

gzip -9nf AUTHORS TODO Changelog README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_libdir}/busybox
%{_mandir}/man1/*

%files BOOT
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bootdisk/bin/*
%{_libdir}/bootdisk%{_libdir}/*
