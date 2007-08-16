Summary: The Debian Almquist Shell (formerly NetBSD's ash)
Name: dash
Version: 0.5.3
Release: %mkrel 1
URL: http://ftp.debian.org/debian/pool/main/d/dash
License: BSD
Group: Shells
Source: dash_%{version}.orig.tar.bz2
Requires(post): rpm-helper
Requires(postun): rpm-helper
BuildRoot: %{_tmppath}/%name-%version
BuildRequires: bison, dietlibc-devel

%description
"dash" is a POSIX  compliant shell  that is  much smaller  than "bash".
Dash supports many features that a real sh shell would support, however
it much smaller in size. This becomes an advantage in situations  where
there is a  lack of  memery (initial  ram-disks, etc). dash does lack a 
few features, like command line history.

dash is the continuation of the original NetBSD ash fork.  dash is much
more up-to-date, and properly maintained.

You should install dash if you need a near featureful lightweight shell
that is similar to GNU's bash.

%package static
Summary: The Debian Almquist Shell (statically compiled)
License: BSD
Group: Shells
Requires(post): rpm-helper
Requires(postun): rpm-helper

%description static
"dash" is a POSIX  compliant shell  that is  much smaller  than "bash".
Dash supports many features that a real sh shell would support, however
it much smaller in size. This becomes an advantage in situations  where
there is a  lack of  memery (initial  ram-disks, etc). dash does lack a
few features, like command line history.

dash is the continuation of the original NetBSD ash fork.  dash is much
more up-to-date, and properly maintained.

You should install dash if you need a near featureful lightweight shell
that is similar to GNU's bash.

This version is statically compiled

%prep
%setup -q

%build

%configure

# Build dynamically linked dash first
make
strip src/dash
mv src/dash src/dash.dynamic

# Build statically linked dietlibc dash last
make clean
%configure CC="diet gcc"
make CC="diet gcc"
strip src/dash
mv src/dash src/dash.static



%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}/bin
mkdir -p %{buildroot}/%{_mandir}/man1

install -m 755 src/dash.dynamic %{buildroot}/bin/dash
install -m 644 src/dash.1 %{buildroot}/%{_mandir}/man1/dash.1

install -m 755 src/dash.static %{buildroot}/bin/dash.static

%post
/usr/share/rpm-helper/add-shell %name $1 /bin/dash

%post static
/usr/share/rpm-helper/add-shell %name $1 /bin/dash.static

%postun
/usr/share/rpm-helper/del-shell %name $1 /bin/dash

%postun static
/usr/share/rpm-helper/del-shell %name $1 /bin/dash.static

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/bin/dash
%{_mandir}/man1/*

%doc ChangeLog COPYING

%files static
%defattr(-,root,root)
/bin/dash.static
