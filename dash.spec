%bcond_without	musl

Summary:	The Debian Almquist Shell (formerly NetBSD's ash)
Name:		dash
Version:	0.5.7
Release:	10
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
BuildRequires:	musl-devel

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
mv src/dash src/dash.dynamic

%if %{with musl}
# Build statically linked dietlibc dash last
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


%changelog
* Sat Aug 20 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.5.7-1mdv2012.0
+ Revision: 695918
- update to new version 0.5.7
- rediff patch 0

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5.6.1-2
+ Revision: 663750
- mass rebuild

* Sun Aug 01 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0.5.6.1-1mdv2011.0
+ Revision: 564823
- Patch0: fix format not a string...
- update to new version 0.5.6.1
- update links for URL and SOURCE0
- compile with -Os flag

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.5.1-3mdv2010.1
+ Revision: 520064
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5.5.1-2mdv2010.0
+ Revision: 413326
- rebuild

* Wed Feb 18 2009 Jérôme Soyer <saispo@mandriva.org> 0.5.5.1-1mdv2009.1
+ Revision: 342435
- New upstream release

* Thu Dec 18 2008 Pixel <pixel@mandriva.com> 0.5.4-10mdv2009.1
+ Revision: 315726
- add explicit file provide /bin/dash

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0.5.4-9mdv2009.0
+ Revision: 264384
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5.4-8mdv2009.0
+ Revision: 217537
- rebuilt against dietlibc-devel-0.32

* Thu Feb 28 2008 Anssi Hannula <anssi@mandriva.org> 0.5.4-7mdv2008.1
+ Revision: 176252
- dash-static conflicts with old dash

* Thu Feb 28 2008 Pixel <pixel@mandriva.com> 0.5.4-6mdv2008.1
+ Revision: 176168
- add explicit file provide /dash.static

* Wed Feb 27 2008 Pixel <pixel@mandriva.com> 0.5.4-5mdv2008.1
+ Revision: 175832
- also remove "Requires(post,postun): rpm-helper" (cf previous commit)

* Wed Feb 27 2008 Pixel <pixel@mandriva.com> 0.5.4-4mdv2008.1
+ Revision: 175823
- dash-static can't have %%post/%%preun using bash otherwise we get loop
  (we could restore %%pro/%%preun from old ash package, but it needs testing)

* Wed Feb 27 2008 Pixel <pixel@mandriva.com> 0.5.4-3mdv2008.1
+ Revision: 175822
- ash was static, so move obsolete,provides,/bin/ash to dash-static

* Mon Jan 28 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.4-2mdv2008.1
+ Revision: 159211
- whoops, wrong order for symlink
- provides and obsoletes ash (#21233 for e.g.)
- provide /bin/ash and matching manpage
- rewrap description
- spec clean

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 0.5.4-1mdv2008.1
+ Revision: 136360
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Pascal Terjan <pterjan@mandriva.org>
    - 0.5.4
    - Import dash

  + Jérôme Soyer <saispo@mandriva.org>
    - New release 0.5.4



* Wed Dec 07 2005 Michael Scherer <misc@mandriva.org> 0.5.3-1mdk
- New release 0.5.3
- use mkrel
- remove patch 0, implemented upstream
- remove PreReq

* Fri Feb 11 2005 Michael Scherer <misc@mandrake.org> 0.5.2-1mdk
- rpmbuildupdateable
- From Sunny Dubey <sdubey@nylug.org>  
  * Removed debian specific patch
  * updated to 0.5.2

* Mon Nov 29 2004 Michael Scherer <misc@mandrake.org> 0.5.1-3mdk 
- various adjustement ( .bz2, prereq, etc )
- uploaded to contribs

* Tue Nov 23 2004 Sunny Dubey <sunny@opencurve.org> 0.5.1-2mdk
- Fixed dietlibc support

* Tue Nov 23 2004 Sunny Dubey <sunny@opencurve.org> 0.5.1-1mdk
- Initial Mandrake release :)

* Tue Jun 29 2004 Sunny Dubey <sunny@opencurve.org>
- use $(command) instead of `command`
- add to %%doc

* Fri Jun 25 2004 Sunny Dubey <sunny@opencurve.org>
- No more mindless copying/renaming during build

* Thu Jun 24 2004 Sunny Dubey <sunny@opencurve.org>
- Brand-spanking new package (no more unmaintained ash)
- patched mktemp issue
