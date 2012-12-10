Summary:	Java/JNI glue code generator to call out to ANSI C
Name:		gluegen
Version:	1.0b06
Release:	%mkrel 0.0.6
Group:		Development/Java
License:	BSD
URL:		https://gluegen.dev.java.net/
# svn co https://svn.java.net/svn/gluegen~svn/branches/1.0b06-maint gluegen-1.0b06
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	ant
BuildRequires:	ant-antlr
BuildRequires:	antlr
BuildRequires:	jpackage-utils
BuildRequires:	java-rpmbuild
BuildRequires:	update-alternatives
BuildRequires:	xml-commons-apis
BuildRequires:	cpptasks
Requires:	java >= 1.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
GlueGen is a tool which automatically generates the Java and JNI code 
necessary to call C libraries. It reads as input ANSI C header files 
and separate configuration files which provide control over many aspects 
of the glue code generation. GlueGen uses a complete ANSI C parser and 
an internal representation (IR) capable of representing all C types to 
represent the APIs for which it generates interfaces. It has the ability 
to perform significant transformations on the IR before glue code emission.

GlueGen is currently powerful enough to bind even low-level APIs such as 
the Java Native Interface (JNI) and the AWT Native Interface (JAWT) 
back up to the Java programming language.

#%package javadoc
#Summary:	Javadoc for %{name}
#Group:		Development/Java

#%description javadoc
#Javadoc for %{name}.

%package manual
Summary:	User documetation for %{name}
Group:		Development/Java

%description manual
Usermanual for %{name}.


%prep
%setup -q

%build
export CLASSPATH=$(build-classpath antlr ant/ant-antlr)

pushd make
%ant all
popd

%install
rm -rf %{buildroot}

# jars
%__install -dm 755 %{buildroot}%{_javadir}
%__install -m 644 build/%{name}.jar \
	%{buildroot}%{_javadir}/%{name}-%{version}.jar
%__install -m 644 build/%{name}-rt.jar \
	%{buildroot}%{_javadir}/%{name}-rt-%{version}.jar
pushd %{buildroot}%{_javadir}
	for jar in *-%{version}*; do
		ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
	done
popd

# native lib
%__install -dm 755 %{buildroot}%{_libdir}
%__install -m 644 build/obj/lib*.so \
	%{buildroot}%{_libdir}

# javadoc
#%__install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
#%__cp -pr javadoc_jogl_dev/* \
#	%{buildroot}%{_javadocdir}/%{name}-%{version}
#ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf %{buildroot}
 
#%post javadoc
#%__rm -f %{_javadocdir}/%{name}
#ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
%attr(755,root,root) %{_libdir}/lib*.so

#%files javadoc
#%defattr(-,root,root)
#%doc %{_javadocdir}/%{name}-%{version}
#%ghost %doc %{_javadocdir}/%{name}

%files manual
%defattr(-,root,root)
%doc doc/*


%changelog
* Wed Aug 03 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.0b06-0.0.6mdv2012.0
+ Revision: 693101
- Rebuild and update from newer checkout from 1.0b06 checkout

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0b06-0.0.5mdv2011.0
+ Revision: 610865
- rebuild

* Thu Apr 29 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0b06-0.0.4mdv2010.1
+ Revision: 540947
- rebuild

* Sun Sep 27 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0b06-0.0.3mdv2010.0
+ Revision: 449798
- rebuild for new era

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Nov 09 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0b06-0.0.1mdv2009.1
+ Revision: 301390
- add buildrequires on cpptasks
- add source and spec files
- Created package structure for gluegen.

