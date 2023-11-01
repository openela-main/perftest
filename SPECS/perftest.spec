Name:           perftest
Summary:        IB Performance Tests
# Upstream uses a dash in the version. Not valid in the Version field, so we use a dot instead.
# Issue "Please avoid dashes in version":
#   https://github.com/linux-rdma/perftest/issues/18
%global upstream_ver 4.5-0.20
Version:        %{lua: print((string.gsub(rpm.expand("%{upstream_ver}"),"-",".")))}
Release:        4%{?dist}
License:        GPLv2 or BSD
Source:         https://github.com/linux-rdma/perftest/releases/download/v4.5-0.20/perftest-4.5-0.20.gac7cca5.tar.gz
Url:            https://github.com/linux-rdma/perftest

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libibverbs-devel >= 1.2.0
BuildRequires:  librdmacm-devel >= 1.0.21
BuildRequires:  libibumad-devel >= 1.3.10.2
BuildRequires:  pciutils-devel
Obsoletes:      openib-perftest < 1.3
ExcludeArch:    s390 %{arm}

%description
Perftest is a collection of simple test programs designed to utilize 
RDMA communications and provide performance numbers over those RDMA
connections.  It does not work on normal TCP/IP networks, only on
RDMA networks.

%prep
# The directory in the tarball has only the part before the dash.
%global tarball_ver %{lua: _,_,v=string.find(rpm.expand("%{upstream_ver}"),"([^-]+)"); print(v)}

%setup -q -n %{name}-%{tarball_ver}
find src -type f -iname '*.[ch]' -exec chmod a-x '{}' ';'

%build
%configure
%make_build

%install
for file in ib_{atomic,read,send,write}_{lat,bw} raw_ethernet_{lat,bw}; do
	install -D -m 0755 $file %{buildroot}%{_bindir}/$file
done

%files
%doc README
%license COPYING
%_bindir/*

%changelog
* Tue Feb 07 2023 Michal Schmidt <mschmidt@redhat.com> - 4.5.0.20-4
- Use rpm lua code from Fedora perftest-4.5.0.20-4.fc38.
- Resolves: rhbz#2167405

* Mon Feb 06 2023 Kamal Heib <kheib@redhat.com> - 4.5.0.20-1
- Rebase to upstream release perftest-4.5-0.20
- Resolves: rhbz#2167405

* Tue Nov 09 2021 Honggang Li <honli@redhat.com> - 4.5-12
- Rebase to upstream release perftest-4.5-0.12
- Resolves: rhbz#2020061

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 4.5-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 4.5-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Mon Mar 29 2021 Honggang Li <honli@redhat.com> - 4.5-1
- Rebase to upstream release perftest-4.5-0.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Honggang Li <honli@redhat.com> - 4.4-9
- Rebase to upstream release perftest-4.4-0.37

* Sun Dec 06 2020 Honggang Li <honli@redhat.com> - 4.4-8
- Rebase to upstream release perftest-4.4-0.36

* Sun Oct 11 2020 Honggang Li <honli@redhat.com> - 4.4-7
- Rebase to upstream release perftest-4.4-0.32

* Fri Sep 18 2020 Honggang Li <honli@redhat.com> - 4.4-6
- Build perftest for s390x

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 4.4-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Sun May 24 2020 Honggang Li <honli@redhat.com> - 4.4-3
- Rebase to upstream release perftest-4.4-0.29

* Sun Apr 12 2020 Honggang Li <honli@redhat.com> - 4.4-2
- Rebase to upstream release perftest-4.4-0.23

* Mon Feb 10 2020 Honggang Li <honli@redhat.com> - 4.4-1
- Rebase to upstream release perftest-4.4-0.11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018  Honggang Li <honli@redhat.com> - 4.2-3
- Rebase to latest upstream release v4.2-0.8
- BuildRequires gcc
- Resolves: bz1605400

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 17 2018  Honggang Li <honli@redhat.com> - 4.2-1
- Rebase to latest upstream release V4.2-0.5
- Resolves: bz1568309

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 29 2016 Honggang Li <honli@redhat.com> - 3.0-1
- Update to latest upstream

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.2-1
- Update to 2.2-17

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Doug Ledford <dledford@redhat.com> - 2.0-1
- Update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 06 2012 Doug Ledford <dledford@redhat.com> - 1.3.0-2
- Update to latest upstream release
- Initial import into Fedora
- Remove runme from docs section (review item)
- Improve description of package (review item)

* Fri Jul 22 2011 Doug Ledford <dledford@redhat.com> - 1.3.0-1
- Update to latest upstream release (1.2.3 -> 1.3.0)
- Strip rocee related code out of upstream update
- Add a buildrequires on libibumad because upstream needs it now
- Fix lack of build on i686
- Related: bz725016
- Resolves: bz724896

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.2.3-3.el6
- More minor pkgwrangler cleanups
- Related: bz543948

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.2.3-2.el6
- Fixes for pkgwrangler review
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 1.2.3-1.el5
- Update to latest upstream version
- Related: bz518218

* Mon Jun 22 2009 Doug Ledford <dledford@redhat.com> - 1.2-14.el5
- Rebuild against libibverbs that isn't missing the proper ppc wmb() macro
- Related: bz506258

* Sun Jun 21 2009 Doug Ledford <dledford@redhat.com> - 1.2-13.el5
- Update to ofed 1.4.1 final bits
- Rebuild against non-XRC libibverbs
- Related: bz506097, bz506258

* Sat Apr 18 2009 Doug Ledford <dledford@redhat.com> - 1.2-12.el5
- Update to ofed 1.4.1-rc3 version
- Remove dead patch
- Related: bz459652

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 1.2-11
- Upstream has updated the tarball without updating the version, so we
  grabbed the one from the OFED-1.3.2-20080728.0355 tarball
- Resolves: bz451481

* Wed Apr 09 2008 Doug Ledford <dledford@redhat.com> - 1.2-10
- Fix the fact that the itc clock on ia64 may be a multiple of the cpu clock
- Resolves: bz433659

* Tue Apr 01 2008 Doug Ledford <dledford@redhat.com> - 1.2-9
- Update to OFED 1.3 final bits
- Related: bz428197

* Sun Jan 27 2008 Doug Ledford <dledford@redhat.com> - 1.2-8
- Split out to separate package (used to be part of openib package)
- Related: bz428197

