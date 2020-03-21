#!/bin/sh
# Copyright (c) 2020 The Zcash developers

rm -f src/Makefile
rm -f src/Makefile.in
rm -f doc/man/Makefile
rm -f doc/man/Makefile.in

rm -f src/config/stamp-h1
rm -f src/config/bitcoin-config.h
rm -f src/obj/build.h
rm -f src/leveldb/build_config.mk
rm -f src/test/buildenv.py
rm -f src/test/data/alertTests.raw.h

rm -f qa/pull-tester/run-bitcoind-for-test.sh
rm -f qa/pull-tester/tests-config.sh

rm -rf src/test/data/*.json.h

rm -f src/bench/bench_bitcoin
rm -f src/zcash-cli
rm -f src/zcashd
rm -f src/zcash-gtest
rm -f src/zcash-tx
rm -f src/test/test_bitcoin

find src -type f -and \( -name '*.Po' -or -name '*.Plo' -or -name '*.o' -or -name '*.a' -or -name '*.la' -or -name '*.lo' -or -name '*.lai' -or -name '*.pc' -or -name '.dirstamp' \) -delete
find . -depth -path '*/.deps/*' -or \( -type d -and -name '.deps' \) -delete

cleanme()
{
    rm -rf "$1/autom4te.cache"
    rm -f "$1/build-aux/compile"
    rm -f "$1/build-aux/config.guess"
    rm -f "$1/build-aux/config.sub"
    rm -f "$1/build-aux/depcomp"
    rm -f "$1/build-aux/install-sh"
    rm -f "$1/build-aux/ltmain.sh"
    rm -f "$1/build-aux/missing"
    rm -f "$1/build-aux/test-driver"
    rm -f "$1/build-aux/m4/libtool.m4"
    rm -f "$1/build-aux/m4/lt~obsolete.m4"
    rm -f "$1/build-aux/m4/ltoptions.m4"
    rm -f "$1/build-aux/m4/ltsugar.m4"
    rm -f "$1/build-aux/m4/ltversion.m4"
    rm -f "$1/aclocal.m4"
    rm -f "$1/config.log"
    rm -f "$1/config.status"
    rm -f "$1/gen_context"
    rm -f "$1/configure"
    rm -f "$1/libtool"
    rm -f "$1/Makefile"
    rm -f "$1/Makefile.in"
    rm -f "$1/$2"
    rm -f "$1/$2~"
}

cleanme . src/config/bitcoin-config.h.in

cleanme src/secp256k1 src/libsecp256k1-config.h.in
rm -f src/secp256k1/src/ecmult_static_context.h
rm -f src/secp256k1/src/libsecp256k1-config.h
rm -f src/secp256k1/src/stamp-h1

cleanme src/univalue univalue-config.h.in
rm -f src/univalue/univalue-config.h
rm -f src/univalue/stamp-h1
