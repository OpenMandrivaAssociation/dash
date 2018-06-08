%ifnarch %arm aarch64
%bcond_without	musl
%else
%bcond_with	musl
%endif

Summary:	The Debian Almquist Shell (formerly NetBSD's ash)
Name:		dash
Version:	0.5.10.2
Release:	1
License:	BSD
Group:		Shells
URL:		http://gondor.apana.org.au/~herbert/dash/
Source0:	http://gondor.apana.org.au/~herbert/dash/files/%{name}-%{version}.tar.gz
Patch0:		dash-0.5.7-format-not-a-string-literal-and-no-format-arguments.patch
Patch1:		dash-0.5.7-hack-to-fix-test-build.patch
Requires(post):	rpm-helper
Requires(postun):	rpm-helper
# explicit file provide:
Provides:	/bin/dash
BuildRequires:	bison
%if %{with musl}
BuildRequires:	musl-devel
%endif

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

%if %{with musl}
%package static
Summary:	The Debian Almquist Shell (statically compiled)
License:	BSD
Group:		Shells
Obsoletes:	ash < %{version}
Provides:	ash = %{version}
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
%endif

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure

# Build dynamically linked dash first
%make
mv src/dash src/dash.dynamic

%if %{with musl}
# Build statically linked musl dash
make clean
%configure CC="musl-gcc"
%make CC="musl-gcc"
mv src/dash src/dash.static
%endif

%install

mkdir -p %{buildroot}/bin
mkdir -p %{buildroot}/%{_mandir}/man1

install -m 755 src/dash.dynamic %{buildroot}/bin/dash
install -m 644 src/dash.1 %{buildroot}%{_mandir}/man1/dash.1

%if %{with musl}
install -m 755 src/dash.static %{buildroot}/bin/dash.static
ln -s /bin/dash.static %{buildroot}/bin/ash
ln -s %{_mandir}/man1/dash.1 %{buildroot}%{_mandir}/man1/ash.1
%endif

%post
/usr/share/rpm-helper/add-shell %{name} $1 /bin/dash

%postun
/usr/share/rpm-helper/del-shell %{name} $1 /bin/dash

%files
/bin/dash
%{_mandir}/man1/*

%if %{with musl}
%files static
/bin/dash.static
/bin/ash
%endif
