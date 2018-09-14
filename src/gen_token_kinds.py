#!/usr/bin/env python3

# Token kind array

token_kinds = [

	# NOTE(zachary): The entries like _LiteralBegin are used
	# so that we can compare a token type with a
	# start and end range to see what the token _does_.

	["EOF",                                "EOF"],
	# Comments. Mostly ignored,
	# unless metaprogramming scripts
	# touch them.
	["Comment",                            "Comment"],
	# Simple things like  names, etc.
	["_LiteralBegin",                      ""],
	["Identifier",                         "Identifier"],
	# Literal types
	["Integer",                            "Integer"],
	["Float",                              "Float"],
	["Char",                               "Char"],
	["String",                             "String"],
	["_LiteralEnd",                        ""],
	# From here on out, the tokens should be
	# literal representations of what they're
	# supposed to be.
	["_AbsoluteCaptureBegin",              ""],
	["_OperatorBegin",                     ""],
	# Assignment operators
	["_AssignOpBegin",                     ""],
	["AddEq",                              "+="],
	["SubEq",                              "-="],
	["MulEq",                              "*="],
	["DivEq",                              "/="],
	["ModEq",                              "%="],
	["AndEq",                              "&="],
	["OrEq",                               "|="],
	["XorEq",                              "~="],
	["AndNotEq",                           "&~="],
	["ShiftLeftEq",                        "<<="],
	["ShiftRightEq",                       ">>="],
	["_AssignOpEnd",                       ""],
	# These have to be here so that they're
	# over the Lt and Gt operators
	["ShiftLeft",                          "<<"],
	["ShiftRight",                         ">>"],
	# Comparison operators
	["_ComparisonBegin",                     ""],
	["CmpAnd",                             "&&"],
	["CmpOr",                              "||"],
	["CmpEq",                              "=="],
	["CmpNotEq",                           "!="],
	["CmpLtEq",                            "<="],
	["CmpLt",                              "<"],
	["CmpGtEq",                            ">="],
	["CmpGt",                              ">"],
	["_ComparisonEnd",                     ""],
	# Other Operators
	["Increment",                          "++"],
	["Decrement",                          "--"],
	["Equals",                             "="],
	["Not",                                "!"],
	["At",                                 "@"],
	["Arrow",                              "->"],
	["AndNot",                             "&~"],
	["And",                                "&"],
	["Or",                                 "|"],
	["Xor",                                "~"],
	["Caret",                              "^"],
	["Question",                           "?"],
	# Arithmetic operators
	["_ArithmeticBegin",                   ""],
	["Sub",                                "-"],
	["Add",                                "+"],
	["Mul",                                "*"],
	["Div",                                "/"],
	["Mod",                                "%"],
	["_ArithmeticEnd",                     ""],
	# Simple symbols
	["OpenParen",                          "("],
	["CloseParen",                         ")"],
	["OpenBracket",                        "["],
	["CloseBracket",                       "]"],
	["OpenBrace",                          "{"],
	["CloseBrace",                         "}"],
	["Colon",                              ":"],
	["Semicolon",                          ";"],
	["Ellipsis",                           "..."],
	["Period",                             "."],
	["Comma",                              ","],
	["NewLine",                            "\\n"],
	["_OperatorEnd",                       ""],
	# Keywords

	# A word of caution: Be careful to place
	# any variations on a token at the top.
	# For example, "foreach" comes before "for"

	["_KeywordBegin",                      ""],
	["Alias",                              "alias"],
	["When",                               "when"],
	["If",                                 "if"],
	["Else",                               "else"],
	["For",                                "for"],
	["In",                                 "in"],
	["Switch",                             "switch"],
	["Case",                               "case"],
	["Default",                            "default"],
	["Break",                              "break"],
	["Continue",                           "continue"],
	["Fallthrough",                        "fallthrough"],
	["Defer",                              "defer"],
	["Return",                             "return"],
	["Sig",                                "sig"],
	["Struct",                             "struct"],
	["Class",                              "class"],
	["Union",                              "union"],
	["Enum",                               "enum"],
	["Cast",                               "cast"],
	["Load",                               "load"],
	["Import",                             "import"],
	["HashIf",                             "#if"],
	["HashElse",                           "#else"],
	["HashType",                           "#type"],
	["HashGlobal",                         "#global"],
	["HashRaw",                            "#raw"],
	["HashForeign",                        "#foreign"],
	["_KeywordEnd",                        ""],
	["_AbsoluteCaptureEnd",                ""],
	["Count",                              ""]
]

# The different "zones" that demarcate different forms of tokens.

token_zones = [
	["Literal",         "literal"],
	["AbsoluteCapture", "absolute_capture"],
	["Operator",        "operator"],
	["AssignOp",        "assign"],
	["Comparison",      "comparison"],
	["Arithmetic",      "arithmetic"],
	["Keyword",         "keyword"]
]

######################
##                  ##
##  Generate code.  ##
##                  ##
######################


# Generate token list

enum = 'Token_Kind :: enum {'
names = 'token_names := [' + str(len(token_kinds)) + ']string {'

for pair in token_kinds:
	enum += '\n\t' + pair[0] + ','
	names += '\n\t\"' + pair[1] + '\",'

source_code = '// This file is automatically generated by token_kinds.py every build.\n\n' + enum + '\n}\n\n' + names + '\n};\n\n'

# Create src/gen

import os
os.makedirs('gen', exist_ok=True)

# Write file src/gen/token_kinds.helm

out_file = open('gen/token_kinds.helm', 'w')
out_file.write(source_code)
out_file.close()



# Generate comparison functions

source_code = '// This file is automatically generated by token_kinds.py every build.\n\nusing import "token_kinds";\nusing import "../types.helm"\n\n'

for zone in token_zones:
	source_code += 'is_token_' + zone[1] + '_a :: inline(t: Token_Kind) -> bool do return t > Token_Kind._' + zone[0] + 'Begin && t < Token_Kind._' + zone[0] + 'End;\n'
	source_code += 'is_token_' + zone[1] + '_b :: inline(t: Token) -> bool do return is_token_' + zone[1] + '(t.kind);\n'
	source_code += 'is_token_' + zone[1] + ' :: proc[is_token_' + zone[1] + '_a, is_token_' + zone[1] + '_b];\n\n'

# Write file src/gen/token_comp.helm

out_file = open('gen/token_comp.helm', 'w')
out_file.write(source_code)
out_file.close()