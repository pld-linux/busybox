Summary:	Set of common unix utils for embeded systems
Name:		busybox
Version:	0.50
Release:	1
License:	GPL
Group:		Applications/File
Patch0:		busybox-0.50.patch
Patch1:		busybox-logconsole.patch
Patch2:		busybox-tee.patch
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-config.h
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ye know..

%prep
%setup -q
%patch0 -p1
%patch1
%patch2

%build
cp %{SOURCE1} Config.h
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/usr/lib/bootdisk/{bin,config}
install -m 755 busybox $RPM_BUILD_ROOT/usr/lib/bootdisk/bin/
install -m 755 busybox.links $RPM_BUILD_ROOT/usr/lib/bootdisk/config/

gzip -9nf AUTHORS TODO Changelog README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) /usr/lib/bootdisk/bin/*
/usr/lib/bootdisk/config/*
