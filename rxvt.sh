#!/bin/sh
#
# by Chih-Wei Huang
# modified by Pablo Saratxaga <pablo@mandrakesoft.com>
# modified by Geoffrey Lee <snailtalk@mandrakesoft.com>
# modified by Andrew Lee <andrew@linux.org.tw>
#
#              Updated   22-24 July - 24 August 1999
#			 23 January 2001
#        Last modified   14 September 2001
# 2002-08-07 Pablo Saratxaga <pablo@mandrakesoft.com>
#	* added charset autodetection for non-CJK languages
# 2004-01-08 Pablo Saratxaga <pablo@mandrakesoft.com>
#	* fonts are not defined if an explicit X11 ressource defines them
#

#PATH="/bin:/usr/bin:/usr/X11R6/bin:/usr/local/bin"
SCRIPTNAME=`basename $0`

RXVT=/usr/bin/rxvt.cjk

if [ "$SCRIPTNAME" = "rxvt" -o "$SCRIPTNAME" = "rxvt.sh" -o "$SCRIPTNAME" = "xvt" ]; then
    if [ ! -z $LANGUAGE ]; then
        locale=`echo $LANGUAGE | cut -d: -f1`
    elif [ ! -z $LC_ALL ]; then
        locale=$LC_ALL
    elif [ ! -z $LC_CTYPE ]; then
        locale=$LC_CTYPE
    elif [ ! -z $LANG ]; then
        locale=$LANG
    fi

    case $locale in
        zh_TW*|zh_HK*)
        SCRIPTNAME=crxvt
        ;;

        zh_CN*)
        SCRIPTNAME=gbrxvt
	;;

	ja*)
	SCRIPTNAME=jrxvt
	;;

	ko*)
	SCRIPTNAME=krxvt
	;;

      # unknown locale, ignore it
    *)
	SCRIPTNAME=rxvt
	MENU=""
        ;;
    esac

    unset locale
fi

case $SCRIPTNAME in
    crxvt)
    LANG=zh_TW.Big5
    LANGUAGE="zh_TW.Big5:zh_TW:zh"
    ENC=big5
    XA_FACE=ming
    XA_FAMILY=default
    XIM=SCIM
  #  MENU="/etc/rxvt/rxvt-zh.menu;big5"
    FNFONT="8x16"
  #  FMFONT="-default-ming-medium-r-normal--16-*-*-*-c-160-big5-0"
    _TITLE="Chinese"
    ;;

    gbrxvt)
    LANG=zh_CN.GB2312
    LANGUAGE=zh_CN.GB2312:zh_CN:zh
    ENC=gb
    XA_FACE=ming
    XA_FAMILY=default
    XIM=SCIM
    FNFONT="8x16"
   # MENU="/etc/rxvt/rxvt-zh.menu;gb"
   # FMFONT="-default-ming-medium-r-normal--16-*-*-*-c-160-gb2312.1980-0"
    _TITLE="Chinese"
    ;;

    jrxvt)
    LANG=ja_JP
    LANGUAGE="ja_JP.EUC-JP:ja_JP.ujis:ja_JP:ja"
    FNFONT="7x14"
    ENC=eucj
    XIM=SCIM
    #MENU="/usr/share/rxvt/rxvt-ja;eucj"
    _TITLE="Japanese"
    ;;

    krxvt)
    LANG=ko_KR
    LANGUAGE="ko_KR.EUC-KR:ko_KR:ko"
    ENC=kr
    FNFONT="8x16"
    XIM=SCIM
    #MENU="/usr/share/rxvt/rxvt-ko;kr"
    _TITLE="Korean"
    ;;

    # Locale other than jp / zh / ko, give ENC == noenc
    rxvt | xvt)
    RXVT="/usr/bin/rxvt.bin"
    unset $ENC
    unset $XIM
    CHARSET=`locale charmap`
    case "$CHARSET" in
	ANSI_X3.4-1968|ISO-8859-1) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-iso8859-1" ;;
	ISO-8859-2) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-iso8859-2" ;;
	# there is no bitmap font for iso-8859-3, which is deprecated in favor
	# of utf-8, so we use the Adobe Courier Type1.
	ISO-8859-3) FNFONT="-*-courier-medium-r-normal-*-*-140-75-75-*-*-iso8859-3" ;;
	ISO-8859-5) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-iso8859-5" ;;
	ISO-8859-7) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-iso8859-7" ;;
	ISO-8859-9) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-iso8859-9" ;;
	ISO-8859-13) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-iso8859-13" ;;
	ISO-8859-15) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-iso8859-15" ;;
	# we don't provide a default monospaced font for cp1251 encoding...
	# it is better to use xterm for it 
	# this font is very ugly, but at least it works
	CP1251) FNFONT="-*-*-medium-r-normal-*-*-100-75-75-*-*-microsoft-cp1251" ;;
	KOI8-R) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-koi8-r" ;;
	KOI8-U) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-koi8-u" ;;
	# other encodings don't work properly anyway with rxvt; xterm should be
	# used instead.
	*) FNFONT="-*-fixed-medium-r-normal-*-*-140-75-75-*-*-iso8859-15" ;
	echo ""
	echo "=============================================="
	echo "WARNING!!"
	echo ""
	echo "rxvt is unable to display in $CHARSET encoding"
	echo "you should use xterm instead"
	echo "=============================================="
	;;
    esac
    ;;
	
