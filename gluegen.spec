Summary:	Java/JNI glue code generator to call out to ANSI C
Name:		gluegen
Version:	1.0b06
Release:	%mkrel 0.0.5
Group:		Development/Java
License:	BSD
URL:		https://gluegen.dev.java.net/
# vs -d :pserver:username@cvs.dev.java.net:/cvs checkout gluegen
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
