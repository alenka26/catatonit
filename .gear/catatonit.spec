Name: catatonit
Version: 0.1.5
Release: alt1
Summary: A signal-forwarding process manager for containers
License: GPLv3+
Group: System/Configuration/Boot and Init
URL: https://github.com/openSUSE/catatonit
Source0: %name-%version.tar
#Patch0: %name-%version-alt.patch
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: file
BuildRequires: gcc
BuildRequires: git
BuildRequires: glibc-devel-static
BuildRequires: libtool

%description
Catatonit is a /sbin/init program for use within containers. It
forwards (almost) all signals to the spawned child, tears down
the container when the spawned child exits, and otherwise
cleans up other exited processes (zombies).

This is a reimplementation of other container init programs (such as
"tini" or "dumb-init"), but uses modern Linux facilities (such as
signalfd(2)) and has no additional features.

%prep
%setup -q
#patch -p1

%build
autoreconf -fi
%configure
%make_build

# Make sure we *always* build a static binary. Otherwise we'll break containers
# that don't have the necessary shared libs.
file ./%name | grep 'statically linked'
if [ $? != 0 ]; then
   echo "ERROR: %name binary must be statically linked!"
   exit 1
fi

%install
install -dp %buildroot%_libexecdir/%name
install -p %name %buildroot%_libexecdir/%name
install -dp %buildroot%_libexecdir/podman
ln -s %_libexecdir/%name/%name %buildroot%_libexecdir/podman/%name

%files
%doc README.md COPYING
%dir %_libexecdir/%name
%_libexecdir/%name/%name
%dir %_libexecdir/podman
%_libexecdir/podman/%name

%changelog
* Wed Aug 05 2020 Alenka Glukhovskaya <alenka@altlinux.org> 0.1.5-alt1
- Initial build for Sisyphus