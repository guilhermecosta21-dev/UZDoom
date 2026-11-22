cmake_minimum_required( VERSION 3.16 )

if( NOT CMAKE_CROSSCOMPILING )

include( CheckIncludeFile )

# re2c is written in C++11
set( CMAKE_CXX_STANDARD 11 )
set( CMAKE_CXX_STANDARD_REQUIRED ON )

if( MSVC )
	# Runtime type information is required and don't complain about uint32_t to bool conversions
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /GR /wd4800" )
	# Same as re2c's own build: ignore GCC/Clang pragmas and the CRT "unsafe function" deprecations
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc /wd4068" )
	add_definitions( -D_CRT_SECURE_NO_WARNINGS )
endif()

set( PACKAGE_VERSION 4.6 )

CHECK_INCLUDE_FILE( sys/types.h HAVE_SYS_TYPES_H )
CHECK_INCLUDE_FILE( sys/stat.h HAVE_SYS_STAT_H )
CHECK_INCLUDE_FILE( fcntl.h HAVE_FCNTL_H )
CHECK_INCLUDE_FILE( unistd.h HAVE_UNISTD_H )
CHECK_INCLUDE_FILE( io.h HAVE_IO_H )

configure_file( ${CMAKE_CURRENT_SOURCE_DIR}/config.h.in ${CMAKE_CURRENT_BINARY_DIR}/config.h )
# bootstrap/ holds the pre-generated lexers, parsers, syntax files and help text,
# so neither bison nor python (nor an existing re2c) is needed to build re2c.
include_directories( ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/bootstrap )
add_definitions( "-DRE2C_STDLIB_DIR=\"${CMAKE_CURRENT_SOURCE_DIR}/include/\"" )

file( GLOB SRC_HDR
	src/*.h
	src/adfa/*.h
	src/cfg/*.h
	src/codegen/*.h
	src/debug/*.h
	src/dfa/*.h
	src/encoding/*.h
	src/msg/*.h
	src/nfa/*.h
	src/options/*.h
	src/parse/*.h
	src/regexp/*.h
	src/skeleton/*.h
	src/util/*.h )

add_executable( re2c
	${SRC_HDR}
	src/codegen/helpers.cc
	src/codegen/output.cc
	src/codegen/pass1_analyze.cc
	src/codegen/pass2_generate.cc
	src/codegen/pass3_fixup.cc
	src/codegen/pass4_render.cc
	src/options/opt.cc
	src/options/symtab.cc
	src/nfa/re_to_nfa.cc
	src/adfa/adfa.cc
	src/debug/dump_adfa.cc
	src/debug/dump_cfg.cc
	src/debug/dump_dfa.cc
	src/debug/dump_dfa_tree.cc
	src/debug/dump_interf.cc
	src/debug/dump_nfa.cc
	src/cfg/cfg.cc
	src/cfg/compact.cc
	src/cfg/dce.cc
	src/cfg/freeze.cc
	src/cfg/interfere.cc
	src/cfg/liveanal.cc
	src/cfg/normalize.cc
	src/cfg/optimize.cc
	src/cfg/rename.cc
	src/cfg/varalloc.cc
	src/dfa/closure.cc
	src/dfa/dead_rules.cc
	src/dfa/determinization.cc
	src/dfa/fallback_tags.cc
	src/dfa/fillpoints.cc
	src/dfa/find_state.cc
	src/dfa/minimization.cc
	src/dfa/tagver_table.cc
	src/dfa/tcmd.cc
	src/encoding/ebcdic.cc
	src/encoding/enc.cc
	src/encoding/range_suffix.cc
	src/encoding/unicode_casemap.cc
	src/encoding/utf8.cc
	src/encoding/utf16.cc
	src/msg/msg.cc
	src/msg/warn.cc
	src/regexp/ast_to_re.cc
	src/regexp/default_tags.cc
	src/regexp/fixed_tags.cc
	src/regexp/nullable.cc
	src/regexp/regexp.cc
	src/regexp/split_charset.cc
	src/skeleton/control_flow.cc
	src/skeleton/generate_code.cc
	src/skeleton/generate_data.cc
	src/skeleton/maxpath.cc
	src/skeleton/skeleton.cc
	src/parse/ast.cc
	src/parse/input.cc
	src/util/file_utils.cc
	src/util/string_utils.cc
	src/util/range.cc
	src/main.cc
	bootstrap/src/msg/help_re2c.cc
	bootstrap/src/msg/ver_to_vernum.cc
	bootstrap/src/options/parse_opts.cc
	bootstrap/src/parse/conf_lexer.cc
	bootstrap/src/parse/conf_parser.cc
	bootstrap/src/parse/lexer.cc
	bootstrap/src/parse/parser.cc )

set( CROSS_EXPORTS ${CROSS_EXPORTS} re2c PARENT_SCOPE )

endif()
