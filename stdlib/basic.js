
function str(val) {
	return val.toString()
}

function print(val) {
	console.log(JSON.stringify(val))
}

function __fab__eq(v1, v2) {
	return (v1.valueOf() === v2.valueOf())
}

function __fab__neq(v1, v2) {
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
