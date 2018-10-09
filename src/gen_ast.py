#!/usr/bin/env python3

imports = """
using import "../types"
"""

typedefs = """
enum Value_Decl_Mode {
	Constant, Variable, Immutable
}
"""

# Name, lines of struct definition, way to get token from the node
ast_nodes = [
	["Invalid"],
	["Identifier",       ["token: Token"],                                      "token"],            # my_var_name
	["Basic_Literal",    ["token: Token"],                                      "token"],            # 15
	["Proc_Literal",     ["type, body: ^Ast_Node", "inline: bool"],             "get_token(type)"],  # (a: int) -> bool {return a > 5}
# ??
# 	["Identifier",       ["token: Token"],                                      "token"],            # 
	["_Expr_Begin"],
	["Run_Expr",         ["token: Token", "expr: ^Ast_Node"],                   "token"],           # #run my_ctfe_proc();
	["Unary_Expr",       ["op: Token", "expr: ^Ast_Node"],                      "op"],              # !success
	["Binary_Expr",      ["op: Token", "left, right: ^Ast_Node"],               "op"],              # a + b
	["Paren_Expr",       ["open, close: Token", "expr: ^Ast_Node"],             "open"],            # ( a + ... + 5 * proc_call() )
	["Selector_Expr",    ["token: Token", "expr, selector: ^Ast_Node"],         "token"],           # struct_name.member
	["Index_Expr",       ["open, close: Token", "expr, selector: ^Ast_Node"],   "open"],            # my_arr[5 + 2]
	["Slice_Expr",       ["open, close: Token", "expr, start, end: ^Ast_Node"], "open"],            # my_arr[5 .. 9]  (5 - 8 inclusive)
	["Call_Expr",        ["open, close: Token", "proc: ^Ast_Node",
	                      "args: [dynamic]Ast_Node"],                           "open"],            # my_proc(a, b, 50, (a: int) -> bool {log(a);})
	["Ternary_Expr",     ["cond, a, b: ^Ast_Node"],                             "get_token(cond)"], # success ? contents : default_value
	["Cast_Expr",        ["token: Token", "type, expr: ^Ast_Node"],             "token"],           # cast(f32) my_int
	["Tpl_Inst_Expr",    ["bang: Token", "name: ^Ast_Node",
	                      "args: [dynamic]Ast_Node"]],                          "bang"],            # my_proc!string, thing!(My_Struct, 2)
	["_Expr_End"],
	["_Stmt_Begin"],
	["Assign_Stmt",      ["op: Token", "lhs, rhs: [dynamic]Ast_Node"],          "op"],              # int_a, int_b += 10, 50;
	["Block_Stmt",       ["open, close: Token", "stmts: [dynamic]Ast_Node"],    "open"],            # {i := 5; writeln(i + 5);}
	["If_Stmt",          ["token: Token", "decl, cond, body, else: ^Ast_Node"], "token"],           # if a:=5; a < 10 {} else if ...
	["When_Stmt",        ["token: Token", "cond, body, else: ^Ast_Node"],       "token"],           # when os.OS_WIN32 {...} else {...}
	["Return_Stmt",      ["token: Token", "results: [dynamic]Ast_Node"],        "token"],           # return a, b;
	["For_Stmt",         ["token: Token",
	                      "label, init, cond, post, body: ^Ast_Node"],          "token"],           # for i := 5; i < 10; i += 1 {}
	["For_In_Stmt",      ["for_token, in_token: Token",
	                      "label, decl, range: ^Ast_Node"],                     "for_token"],       # for i in 5..10 {}
	["Switch_Stmt",      ["token: Token", "init, cond: ^Ast_Node"],             "token"],           # switch error_kind := get_error(); error_kind {}
	["Case_Clause",      ["token: Token", "conds: [dynamic]Ast_Node",
	                      "stmt: ^Ast_Node"],                                   "token"],           # case 10, 15: {io.writeln("got 10 or 15"); exit(1);}
	["Match_Stmt",       ["token: Token", "type, name, stmt: ^Ast_Node"],       "token"],           # match err {TypeError -> te: io.writeln(te);}
	["Defer_Stmt",       ["token: Token", "stmt: ^Ast_Node"],                   "token"],           # defer free(c_str);
	["_Stmt_End"],
	["_Decl_Begin"],
	#["Label_Decl",       ["token: Token", "name: ^Ast_Node"],                   "token"],           # 
	["Value_Decl",       ["colon: Token", "names, values, attrs: [dynamic]Ast_Node",
	                      "type: ^Ast_Node", "is_using: bool",
						  "mode: Value_Decl_Mode", "docs: [dynamic]Token"],     "colon"],           # @(no_bounds_check) my_var, success := get_info(file_path);
	["Import_Decl",      ["token, colon, collection, name: Token",
	                      "path, full_path: string", "is_using: bool"],         "token"],           # import std:os/posix;
	["Foreign_Lib_Decl", ["token, kind: Token", "locator, name: string"],       "token"],           # foreign_lib framework Foundation;
	["_Decl_End"],
	["Attribute",        ["eq_sign: Token", "name, value: ^Ast_Node"],          "eq_sign"],         # size=50
	["Attribute_List",   ["at_sign: Token", "attrs: [dynamic]Ast_Node"],        "at_sign"],         # @(size=50, serializable)
	["_Type_Begin"],
	["Pointer_Type",     ["token: Token", "type: ^Ast_Node"],                   "token"],           # ^i32
	["Array_Type",       ["token: Token", "count, type: ^Ast_Node"],            "token"],           # [4]string
	["Struct_Type",      ["token: Token", "fields: [dynamic]Ast_Node"],         "token"],           # struct {name: string; id: i32}
	["Class_Type",       ["token: Token", "tpl_params, stmts: [dynamic]Ast_Node",
	                      ""]]
]