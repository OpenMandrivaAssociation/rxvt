Summary:	A color VT102 terminal emulator for the X Window System
Name:		rxvt
Epoch:		3
Version:	2.7.10
Release: 	%mkrel 25
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
URL:		http://rxvt.sourceforge.net/
Obsoletes:	crxvt <= 2.7.10, gbrxvt <= 2.7.10
Obsoletes:	rxvt-CLE <= 2.7.10
Provides:	crxvt = %{version}-%{release}, gbrxvt = %{version}-%{release}
Provides:	rxvt-CLE = %{version}-%{release}
BuildRequires:	xpm-devel utempter-devel lesstif-devel
# X11 locales are required to build IM support
BuildRequires:	libx11-common
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




%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2.7.10-24mdv2011.0
+ Revision: 669467
- mass rebuild

* Wed Dec 01 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 3:2.7.10-23mdv2011.0
+ Revision: 604512
- Update URL
- Remove useless X11-devel BR

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2.7.10-22mdv2010.1
+ Revision: 523940
- rebuilt for 2010.1

* Fri Oct 09 2009 Olivier Blin <oblin@mandriva.com> 3:2.7.10-21mdv2010.0
+ Revision: 456350
- buildrequire libx11-common to fix build with xim (#54432)

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 3:2.7.10-20mdv2010.0
+ Revision: 426970
- rebuild

  + Rémy Clouard <shikamaru@mandriva.org>
    - fix Obsoletes
    - fix provides/obsoletes
    - fix configure (use 2_5x)
    - fix license
    - fix desktop file
    - clean spec

* Mon Nov 10 2008 Oden Eriksson <oeriksson@mandriva.com> 3:2.7.10-18mdv2009.1
+ Revision: 301745
- rebuild

* Fri Aug 01 2008 Oden Eriksson <oeriksson@mandriva.com> 3:2.7.10-17mdv2009.0
+ Revision: 260002
- fix deps
- rebuild
- sync patches with gentoo

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 3:2.7.10-16mdv2009.0
+ Revision: 218436
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Thierry Vignaud <tv@mandriva.org> 3:2.7.10-16mdv2008.1
+ Revision: 134673
- auto-convert XDG menu entry
- kill re-definition of %%buildroot on Pixel's request
- buildrequires X11-devel instead of XFree86-devel


* Thu Dec 21 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.7.10-16mdv2007.0
+ Revision: 101041
- fix startup now that binary has moved

* Wed Dec 20 2006 Thierry Vignaud <tvignaud@mandriva.com> 3:2.7.10-15mdv2007.1
+ Revision: 100845
- Import rxvt

* Wed Dec 20 2006 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7.10-15mdv2007.1
- do not install in /usr/X11R6 (#24759)
- simplify a little the spec file (more to do)
- use %%{1}mdv2007.1

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.7.10-14mdk
- Rebuild

* Mon Jan 31 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7.10-13mdk
- patch 3: fix IM support (thus enabling SCIM support in rxvt)

* Fri Sep 24 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7.10-12mdk
- source 1: use SCIM for CJK by default (UTUMI Hirosi)

* Sat Aug 21 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7.10-11mdk
- enable various kinds of scrollbars (#10534)
- fix typo in menu entry

* Thu Jun 10 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.7.10-10mdk
- Remove the --enable-xgetdefault configure flag

* Sun Feb 08 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7.10-9mdk
- fix CJK description

* Mon Jan 19 2004 Abel Cheung <deaddog@deaddog.org> 2.7.10-8mdk
- Requires with epoch

* Sun Jan 18 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7.10-7mdk
- readd back rxvt menu entry now that mcc does not force rxvt installation
  anymore

* Thu Jan 15 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7.10-6mdk
- update source 1 : fix script (#6867, Olivier Blin)

* Fri Jan 09 2004 Pablo Saratxaga <pablo@mandrakesoft.com> 2.7.10-5mdk
- Changed wrapper script to avoid overwritten values defined trough
  X11 ressources (bug #180)

