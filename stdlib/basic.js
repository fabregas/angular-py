
function str(val) {
	return val.toString()
}

function len(val) {
	return val.valueOf().length
}

function print(val) {
	console.log(JSON.stringify(val))
}


function __fab_arr_eq(a1, a2) {
	if (!a2)
		return false;
	// compare lengths - can save a lot of time 
     	if (a1.length != a2.length)
		return false;
     
     	for (var i = 0, l=a1.length; i < l; i++) {
		if (__fab__neq(a1[i], a2[i])) {
			return false;
		}
	}
	return true;
}

function __fab__eq(v1, v2) {
	if (v1.valueOf() instanceof Array) {
		return __fab_arr_eq(v1.valueOf(), v2.valueOf())
	}
	return (v1.valueOf() === v2.valueOf())
}

function __fab__neq(v1, v2) {
	if (v1.valueOf() instanceof Array) {
		return ! __fab_arr_eq(v1.valueOf(), v2.valueOf())
	}
	return (v1.valueOf() !== v2.valueOf())
}

function __fab__lte(v1, v2) {
	return (v1.valueOf() <= v2.valueOf())
}

function __fab__lt(v1, v2) {
	return (v1.valueOf() < v2.valueOf())
}

function __fab__gte(v1, v2) {
	return (v1.valueOf() >= v2.valueOf())
}

function __fab__gt(v1, v2) {
	return (v1.valueOf() > v2.valueOf())
}

function __fab__mul_op(v1, v2) {
	if ((typeof v1.valueOf() == "string") && (typeof v2.valueOf() == "number")) {
		return PyStr(Array(v2.valueOf()+1).join(v1.valueOf()))
	} else if ((typeof v2.valueOf() == "string") && (typeof v1.valueOf() == "number")) {
		return PyStr(Array(v1.valueOf()+1).join(v2.valueOf()))
	} else {
		return v1 * v2
	}
}

function __fab__add_op(v1, v2) {
	if ((typeof v1.valueOf() == "string") && (typeof v2.valueOf() == "string")) {
		return PyStr(v1+v2)
	} else if (v1.valueOf() instanceof Array) {
		return v1.concat(v2)
	} else {
		return v1+v2
	}
}

function __fab__slice(target, start, upper) {
	val = target.valueOf()
	if (typeof val == "string") {
		return val.slice(start, upper)
	} else if (val instanceof Array) {
		return val.slice(start, upper)
	}	
	else {
		throw "unknown target type: " + target
	}
}

function __fab__idx(target, idx) {
	val = target.valueOf()
	if (idx < 0) {
		idx = val.length + idx
	}
	if (typeof val == "string") {
		return PyStr(val[idx])
	} else {
		return val[idx]
	}
}
