Name:           perftest
Summary:        IB Performance Tests
# Upstream uses a dash in the version. Not valid in the Version field, so we use a dot instead.
# Issue "Please avoid dashes in version":
#   https://github.com/linux-rdma/perftest/issues/18
%global upstream_ver 23.04.0-0.23
Version:        %{lua: print((string.gsub(rpm.expand("%{upstream_ver}"),"-",".")))}
Release:        2%{?dist}
License:        GPLv2 or BSD
Source:         https://github.com/linux-rdma/perftest/releases/download/23.04.0-0.23/perftest-23.04.0-0.23.g63e250f.tar.gz
Source1:	ib_atomic_bw.1
Url:            https://github.com/linux-rdma/perftest
Patch01: 0001-perftest-Add-Intel-device-names-and-inline-data-size.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libibverbs-devel >= 1.2.0
BuildRequires:  librdmacm-devel >= 1.0.21
BuildRequires:  libibumad-devel >= 1.3.10.2
BuildRequires:  pciutils-devel
Obsoletes:      openib-perftest < 1.3

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
%patch01 -p1

%build
%configure
%make_build

%install
for file in ib_{atomic,read,send,write}_{lat,bw} raw_ethernet_{lat,bw}; do
	install -D -m 0755 $file %{buildroot}%{_bindir}/$file
done
mkdir -p %{buildroot}%{_mandir}/man1/
install -D -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/
pushd %{buildroot}%{_mandir}/man1/
for file in ib_atomic_lat ib_{read,send,write}_{lat,bw} raw_ethernet_{lat,bw}; do
	ln -s ib_atomic_bw.1 ${file}.1
done
popd

%files
%doc README
%{_mandir}/man1/*
%license COPYING
%_bindir/*

%changelog
* Tue Jul 18 2023 Kamal Heib <kheib@redhat.com> - 23.04.0.0.23-2
- Add missing Intel Parameters
- Resolves: rhbz#2211464

* Mon Jun 05 2023 Kamal Heib <kheib@redhat.com> - 23.04.0.0.23-1
- Update to upstream release 23.04.0.0.23
- Add gating tests
- Resolves: rhbz#2212517

* Wed Feb 08 2023 Michal Schmidt <mschmidt@redhat.com> - 4.5.0.20-4
- Rebase to upstream version 4.5-0.20
- Resolves: rhbz#2168109

* Wed Nov 10 2021 Honggang Li <honli@redhat.com> - 4.5-12
- Rebase to upstream release perftest-4.5-0.12
- Resolves: rhbz#2020062

* Thu May 13 2021 Honggang Li <honli@redhat.com> - 4.5-1
- Rebase to upstream release perftest-4.5-0.2
- Resolves: rhbz#1960074

* Sat Jan 30 2021 Honggang Li <honli@redhat.com> - 4.4-8
- Check PCIe relaxed ordering compliant
- Resolves: rhbz#1902855

* Thu Nov 05 2020 Honggang Li <honli@redhat.com> - 4.4-7
- Rebase to upstream release perftest-4.4-0.32
- Resolves: bz1888570

* Fri Jul 24 2020 Honggang Li <honli@redhat.com> - 4.4-3
- Fix segment fault with large QP numbers
- Resolves: rhbz#1859358

* Mon May 25 2020 Honggang Li <honli@redhat.com> - 4.4-2
- Update to upstream 4.4-0.29.g817ec38 tarball
- Resolves: rhbz#1832709

* Wed Apr 15 2020 Honggang Li <honli@redhat.com> - 4.4-1
- Update to upstream 4.4-0.23.g89e176a tarball
- Resolves: rhbz#1817830

* Mon Jul 23 2018 Jarod Wilson <jarod@redhat.com> - 4.2-2
- Update to upstream 4.2-0.8.g0e24e67 tarball

* Mon Apr 30 2018 Jarod Wilson <jarod@redhat.com> - 4.2-1
- Update to upstream 4.2-0.5.gdd28746 tarball

* Mon Apr 03 2017 Jarod Wilson <jarod@redhat.com> - 3.4-1
- Update to upstream 3.4-0.9.g98a9a17 tarball
- Resolves: rhbz#1437978

* Thu Aug 18 2016 Jarod Wilson <jarod@redhat.com> - 3.0-7
- Address a myriad more coverity/clang warnings
- Add raw_ethernet_* man page symlinks
- Related: rhbz#1273176
- Related: rhbz#948476

* Mon Aug 15 2016 Jarod Wilson <jarod@redhat.com> - 3.0-6
- Update to upstream 3.0-3.1.gb36a595 tarball for upstream fixes
- Add in manpages
- Related: rhbz#1365750
- Resolves: rhbz#948476

* Fri Aug 12 2016 Jarod Wilson <jarod@redhat.com> - 3.0-5
- Make it possible to actually test with XRC connections again
- Resolves: rhbz#1365750

* Mon Aug 08 2016 Jarod Wilson <jarod@redhat.com> - 3.0-4
- Install raw_ethernet{lat,bw} tools
- Resolves: rhbz#1365182

* Wed May 18 2016 Jarod Wilson <jarod@redhat.com> - 3.0-3
- Fix additional memory leaks reported and spotted after last fix

* Wed May 18 2016 Jarod Wilson <jarod@redhat.com> - 3.0-2
- Fix issues uncovered by coverity

* Wed May 04 2016 Jarod Wilson <jarod@redhat.com> - 3.0-1
- Update to upstream release v3.0
- Resolves: bz1309586, bz1273176

* Tue Jun 16 2015 Michal Schmidt <mschmidt@redhat.com> - 2.4-1
- Update to latest upstream release
- Enable s390x platform
- Resolves: bz1182177

* Fri Oct 17 2014 Doug Ledford <dledford@redhat.com> - 2.3-1
- Update to latest upstream release
- Resolves: bz1061582

* Tue May 20 2014 Kyle McMartin <kmcmarti@redhat.com> - 2.0-4
- aarch64: add get_cycles implementation since <asm/timex.h> is no longer
  exported by the kernel.
- Resolves: #1100043

* Thu Jan 23 2014 Doug Ledford <dledford@redhat.com> - 2.0-3
- Fix for rpmdiff found issues
- Related: bz1017321

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0-2
- Mass rebuild 2013-12-27

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

