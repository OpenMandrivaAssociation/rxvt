Summary:	A color VT102 terminal emulator for the X Window System
Name:		rxvt
Epoch:		3
Version:	2.7.10
Release: 	%mkrel 16
License:	GPL
Group:		Terminals

Source:		ftp://ftp.rxvt.org/pub/rxvt/rxvt-%{version}.tar.bz2
Source1:	rxvt.sh
Source2:	rxvt-zh.menu
Source3:	rxvt-CLE-mini.png
Source4:	rxvt-CLE.png
Source5:	rxvt-CLE-large.png

Patch0:		rxvt-2.7.8-big-buffer.patch
# definition of the default fonts to use depending on language -- pablo 
Patch2:		rxvt-2.7.10-fonts.patch
# IM fix from http://www.giga.it.okayama-u.ac.jp/~ishihara/opensource/:
Patch3:		rxvt-2.7.10-xim-fix.patch 

Buildroot:	%{_tmppath}/%name-%{version}-%{release}-root
URL:		http://www.rxvt.org/
Obsoletes:	crxvt gbrxvt rxvt-CLE
Provides:	crxvt gbrxvt rxvt-CLE
BuildRequires:	XFree86-devel xpm-devel utempter-devel
Conflicts:	drakconf < 9.3-25mdk

%package CJK
Summary:	CJK menus for rxvt
Requires:	%{name} = %{epoch}:%{version}-%{release}
Group:		Terminals

%description
Rxvt is a color VT102 terminal emulator for the X Window System.
Rxvt is intended to be an xterm replacement for users who don't need
the more esoteric features of xterm, like Tektronix 4014 emulation,
session logging and toolkit style configurability.  Since it doesn't
support those features, rxvt uses much less swap space than xterm
uses.  This is a significant advantage on a machine which is serving
a large number of X sessions.

The rxvt package should be installed on any machine which serves a
large number of X sessions, if you'd like to improve that machine's
performance.

This version of rxvt can display Japanese, Chinese (Big5 and GuoBiao) 
and Korean.

%description CJK
This package contains the CJK versions of rxvt.

%prep
%setup -q
%patch0 -p1 -b .bigbuf
%patch2 -p1 -b .fonts
%patch3 -p1 -b .im

%build
# NeXT scrollbar is cool :)
perl -pi -e s/-eten-/-\*-/g src/defaultfont.h

export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -DUTEMPTER"  
%configure --mandir=%_mandir \
	--enable-xpm-background --enable-menubar \
	--enable-utmp --enable-ttygid \
	--enable-transparency --enable-next-scroll --enable-rxvt-scroll --enable-xterm-scroll \
	--enable-xim --enable-languages --enable-smart-resize  \
	--enable-mousewheel --enable-static=yes

# make -j doesn't works... seems some Makefile tasks are done in wrong order
#make -j 2
make
cp src/rxvt src/rxvt.cjk
cp src/rxvt src/rxvt.bin

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
mkdir -p $RPM_BUILD_ROOT/etc/X11/app-defaults
touch src/rxvt
for i in cjk bin;do
   install -m755 src/rxvt.$i $RPM_BUILD_ROOT/usr/bin
done
rm -f $RPM_BUILD_ROOT/usr/bin/rxvt
rm -f $RPM_BUILD_ROOT/usr/bin/rxvt-%{version}

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/usr/bin

# (fg) 20000925 Make the necessary links
( cd $RPM_BUILD_ROOT/usr/bin;
  for i in {gb,c,j,k}rxvt; do
		ln rxvt.sh $i
  done
  ln -s rxvt.sh rxvt
)

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rxvt

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << "EOF" > $RPM_BUILD_ROOT%{_menudir}/rxvt
?package(rxvt):\
  needs="X11"\
  section="Terminals"\
  title="RXvt"\
  longtitle="A version of the rxvt terminal with support for Traditional Chinese, Simplified Chinese, Japanese and Korean."\
  command="/usr/bin/rxvt" \
  icon="rxvt-CLE.png"
EOF

cat << EOF > $RPM_BUILD_ROOT%{_menudir}/rxvt-CJK
?package(rxvt-CJK):\
 needs=x11 section="Terminals" title="CRXvt (Big5)"\
  longtitle="Traditional Chinese rxvt terminal"\
  command="/usr/bin/crxvt -ls" \
  icon="rxvt-CJK.png"

?package(rxvt-CJK):\
  needs=x11 section="Terminals" title="GBRXvt (GB2312)"\
  longtitle="Simplified Chinese rxvt terminal"\
  command="/usr/bin/gbrxvt -ls" \
  icon="rxvt-CJK.png"

?package(rxvt-CJK):\
  needs=x11 section="Terminals" title="JRXvt (JIS)"\
  longtitle="Japanese rxvt terminal"\
  command="/usr/bin/jrxvt -ls" icon="rxvt-CJK.png"

?package(rxvt-CJK):\
  needs=x11 section="Terminals" title="KRXvt (KSC5601)"\
  longtitle="Korean rxvt terminal"\
  command="/usr/bin/krxvt -ls" icon="rxvt-CJK.png"
EOF

# (fg) 20000929 New icons from ln
mkdir -p $RPM_BUILD_ROOT/%{_iconsdir}/{large,mini}
for i in CLE CJK; do
install -m644 %{SOURCE3} $RPM_BUILD_ROOT/%{_miconsdir}/rxvt-$i.png
install -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_iconsdir}/rxvt-$i.png
install -m644 %{SOURCE5} $RPM_BUILD_ROOT/%{_liconsdir}/rxvt-$i.png
done

%post
%{update_menus}
update-alternatives --install /usr/bin/xvt xvt /usr/bin/rxvt 20

%postun
%{clean_menus}

if [ "$1" = "0" ]; then
    update-alternatives --remove xvt /usr/bin/rxvt
fi

%post CJK
%update_menus

%postun CJK
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/*
%_bindir/rclock
%_bindir/rxvt
%_bindir/rxvt.bin
%_bindir/rxvt.cjk
%_bindir/rxvt.sh
%_mandir/man1/*
#%config(missingok,noreplace) /etc/rxvt/rxvt-zh.menu
%{_menudir}/rxvt
%{_iconsdir}/rxvt-CLE.png
%{_liconsdir}/rxvt-CLE.png
%{_miconsdir}/rxvt-CLE.png

%files CJK
%defattr(-,root,root)
%_bindir/crxvt
%_bindir/gbrxvt
%_bindir/jrxvt
%_bindir/krxvt
%{_menudir}/rxvt-CJK
%{_iconsdir}/rxvt-CJK.png
%{_liconsdir}/rxvt-CJK.png
%{_miconsdir}/rxvt-CJK.png


