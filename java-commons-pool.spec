#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%include	/usr/lib/rpm/macros.java

%define		srcname	commons-pool
Summary:	Commons Pool - object pooling interfaces
Summary(pl.UTF-8):	Commons Pool - interfejsy gospodarujące obiektami
Name:		java-commons-pool
Version:	1.5.4
Release:	1
License:	Apache
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/commons/pool/source/commons-pool-%{version}-src.tar.gz
# Source0-md5:	4216bb6eca49e7b3db9f287d7b0c0cd8
Source1:	jakarta-commons-pool-tomcat5-build.xml
URL:		http://commons.apache.org/pool/
BuildRequires:	ant
BuildRequires:	java-commons-collections >= 1.0
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-commons-collections >= 1.0
Requires:	jpackage-utils
Provides:	jakarta-commons-pool
Obsoletes:	jakarta-commons-pool
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Pool package defines a generalized object pooling interfaces, and
provides several general-purpose implementations.

%description -l pl.UTF-8
Pakiet Pool definiuje uogólnione interfejsy gospodarowania obiektami
oraz dostarcza kilku implementacji ogólnego przeznaczenia.

%package javadoc
Summary:	Commons Pool documentation
Summary(pl.UTF-8):	Dokumentacja do Commons Pool
Group:		Documentation
Provides:	jakarta-commons-pool-javadoc
Obsoletes:	jakarta-commons-pool-doc
Obsoletes:	jakarta-commons-pool-javadoc

%description javadoc
Commons Pool documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do Commons Pool.

%package tomcat5
Summary:	Commons Pool dependency for Tomcat5
Summary(pl.UTF-8):	Elementy Commons Pool dla Tomcata 5
Group:		Development/Languages/Java
Provides:	jakarta-commons-pool-tomcat5
Obsoletes:	jakarta-commons-pool-source
Obsoletes:	jakarta-commons-pool-tomcat5

%description tomcat5
Commons Pool dependency for Tomcat5.

%description tomcat5 -l pl.UTF-8
Elementy Commons Pool dla Tomcata 5.

%prep
%setup -q -n commons-pool-%{version}-src
cp %{SOURCE1} tomcat5-build.xml

%build
required_jars="commons-collections"
export CLASSPATH=$(build-classpath $required_jars)
%ant clean
%ant build-jar %{?with_javadoc:javadoc}
%ant -f tomcat5-build.xml

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a dist/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

cp -a pool-tomcat5/%{srcname}-tomcat5.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-tomcat5-%{version}.jar
ln -sf %{srcname}-tomcat5-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-tomcat5.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc RELEASE-NOTES.txt
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%files tomcat5
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-tomcat5.jar
%{_javadir}/%{srcname}-tomcat5-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
