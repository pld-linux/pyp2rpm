#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

Summary:	Convert Python packages to RPM .spec files
Name:		pyp2rpm
Version:	3.1.2
Release:	1
License:	MIT
Group:		Development
Source0:	https://github.com/fedora-python/pyp2rpm/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b2b7f9b318f0e24f5c36ee8b85accf39
Patch0:		default-savepath.patch
Patch1:		no-rpmdev-packager.patch
Patch2:		default-distro.patch
URL:		https://github.com/fedora-python/pyp2rpm
BuildRequires:	python-flexmock >= 0.9.3
BuildRequires:	python-pytest
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-click
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
%patch2 -p1

%build
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) py.test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/pyp2rpm
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
%dir %{py_sitescriptdir}/%{name}/templates
%{py_sitescriptdir}/%{name}/templates/fedora.spec
%{py_sitescriptdir}/%{name}/templates/fedora_subdirs.spec
%{py_sitescriptdir}/%{name}/templates/macros.spec
%{py_sitescriptdir}/%{name}/templates/mageia.spec
%{py_sitescriptdir}/%{name}/templates/pld.spec
%{py_sitescriptdir}/%{name}-%{version}-py*.egg-info
