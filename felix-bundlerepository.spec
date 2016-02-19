%global pkg_name felix-bundlerepository
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global site_name org.apache.felix.bundlerepository
%global grp_name  felix

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.6.6
Release:        15.9%{?dist}
Summary:        Bundle repository service
License:        ASL 2.0 and MIT
URL:            http://felix.apache.org/site/apache-felix-osgi-bundle-repository.html

Source0:        http://www.fightrice.com/mirrors/apache/felix/org.apache.felix.bundlerepository-%{version}-source-release.tar.gz
Patch1:         0001-Unbundle-libraries.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:  maven30-mvn(net.sf.kxml:kxml2)
BuildRequires:  maven30-mvn(org.apache.felix:felix-parent:pom:)
BuildRequires:  maven30-mvn(org.apache.felix:org.apache.felix.shell)
BuildRequires:  maven30-mvn(org.apache.felix:org.apache.felix.utils)
BuildRequires:  maven30-mvn(org.apache.felix:org.osgi.service.obr)
BuildRequires:  maven30-mvn(org.codehaus.woodstox:woodstox-core-asl)
BuildRequires:  maven30-mvn(org.osgi:org.osgi.compendium)
BuildRequires:  maven30-mvn(org.osgi:org.osgi.core)
BuildRequires:  %{?scl_prefix_java_common}mvn(xpp3:xpp3)
%{?fedora:BuildRequires: %{?scl_prefix}mvn(org.easymock:easymock)}


%description
Bundle repository service

%package javadoc
Summary:          API documentation for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{site_name}-%{version}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%patch1 -p1

# Parent POM pulls in unneeded dependencies (mockito)
%pom_remove_parent
%pom_xpath_inject "pom:project" "<groupId>org.apache.felix</groupId>"
%pom_add_dep junit:junit::test
%if 0%{?fedora}
  # easymock is test dependency
  %pom_xpath_inject "pom:dependency[pom:artifactId[text()='easymock']]" "<scope>test</scope>"
%else
  %pom_remove_dep org.easymock:easymock
%endif

%if !0%{?fedora}
  # These tests won't work without easymock3
  rm -f src/test/java/org/apache/felix/bundlerepository/impl/RepositoryAdminTest.java
  rm -f src/test/java/org/apache/felix/bundlerepository/impl/RepositoryImplTest.java
  rm -f src/test/java/org/apache/felix/bundlerepository/impl/StaxParserTest.java
  rm -f src/test/java/org/apache/felix/bundlerepository/impl/ResolverImplTest.java
%endif

# Add xpp3 dependency (upstream bundles this)
%pom_add_dep "xpp3:xpp3:1.1.3.4.O" pom.xml "<optional>true</optional>"

# Make felix utils mandatory dep
%pom_xpath_remove "pom:dependency[pom:artifactId[text()='org.apache.felix.utils']]/pom:optional"

# For compatibility reasons
%mvn_file : felix/%{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE LICENSE.kxml2 NOTICE DEPENDENCIES

%files javadoc -f .mfiles-javadoc
%doc LICENSE LICENSE.kxml2 NOTICE

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.6.6-15.9
- maven33 rebuild

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.6.6-15.8
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 1.6.6-15.7
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.6.6-15.6
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.6-15.5
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.6-15.4
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.6-15.3
- Mass rebuild 2014-02-18

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.6-15.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.6-15.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.6.6-15
- Mass rebuild 2013-12-27

* Wed Jul 17 2013 Michal Srb <msrb@redhat.com> - 1.6.6-14
- Fix license tag. kxml is licensed under MIT, not BSD

* Tue Jul 09 2013 Michal Srb <msrb@redhat.com> - 1.6.6-13
- Make easymock and junit test-only dependencies

* Tue Jul 09 2013 Michal Srb <msrb@redhat.com> - 1.6.6-12
- Run some tests only contidionally
- Remove unneeded BR: mockito

* Wed Jul 03 2013 Michal Srb <msrb@redhat.com> - 1.6.6-11
- Build with XMvn
- Replace patches with %%pom_ macros
- Fix BR

* Wed Jul 03 2013 Michal Srb <msrb@redhat.com> - 1.6.6-10
- Fix BR (Resolves: #979500)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.6.6-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.6.6-6
- Make felix-utils mandatory dep in pom.xml

* Mon Apr 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.6-5
- Unbundle libraries
- Add dependency on xpp3
- Include NOTICE in javadoc package
- Resolves #817581

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Jaromir Capik <jcapik@redhat.com> - 1.6.6-3
- osgi.org groupId patch removed (fixed in felix-osgi-* packages)

* Thu Oct 06 2011 Jaromir Capik <jcapik@redhat.com> - 1.6.6-2
- Depmap removed (not needed anymore)
- woodstox-core-asl renamed to woodstox-core

* Tue Sep 14 2011 Jaromir Capik <jcapik@redhat.com> - 1.6.6-1
- Initial packaging
