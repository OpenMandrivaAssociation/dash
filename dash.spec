# Currently debug is empty so rpmlint rejects build
%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%bcond_without	diet

Summary:	The Debian Almquist Shell (formerly NetBSD's ash)
Name:		dash
Version:	0.5.9
Release:	0.1
License:	BSD
Group:		Shells
URL:		http://gondor.apana.org.au/~herbert/dash/
Source0:	http://gondor.apana.org.au/~herbert/dash/files/%{name}-%{version}.tar.gz
Patch0:		dash-0.5.7-format-not-a-string-literal-and-no-format-arguments.patch
Patch1:		dash-0.5.7-hack-to-fix-test-build.patch
Requires(post):	rpm-helper
Requires(postun):	rpm-helper
# explicit file provide:
Provides:		/bin/dash
BuildRequires:	bison
BuildRequires:	dietlibc-devel

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
Obsoletes:	ash < %{version}
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
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="%{optflags} -Os"
export CXXFLAGS=$CFLAGS

%configure2_5x

# Build dynamically linked dash first
%make
%{__strip} src/dash
mv src/dash src/dash.dynamic

%if %{with diet}
# Build statically linked dietlibc dash last
make clean
%configure2_5x CC="diet gcc"
%make CC="diet gcc"
%{__strip} src/dash
mv src/dash src/dash.static
%endif

%install

mkdir -p %{buildroot}/bin
mkdir -p %{buildroot}/%{_mandir}/man1

install -m 755 src/dash.dynamic %{buildroot}/bin/dash
install -m 644 src/dash.1 %{buildroot}%{_mandir}/man1/dash.1

%if %{with diet}
install -m 755 src/dash.static %{buildroot}/bin/dash.static
ln -s /bin/dash.static %{buildroot}/bin/ash
ln -s %{_mandir}/man1/dash.1 %{buildroot}%{_mandir}/man1/ash.1
%endif

%post
/usr/share/rpm-helper/add-shell %{name} $1 /bin/dash

%postun
/usr/share/rpm-helper/del-shell %{name} $1 /bin/dash

%files
%doc ChangeLog COPYING
/bin/dash
%{_mandir}/man1/*

%if %{with diet}
%files static
%doc ChangeLog COPYING
/bin/dash.static
/bin/ash
%endif
