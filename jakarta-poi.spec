# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section         free
%define base_name       poi
%define gcj_support     1

Name:           jakarta-%{base_name}
Version:        3.0
Release:        %mkrel 3
Epoch:          0
Summary:        Java API To Access Microsoft Format Files
Group:          Development/Java
License:        Apache License
URL:            http://jakarta.apache.org/poi/
Source0:        http://www.apache.org/dist/poi/release/src/poi-src-3.0-FINAL-20070503.tar.gz
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Requires:       jakarta-commons-beanutils >= 0:1.6.1
Requires:       jakarta-commons-collections >= 0:2.1
Requires:       jakarta-commons-lang >= 0:2.0
Requires:       jakarta-commons-logging >= 0:1.0.3
Requires:       log4j >= 0:1.2.8
Requires:       xalan-j2 >= 0:2.5.2
Requires:       xerces-j2 >= 0:2.6.0
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-jdepend >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  ant-trax >= 0:1.6
BuildRequires:  jaxp_transform_impl
BuildRequires:  jakarta-commons-beanutils >= 0:1.6.1
BuildRequires:  jakarta-commons-collections >= 0:2.1
BuildRequires:  jakarta-commons-lang >= 0:2.0
BuildRequires:  jakarta-commons-logging >= 0:1.0.3
BuildRequires:  jdepend >= 0:2.6
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  log4j >= 0:1.2.8
BuildRequires:  xalan-j2 >= 0:2.5.2
BuildRequires:  xerces-j2 >= 0:2.6.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The POI project consists of APIs for manipulating 
various file formats based upon Microsoft's OLE 2 
Compound Document format using pure Java. In short, 
you can read and write MS Excel files using Java. 
Soon, you'll be able to read and write Word files 
using Java. POI is your Java Excel solution as well 
as your Java Word solution. However, we have a 
complete API for porting other OLE 2 Compound 
Document formats and welcome others to participate. 
OLE 2 Compound Document Format based files include 
most Microsoft Office files such as XLS and DOC as 
well as MFC serialization API based file formats. 

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%package        manual
Summary:        Documents for %{name}
Group:          Development/Java

%description    manual
%{summary}.


%prep
%setup -q -n %{base_name}-%{version}-rc4
%{_bindir}/find . -name "*.jar" | %{_bindir}/xargs -t %{__rm}

%{__mv} src/testcases/org/apache/poi/hpsf/basic/TestMetaDataIPI.java src/testcases/org/apache/poi/hpsf/basic/TestMetaDataIPI.java.orig
%{_bindir}/iconv -t utf8 -c src/testcases/org/apache/poi/hpsf/basic/TestMetaDataIPI.java.orig -o src/testcases/org/apache/poi/hpsf/basic/TestMetaDataIPI.java

%{__perl} -pi -e 's/<javac/<javac nowarn="true"/g' build.xml
%{__perl} -pi -e 's/fork="no"/fork="yes"/g' build.xml

%build
export OPT_JAR_LIST="ant/ant-junit junit ant/ant-jdepend jdepend jaxp_transform_impl ant/ant-trax"
export CLASSPATH=$(build-classpath commons-beanutils commons-collections commons-lang commons-logging log4j xalan-j2 xerces-j2)
export ANT_OPTS="-Xmx256m -Djava.awt.headless=true -Dbuild.sysclasspath=first -Ddisconnected=true"
# FIXME: can't run the tests because java still wants X
%{ant} jar #test

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}

%{__cp} -a build/dist/%{base_name}-%{version}-*.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__cp} -a build/dist/%{base_name}-contrib-%{version}-*.jar %{buildroot}%{_javadir}/%{name}-contrib-%{version}.jar
%{__cp} -a build/dist/%{base_name}-scratchpad-%{version}-*.jar %{buildroot}%{_javadir}/%{name}-scratchpad-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in %{name}*-%{version}.jar; do %{__ln_s} ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do %{__ln_s} ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

#javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a docs/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
%{__rm} -rf docs/apidocs

#manual
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}-%{version}
%{__cp} -a docs/* %{buildroot}%{_docdir}/%{name}-%{version}
%{__cp} -a LICENSE %{buildroot}%{_docdir}/%{name}-%{version}
%{__ln_s} %{_javadocdir}/%{name}-%{version} %{buildroot}%{_docdir}/%{name}-%{version}/apidocs # ghost symlink

%{__perl} -pi -e 's|\r$||g' \
  `%{_bindir}/find %{buildroot}%{_docdir}/%{name}-%{version} -type f \
  -name "*.css" -o -name "*.html" -o -name "*.js" -o -name "*.rss" -o -name "*.txt" -o -name "*.xml"` \
  %{buildroot}%{_docdir}/%{name}-%{version}/LICENSE

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/LICENSE
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}
