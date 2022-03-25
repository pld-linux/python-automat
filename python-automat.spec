#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Self-service finite-state machines for the programmer on the go
Summary(pl.UTF-8):	Bezobsługowe automaty skończone dla programisty w biegu
Name:		python-automat
Version:	20.2.0
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/automat/
Source0:	https://files.pythonhosted.org/packages/source/a/automat/Automat-%{version}.tar.gz
# Source0-md5:	d6cef9886b037b8857bfbc686f3ae30a
URL:		https://pypi.org/project/Automat/
%if %{with python2}
BuildRequires:	python-m2r
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-attrs >= 19.2.0
BuildRequires:	python-pytest
BuildRequires:	python-six
# it renames xml module to _xmlplus, breaking test_discover.py:WrapFQPNTests.test_singlePackage if Twisted is installed
BuildConflicts:	python-PyXML
%endif
%endif
%if %{with python3}
BuildRequires:	python3-m2r
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-attrs >= 19.2.0
BuildRequires:	python3-pytest
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Automat is a library for concise, idiomatic Python expression of
finite-state automata (particularly deterministic finite-state
transducers).

%description -l pl.UTF-8
Automat to biblioteka do zwięzłego wyrażania automatów skończonych (w
szczególności deterministycznych automatów skończończonych z wyjściem,
tj. transduktorów) w Pythonie.

%package -n python3-automat
Summary:	Self-service finite-state machines for the programmer on the go
Summary(pl.UTF-8):	Bezobsługowe automaty skończone dla programisty w biegu
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-automat
Automat is a library for concise, idiomatic Python expression of
finite-state automata (particularly deterministic finite-state
transducers).

%description -n python3-automat -l pl.UTF-8
Automat to biblioteka do zwięzłego wyrażania automatów skończonych (w
szczególności deterministycznych automatów skończończonych z wyjściem,
tj. transduktorów) w Pythonie.

%package apidocs
Summary:	API documentation for Python automat module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona automat
Group:		Documentation

%description apidocs
API documentation for Python automat module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona automat.

%prep
%setup -q -n Automat-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest automat/_test
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest automat/_test
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/automat-visualize{,-2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-automat-%{version}
cp -p docs/examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python-automat-%{version}

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/automat-visualize{,-3}
ln -sf automat-visualize-3 $RPM_BUILD_ROOT%{_bindir}/automat-visualize
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-automat-%{version}
cp -p docs/examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-automat-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/automat-visualize-2
%{py_sitescriptdir}/automat
%{py_sitescriptdir}/Automat-%{version}-py*.egg-info
%{_examplesdir}/python-automat-%{version}
%endif

%if %{with python3}
%files -n python3-automat
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/automat-visualize
%attr(755,root,root) %{_bindir}/automat-visualize-3
%{py3_sitescriptdir}/automat
%{py3_sitescriptdir}/Automat-%{version}-py*.egg-info
%{_examplesdir}/python3-automat-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,*.html,*.js}
%endif
