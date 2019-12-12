%global srcname pip
%global bashcompdir /usr/share/bash-completion/completions/


Name:           python2-%{srcname}

Version:        19.1.1
Release:        7%{?dist}
Summary:        A tool for installing and managing Python2 packages



License:        MIT and Python and ASL 2.0 and BSD and ISC and LGPLv2 and MPLv2.0 and (ASL 2.0 or BSD)
URL:            http://www.pip-installer.org
Source0:        %pypi_source

BuildArch:      noarch


%description
Pip for the deprecated python2
pip is a package management system used to install and manage software packages
written in Python. Many packages can be found in the Python Package Index
(PyPI). pip is a recursive acronym that can stand for either "Pip Installs
Packages" or "Pip Installs Python".


BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  ca-certificates
BuildRequires:	python2-rpm-macros

Requires:       ca-certificates
Requires:       python2-setuptools


%prep
%setup -q -n %{srcname}-%{version}


# new
rm -rf "src/pip/_vendor/!(__init__.py)"
  sed -i -e 's/DEBUNDLED = False/DEBUNDLED = True/' \
            "src/pip/_vendor/__init__.py"

%build

%py2_build


%install

%py2_install


  mv "%{buildroot}/usr/bin/pip" "%{buildroot}/usr/bin/pip2"
  sed -i "s|#!/usr/bin/env python$|#!/usr/bin/python2|" \
    %{buildroot}/usr/lib/python2.7/site-packages/pip/__init__.py
  python2 -m compileall %{buildroot}/usr/lib/python2.7/site-packages/pip/__init__.py

#  install -Dm644 -t "%{buildroot}"/usr/share/man/man1 docs/build/man-pip2/*

  PYTHONPATH="%{buildroot}"/usr/lib/python2.7/site-packages "%{buildroot}"/usr/bin/pip2 completion --bash \
    | install -Dm644 /dev/stdin "%{buildroot}"/usr/share/bash-completion/completions/pip2

pushd %{buildroot}/usr/share/bash-completion/completions/
ln -sf pip2 pip-2
popd

pushd %{buildroot}/usr/bin/
ln -sf pip2 pip-2
popd


%files 
%license LICENSE.txt
%doc README.rst
%{_bindir}/pip2
%{_bindir}/pip-2
%{_bindir}/pip2.7
%{bashcompdir}/pip2
%{bashcompdir}/pip-2
%{python2_sitelib}/pip*



%changelog

* Tue Dec 10 2019 David Va <davidva AT tuta DOT io> - 19.1.1-7
- Initial build
