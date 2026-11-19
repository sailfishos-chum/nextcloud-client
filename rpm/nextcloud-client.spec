Name:       qt56-nextcloud-client

%global     packagever 2.6.5
%global     packagesrc desktop-%{packagever}

Summary:    Nextcloud command line sync client
Version:    2.6.5
Release:    0
License:    GPLv2
URL:        https://github.com/nextcloud/desktop
Source0:    %{name}-%{version}.tar.gz
Source1:    %{packagesrc}.tar.gz
Patch0:     no-webengine.patch
Patch1:     no-gui-%{packagever}.patch
Patch2:     qasconst.patch
Patch3:     libssl-1.0.patch
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(sqlite3)
#BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
#BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig
BuildRequires:  cmake
BuildRequires:  qt5-qttools-linguist
BuildRequires:  qt5-qmake
BuildRequires:  qt5keychain-devel

%if 0%{?sailfishos_version} <= 40500
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
%endif

Provides: nextcloud-client = %{version}

%description
%{summary}.

NOTE: The library installs in /usr/lib/nextcloud for compatability reasons with OwnCloud.
This means you will have to have that path in your LD_LIBRARY_PATH variable to use the client.

Also be aware that because of the old version of Qt used in Sailfish OS,
the version of this client is *old*.  There might be security and/or
compatability issues.

%if 0%{?_chum}
Title: Nextcloud Sync Client (Qt5.6)
Type: console-application
PackagedBy: nephros
Categories:
 - Utility
 - FileTools
 - NetworkFilesystems
Custom:
  Repo: https://github.com/nextcloud/desktop
  PackagingRepo: https://github.com/sailfishos-chum/nextcloud-client
PackageIcon: https://avatars.githubusercontent.com/u/19211038?s=200&v=4
Links:
  Homepage: https://nextcloud.com/install/#install-clients
  Help: https://github.com/sailfishos-chum/nextcloud-client/-/blob/%{version}/README_SailfishOS.md
%endif


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name}-libs = %{version}-%{release}
Provides:   nextcloud-client-devel = %{version}-%{release}

%description devel
%{summary}.


%package libs
Summary:    Libraries for %{name}
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:   nextcloud-client-libs = %{version}-%{release}

%description libs
%{summary}.

%if 0%{?_chum}
Title: Nextcloud Client Libraries
PackagedBy: nephros
Categories:
 - Library
Custom:
  Repo: https://github.com/nextcloud/desktop
  PackagingRepo: https://github.com/sailfishos-chum/nextcloud-client
PackageIcon: https://avatars.githubusercontent.com/u/19211038?s=200&v=4
Links:
  Homepage: https://nextcloud.com/install/#install-clients
%endif

%prep
%setup -q -a 1 -n %{name}-%{version}

pushd %{packagesrc}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%if 0%{?sailfishos_version} < 40001
%patch3 -p1
%endif
popd

%build
pushd %{packagesrc}
#    -DTOKEN_AUTH_ONLY=ON \
#    -DWITH_PROVIDERS=OFF \
#    -DTOKEN_AUTH_ONLY=OFF requires qt5Widgets, see src/libsync/CMakeLists.txt:107
%cmake .  \
    -DBUILD_SHELL_INTEGRATION=OFF \
    -DBUILD_SHELL_INTEGRATION_DOLPHIN=OFF \
    -DBUILD_SHELL_INTEGRATION_ICONS=OFF \
    -DBUILD_SHELL_INTEGRATION_NAUTILUS=OFF \
    -DNO_SHIBBOLETH=ON \
    -DCMAKE_CXX_FLAGS="${CXXFLAGS} -I/usr/include/qt5keychain" \
    %{nil}

%make_build
popd

%install
pushd %{packagesrc}
%make_install
popd

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%license %{packagesrc}/COPYING
%config %{_sysconfdir}/Nextcloud/*
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*/*.so

%files libs
%{_libdir}/*.so.*
%{_libdir}/*/*.so.*
