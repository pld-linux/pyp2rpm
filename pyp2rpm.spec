#
# Conditional build:
%bcond_with	tests	# do not perform "make test"

Summary:	Convert Python packages to RPM .spec files
Name:		pyp2rpm
Version:	2.0.0
Release:	0.1
License:	MIT
Group:		Applications
Source0:	http://pypi.python.org/packages/source/p/pyp2rpm/%{name}-%{version}.tar.gz
# Source0-md5:	935066a6d90f13f673753c0ce27d98e0
# to get tests:
# git clone git@bitbucket.org:bkabrda/pyp2rpm.git && cd pyp2rpm
# git checkout v1.0.1 && tar czf pyp2rpm-1.0.1-tests.tgz tests/
#Source1:	http://pkgs.fedoraproject.org/repo/pkgs/pyp2rpm/%{name}-%{version}-tests.tgz/159412b3603fdcc673c0a8c731bc22c4/pyp2rpm-%{version}-tests.tgz
## Source1-md5:	159412b3603fdcc673c0a8c731bc22c4
Source2:	pld.spec.tmpl
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

# Remove bundled egg-info
rm -r %{name}.egg-info

#cp -p %{SOURCE2} pyp2rpm/templates/pld.spec

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
%doc LICENSE
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
