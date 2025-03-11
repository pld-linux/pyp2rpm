#
# Conditional build:
%bcond_with	tests	# do not perform "make test". requires network access, https://github.com/fedora-python/pyp2rpm/issues/57

Summary:	Convert Python packages to RPM .spec files
Name:		pyp2rpm
Version:	3.3.2
Release:	5
License:	MIT
Group:		Development
Source0:	https://github.com/fedora-python/pyp2rpm/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	32a6c74763c1b1d8ea6a260750bd0176
Patch0:		default-savepath.patch
Patch1:		no-rpmdev-packager.patch
Patch2:		default-distro.patch
URL:		https://github.com/fedora-python/pyp2rpm
BuildRequires:	python3-flexmock >= 0.9.3
BuildRequires:	python3-setuptools
BuildRequires:	python3-wheel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-click
BuildRequires:	python3-jinja2
BuildRequires:	python3-pytest
BuildRequires:	python3-scripttest
%endif
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
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) py.test-3
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/pyp2rpm
%dir %{py3_sitescriptdir}/%{name}
%{py3_sitescriptdir}/%{name}/__pycache__
%{py3_sitescriptdir}/%{name}/*.py
%{py3_sitescriptdir}/%{name}/command
%dir %{py3_sitescriptdir}/%{name}/templates
%{py3_sitescriptdir}/%{name}/templates/epel6.spec
%{py3_sitescriptdir}/%{name}/templates/epel7.spec
%{py3_sitescriptdir}/%{name}/templates/fedora.spec
%{py3_sitescriptdir}/%{name}/templates/macros.spec
%{py3_sitescriptdir}/%{name}/templates/mageia.spec
%{py3_sitescriptdir}/%{name}/templates/pld.spec
%{py3_sitescriptdir}/%{name}-%{version}-py*.egg-info