esac


export LANG LANGUAGE

FGCOLOR=lightgray
BGCOLOR=black
TITLE="$_TITLE RXVT ($LANG)"

ARGS=""
RESNAME="rxvt"

while [ -n "$1" ]; do
    case $1 in
        -km) shift
        ENC=$1
        ;;

        -im) shift
        XIM=$1
        ;;

        -fg) shift
        _FGCOLOR=$1
        ;;

        -bg) shift
        _BGCOLOR=$1
        ;;

        -T|-title) shift
        TITLE=$1
        ;;

        -menu) shift
        MENU="$1"
        ;;

        -nomenu)
        MENU=""
        ;;

        -fn) shift
        _FNFONT="$1"
        ;;

        -fm) shift
        _FMFONT="$1"
        ;;

        -name) shift
        RESNAME="$1"
        ;;

        *)
        ARGS="$ARGS $1"
        ;;
    esac
    shift
done

# if a ressource is defined for one of the values we define
# here, then we should retain the ressource value;
# unless it is defined in command line
RESLIST=`xrdb -query`

if [ -n "$_BGCOLOR" ]; then
	BGCOLOR=$_BGCOLOR
else
	if echo "$RESLIST" | grep -iq "\<${RESNAME}\>[.*].*\<background\>"
	then
		unset BGCOLOR
	fi
fi

if [ -n "$_FGCOLOR" ]; then
	FGCOLOR=$_FGCOLOR
else
	if echo "$RESLIST" | grep -iq "\<${RESNAME}\>[.*].*\<foreground\>"
	then
		unset FGCOLOR
	fi
fi

if [ -n "$_FNFONT" ]; then
	FNFONT=$_FNFONT
else
	if echo "$RESLIST" | grep -iq "\<${RESNAME}\>[.*].*\<font\>"
	then
		unset FNFONT
	fi
fi

if [ -n "$_FMFONT" ]; then
	FMFONT=$_FMFONT
else
	if echo "$RESLIST" | grep -iq "\<${RESNAME}\>[.*].*\<mfont\>"
	then
		unset FMFONT
	fi
fi

[ -n "$BGCOLOR" ] && ARGS="-bg $BGCOLOR $ARGS"
[ -n "$FGCOLOR" ] && ARGS="-fg $FGCOLOR $ARGS"
[ -n "$ENC" ] && ARGS="-km $ENC $ARGS"
if [ -n "$XIM" -a -n "$ENC" ]; then
    ARGS="-im $XIM $ARGS" 
    export XMODIFIERS="@im=$XIM"
fi

# Alas! Dirty hack for font name containing spaces
# Is there any simpler solution??
if [ -n "$FNFONT" -a -n "$FMFONT" ]; then
    exec $RXVT -T "$TITLE" -menu "$MENU" -fn "$FNFONT" -fm "$FMFONT" $ARGS
elif [ -n "$FNFONT" ]; then
    exec $RXVT -T "$TITLE" -menu "$MENU" -fn "$FNFONT" $ARGS
elif [ -n "$FMFONT" ]; then
    exec $RXVT -T "$TITLE" -menu "$MENU" -fm "$FMFONT" $ARGS
else
    exec $RXVT -T "$TITLE" -menu "$MENU" $ARGS
fi

