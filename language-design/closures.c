
// This code isn't meant to compile.
// The point here is to solidify how Helm
// will translate down and flatten out higher-level
// language features without making a stuffy "design document."

typedef struct Closure {
	void(void *) *proc,
	void         *data,
	void         *vals
} Closure;

#define call_closure(name) name.proc(name.data)

void main() {
	Closure c = sub();

	call_closure(c);

	free_closure(c);
}

void free_closure(Closure c) {
	// ???
}

typedef struct Closure_Data__sub__tp {
	int *i;
} Closure_Data__sub__tp;
typedef struct Closure_Data__sub__s {
	int *i;
	String *name;
} Closure_Data__sub__s;
typedef struct Closure_Data_Value__sub__s {
	int i;
	String name;
} Closure_Data_Value__sub__s;

void closure_proc__sub__tp(Closure_Data__sub__tp *data) {
	*(data->i) = 7;
}
void closure_proc__sub__s(Closure_Data__sub__s *data) {
	printf("%d, %*.s\n", *(data->i), helm_str_printf(*(data->name)));
}

Closure sub() {

	int i = 5;

	String name = helm_str_lit("hi");

	Closure tp = {new Closure_Data__sub__tp{&i},        closure_proc__sub__tp};
	Closure s =  {new Closure_Data__sub__s {&i, &name}, closure_proc__sub__s};

	call_closure(tp);

	i = 4;

	call_closure(s);

	i = 5;

	call_closure(s);

	free_closure(tp);

	//end of scope
	s.vals = malloc(sizeof(Closure_Data_Value__sub__s));
	s.vals.append(new data{i, name, nums});

	s.ChangeAllPointersToPointToNewData();

	return s;

}