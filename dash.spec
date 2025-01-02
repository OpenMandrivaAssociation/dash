%define _disable_rebuild_configure 1

Summary:	The Debian Almquist Shell (formerly NetBSD's ash)
Name:		dash
Version:	0.5.12
Release:	1
License:	BSD
Group:		Shells
URL:		https://gondor.apana.org.au/~herbert/dash/
Source0:	http://gondor.apana.org.au/~herbert/dash/files/%{name}-%{version}.tar.gz
#Patch0:		dash-0.5.7-format-not-a-string-literal-and-no-format-arguments.patch
#Patch1:		dash-0.5.7-hack-to-fix-test-build.patch
Requires(post):	rpm-helper
Requires(postun):	rpm-helper
# explicit file provide:
Provides:	/bin/dash
BuildRequires:	bison

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

%prep
%autosetup -p1

%build
%configure --bindir=%{_bindir}

# Build dynamically linked dash first
%make_build
mv src/dash src/dash.dynamic

%install

mkdir -p %{buildroot}/bin
mkdir -p %{buildroot}/%{_mandir}/man1

install -m 755 src/dash.dynamic %{buildroot}/bin/dash
install -m 644 src/dash.1 %{buildroot}%{_mandir}/man1/dash.1

%post
/usr/share/rpm-helper/add-shell %{name} $1 /bin/dash

%postun
/usr/share/rpm-helper/del-shell %{name} $1 /bin/dash

%files
/bin/dash
%doc %{_mandir}/man1/*
