#!/usr/bin/env python3

# Token kind array

token_kinds = [

	["Invalid",                            "ERROR: Invalid token."],

	# NOTE(zachary): The entries like _LiteralBegin are used
	# so that we can compare a token type with a
	# start and end range to see what the token _does_.

	["EOF",                                "EOF"],
	# Comments. Mostly ignored,
	# unless metaprogramming scripts
	# touch them.
	["Comment",                            "Comment"],
	["Doc_Comment",                        "Documentation Comment"],
	# Simple things like  names, etc.
	["_Literal_Begin",                     ""],
	["Identifier",                         "Identifier"],
	# Literal types
	["Integer",                            "Integer"],
	["Float",                              "Float"],
	["Char",                               "Char"],
	["String",                             "String"],
	["_Literal_End",                       ""],
	# From here on out, the tokens should be
	# literal representations of what they're
	# supposed to be.
	["_Absolute_Capture_Begin",            ""],
	["_Operator_Begin",                    ""],
	# Assignment operators
	["_Assign_Op_Begin",                   ""],
	["Add_Eq",                             "+="],
	["Sub_Eq",                             "-="],
	["Exp_Eq",                             "**="],
	["Mul_Eq",                             "*="],
	["Div_Eq",                             "/="],
	["Mod_Eq",                             "%="],
	["And_Eq",                             "&="],
	["Or_Eq",                              "|="],
	["Xor_Eq",                             "~="],
	["And_Not_Eq",                         "&~="],
	#["ShiftLeftEq",                        "<<="],
	#["ShiftRightEq",                       ">>="],
	["_Assign_Op_End",                     ""],
	# These have to be here so that they're
	# over the Lt and Gt operators
	["Shift_Left",                         "<<"],
	["Shift_Right",                        ">>"],
	# Comparison operators
	["_Comparison_Begin",                  ""],
	["Cmp_And",                            "&&"],
	["Cmp_Or",                             "||"],
	["Cmp_Eq",                             "=="],
	["Cmp_Not_Eq",                         "!="],
	["Cmp_Lt_Eq",                          "<="],
	["Cmp_Gt_Eq",                          ">="],
	["Cmp_Lt",                             "<"],
	["Cmp_Gt",                             ">"],
	["_Comparison_End",                    ""],
	# Other Operators
	["Increment",                          "++"],
	["Decrement",                          "--"],
	["Equals",                             "="],
	["Not",                                "!"],
	["At",                                 "@"],
	["Right_Arrow",                        "->"],
	["Left_Arrow",                         "<-"],
	["And_Not",                            "&~"],
	["And",                                "&"],
	["Or",                                 "|"],
	["Xor",                                "~"],
	["Caret",                              "^"],
	["Question",                           "?"],
	# Arithmetic operators
	["_Arithmetic_Begin",                  ""],
	["Sub",                                "-"],
	["Add",                                "+"],
	["Exp",                                "**"],
	["Mul",                                "*"],
	["Div",                                "/"],
	["Mod",                                "%"],
	["_Arithmetic_End",                    ""],
	# Simple symbols
	["Open_Paren",                         "("],
	["Close_Paren",                        ")"],
	["Open_Bracket",                       "["],
	["Close_Bracket",                      "]"],
	["Open_Brace",                         "{"],
	["Close_Brace",                        "}"],
	["Colon",                              ":"],
	["Semicolon",                          ";"],
	["Open_Ellipsis",                      "..."],
	["Half_Open_Ellipsis",                 ".."],
	["Period",                             "."],
	["Comma",                              ","],
	#["New_Line",                           "\\n"],
	["_Operator_End",                      ""],
	# Keywords

	# A word of caution: Be careful to place
	# any variations on a token at the top.
	# For example, "foreach" comes before "for"

	["_Keyword_Begin",                     ""],
	["Alias",                              "alias"],
	["When",                               "when"],
	["If",                                 "if"],
	["Else",                               "else"],
	["For",                                "for"],
	["In",                                 "in"],
	["Switch",                             "switch"],
	["Match",                              "match"],
	["Case",                               "case"],
	#["Default",                            "default"],
	["Break",                              "break"],
	["Continue",                           "continue"],
	["Fallthrough",                        "fallthrough"],
	["Defer",                              "defer"],
	["Return",                             "return"],
	#["Sig",                                "sig"],
	["Struct",                             "struct"],
	["Class",                              "class"],
	["Union",                              "union"],
	["Enum",                               "enum"],
	["Cast",                               "cast"],
	#["Load",                               "load"],
	["Import",                             "import"],
	["Foreign_Library",                    "foreign_lib"],
	#["Hash_If",                            "#if"],
	#["Hash_Else",                          "#else"],
	#["Hash_Type",                          "#type"],
	#["Hash_Global",                        "#global"],
	#["Hash_Raw",                           "#raw"],
	#["Hash_Foreign",                       "#foreign"],
	["_Keyword_End",                       ""],
	["_Absolute_Capture_End",              ""]
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

source_code = '// This file is automatically generated by gen_token_kinds.py every build.\n\n' + enum + '\n}\n\n' + names + '\n};\n\n'

# Create src/gen

import os
os.makedirs('gen', exist_ok=True)

# Write file src/gen/token_kinds.helm

out_file = open('gen/token_kinds.helm', 'w')
out_file.write(source_code)
out_file.close()



# Generate comparison functions

source_code = '// This file is automatically generated by gen_token_kinds.py every build.\n\nusing import "token_kinds";\nusing import "../types.helm"\n\n'

for zone in token_zones:
	source_code += 'is_token_' + zone[1] + '_a :: inline(t: Token_Kind) -> bool do return t > Token_Kind._' + zone[0] + 'Begin && t < Token_Kind._' + zone[0] + 'End;\n'
	source_code += 'is_token_' + zone[1] + '_b :: inline(t: Token) -> bool do return is_token_' + zone[1] + '(t.kind);\n'
	source_code += 'is_token_' + zone[1] + ' :: proc[is_token_' + zone[1] + '_a, is_token_' + zone[1] + '_b];\n\n'

source_code += 'tokens_equal :: (a, b: Token) -> bool do return (a.col == b.col && a.line == b.line) || a.text == b.text;\n';

# Write file src/gen/token_comp.helm

out_file = open('gen/token_comp.helm', 'w')
out_file.write(source_code)
out_file.close()