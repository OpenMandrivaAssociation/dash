%define Werror_cflags %nil

Summary:	The Debian Almquist Shell (formerly NetBSD's ash)
Name:		dash
Version:	0.5.6.1
Release:	%mkrel 1
License:	BSD
Group:		Shells
URL:		http://gondor.apana.org.au/~herbert/dash/
Source:		http://gondor.apana.org.au/~herbert/dash/files/%{name}-%{version}.tar.gz
Requires(post):		rpm-helper
Requires(postun):	rpm-helper
# explicit file provide:
Provides:	/bin/dash
BuildRequires:	bison
BuildRequires:	dietlibc-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
"dash" is a POSIX compliant shell that is much smaller than "bash".
Dash supports many features that a real sh shell would support, however
it is much smaller in size. This becomes an advantage in situations
where there is a lack of memery (initial ram-disks, etc). dash does
lack a few features, like command line history.

dash is the continuation of the original NetBSD ash fork. dash is much
more up-to-date, and properly maintained.

You should install dash if you need a near featureful lightweight shell
that is similar to GNU's bash.

%package static
Summary:	The Debian Almquist Shell (statically compiled)
License:	BSD
Group:		Shells
Obsoletes:	ash
Provides:	ash
Conflicts:	dash < 0.5.4-3
# explicit file provide:
Provides:	/bin/dash.static

%description static
"dash" is a POSIX compliant shell that is much smaller than "bash".
Dash supports many features that a real sh shell would support, however
it is much smaller in size. This becomes an advantage in situations
where there is a lack of memery (initial ram-disks, etc). dash does
lack a few features, like command line history.

dash is the continuation of the original NetBSD ash fork. dash is much
more up-to-date, and properly maintained.

You should install dash if you need a near featureful lightweight shell
that is similar to GNU's bash.

This version is statically compiled.

%prep
%setup -q

%build
export CFLAGS="%{optflags} -Os"
export CXXFLAGS=$CFLAGS

%configure2_5x

# Build dynamically linked dash first
%make
strip src/dash
mv src/dash src/dash.dynamic

# Build statically linked dietlibc dash last
make clean
%configure2_5x CC="diet gcc"
%make CC="diet gcc"
strip src/dash
mv src/dash src/dash.static

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/bin
mkdir -p %{buildroot}/%{_mandir}/man1

install -m 755 src/dash.dynamic %{buildroot}/bin/dash
install -m 644 src/dash.1 %{buildroot}%{_mandir}/man1/dash.1

install -m 755 src/dash.static %{buildroot}/bin/dash.static

ln -s /bin/dash.static %{buildroot}/bin/ash
ln -s %{_mandir}/man1/dash.1 %{buildroot}%{_mandir}/man1/ash.1

%post
/usr/share/rpm-helper/add-shell %{name} $1 /bin/dash

%postun
/usr/share/rpm-helper/del-shell %{name} $1 /bin/dash

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog COPYING
/bin/dash
%{_mandir}/man1/*

%files static
%doc ChangeLog COPYING
%defattr(-,root,root)
/bin/dash.static
/bin/ash
