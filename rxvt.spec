Summary:	A color VT102 terminal emulator for the X Window System
Name:		rxvt
Epoch:		3
Version:	2.7.10
Release: 	%mkrel 19
License:	GPLv2
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

# from gentoo
Patch4:		rxvt-2.7.10-asneeded.patch
Patch5:		rxvt-2.7.10-azz4.diff
Patch6:		rxvt-2.7.10-line-scroll.patch
Patch7:		rxvt-2.7.10-rk.patch
Patch8:		rxvt-2.7.10-CVE-2008-1142-DISPLAY.patch

Buildroot:	%{_tmppath}/%name-%{version}-%{release}-root
URL:		http://www.rxvt.org/
Obsoletes:	crxvt gbrxvt rxvt-CLE
Provides:	crxvt gbrxvt rxvt-CLE
BuildRequires:	X11-devel xpm-devel utempter-devel lesstif-devel
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

%patch4 -p1 -b .asneeded
%patch5 -p1 -b .azz4
%patch6 -p0 -b .line-scroll
%patch7 -p1 -b .rk
%patch8 -p1 -b .CVE-2008-1142

%build
# NeXT scrollbar is cool :)
perl -pi -e s/-eten-/-\*-/g src/defaultfont.h

export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -DUTEMPTER"  
%configure2_5x --mandir=%_mandir \
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

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-rxvt.desktop
[Desktop Entry]
Type=Application
Categories=X-MandrivaLinux-System-Terminals;TerminalEmulator;
Name=RXvt
Comment=A version of the rxvt terminal with support for Traditional Chinese, Simplified Chinese, Japanese and Korean.
Exec=/usr/bin/rxvt
Icon=rxvt-CLE
EOF

cat << EOF > %buildroot%{_datadir}/applications/mandriva-rxvt-C_tw.desktop
[Desktop Entry]
Type=Application
Categories=X-MandrivaLinux-System-Terminals;TerminalEmulator;
Name=CRXvt (Big5)  
Comment=Traditional Chinese rxvt terminal  
Exec=/usr/bin/crxvt -ls  
Icon=rxvt-CJK
EOF

cat << EOF > %buildroot%{_datadir}/applications/mandriva-rxvt-C_ch.desktop
[Desktop Entry]
Type=Application
Categories=X-MandrivaLinux-System-Terminals;TerminalEmulator;
Name=GBRXvt (GB2312)  
Comment=Simplified Chinese rxvt terminal  
Exec=/usr/bin/gbrxvt -ls  
Icon=rxvt-CJK
EOF

cat << EOF > %buildroot%{_datadir}/applications/mandriva-rxvt-J.desktop
[Desktop Entry]
Type=Application
Categories=X-MandrivaLinux-System-Terminals;TerminalEmulator;
Name=JRXvt (JIS)  
Comment=Japanese rxvt terminal  
Exec=/usr/bin/jrxvt -ls
Icon=rxvt-CJK
EOF

cat << EOF > %buildroot%{_datadir}/applications/mandriva-rxvt-K.desktop
[Desktop Entry]
Type=Application
Categories=X-MandrivaLinux-System-Terminals;TerminalEmulator;
Name=KRXvt (KSC5601)  
Comment=Korean rxvt terminal  
Exec=/usr/bin/krxvt -ls
Icon=rxvt-CJK
EOF

# (fg) 20000929 New icons from ln
mkdir -p $RPM_BUILD_ROOT/%{_iconsdir}/{large,mini}
for i in CLE CJK; do
install -m644 %{SOURCE3} $RPM_BUILD_ROOT/%{_miconsdir}/rxvt-$i.png

install -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_iconsdir}/rxvt-$i.png
install -m644 %{SOURCE5} $RPM_BUILD_ROOT/%{_liconsdir}/rxvt-$i.png
done

chmod -x doc/menu/*

%post
%if %mdkversion < 200900
%{update_menus}
%endif
update-alternatives --install /usr/bin/xvt xvt /usr/bin/rxvt 20

%postun
%if %mdkversion < 200900
%{clean_menus}
%endif

if [ "$1" = "0" ]; then
	update-alternatives --remove xvt /usr/bin/rxvt
fi

%if %mdkversion < 200900
%post CJK
%update_menus
%endif

%if %mdkversion < 200900
%postun CJK
%clean_menus
%endif

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
%{_datadir}/applications/mandriva-rxvt.desktop
%{_iconsdir}/rxvt-CLE.png
%{_liconsdir}/rxvt-CLE.png
%{_miconsdir}/rxvt-CLE.png

%files CJK
%defattr(-,root,root)
%_bindir/crxvt
%_bindir/gbrxvt
%_bindir/jrxvt
%_bindir/krxvt
%{_datadir}/applications/mandriva-rxvt-*.desktop
%{_iconsdir}/rxvt-CJK.png
%{_liconsdir}/rxvt-CJK.png
%{_miconsdir}/rxvt-CJK.png


