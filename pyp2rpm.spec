#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

Summary:	Convert Python packages to RPM .spec files
Name:		pyp2rpm
Version:	1.0.1
Release:	1
License:	MIT
Group:		Applications
Source0:	http://pypi.python.org/packages/source/p/pyp2rpm/%{name}-%{version}.tar.gz
# Source0-md5:	1e9a514d8dab9782f699ded2eb268237
# to get tests:
# git clone git@bitbucket.org:bkabrda/pyp2rpm.git && cd pyp2rpm
# git checkout v1.0.1 && tar czf pyp2rpm-1.0.1-tests.tgz tests/
Source1:	%{name}-%{version}-tests.tgz
# Source1-md5:	d6ffe3cd0acb10af01c99a77e6bd51f3
Patch0:		default-savepath.patch
Patch1:		no-rpmdev-packager.patch
URL:		https://pypi.python.org/pypi/pyp2rpm
BuildRequires:	python-flexmock >= 0.9.3
BuildRequires:	python-pytest
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-jinja2
Requires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Convert Python packages to RPM .spec.

Users can provide their own templates for rendering the package
metadata. Both the package source and metadata can be extracted from
PyPI or from local filesystem (local file doesn't provide that much
information though).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
# Remove bundled egg-info
rm -r %{name}.egg-info

%build
%{__python} setup.py build

%if %{with tests}
PYTHONPATH=$(pwd) py.test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(755,root,root) %{_bindir}/pyp2rpm
%{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}-%{version}-py*.egg-info
