%global pkgname pagure-exporter
%global srcname pagure_exporter
%global desc Simple exporter tool that helps migrate repository files, data assets and issue tickets from projects on Pagure to GitLab

Name:           %{pkgname}
Version:        0.1.1
Release:        1%{?dist}
Summary:        %{desc}

License:        GPL-3.0-or-later
Url:            https://github.com/gridhead/%{pkgname}
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel

%description
%{desc}

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%files -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog

* Thu Oct 19 2023 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.1.1-1
- Initialized packaging workflow with RPM specfile for the project codebase
- Stepped down version of the runtime dependency requests from ^2.31.0 to ^2.28.0
- Stepped down version of the runtime dependency GitPython from ^3.1.37 to ^3.1.0
- Removed unnecessary runtime dependency tqdm from the list

* Tue Oct 17 2023 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.1.0-1
- Created the initial release of the project
- Added support for transferring repositories files from projects on Pagure to GitLab
- Added support for transferring issue tickets from projects on Pagure to GitLab
- Added support for inbuilt logging library for better compatibility with journalling
- Added options for filtering by branch names when transferring repository files
- Added options for filtering by issue ticket status when transferring issue tickets
- Added options for filtering by issue ticket identity selection when transferring issue tickets
- Added options for filtering by issue ticket identity ranges when transferring issue tickets
- Added options for migrating current states when transferring issue tickets
- Added options for migrating tagged labels when transferring issue tickets
- Added options for migrating created comments when transferring issue tickets
- Ensured excellent quality of the codebase with 100% coverage of functional code
- Included support for continuous integration using GitHub Actions and Pre-Commit CI
