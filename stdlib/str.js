

function PyStr(val) {
	return {
		inspect: function() { return val; },
		toJSON: function() { return val; },
		valueOf: function() { return val; },
		toString: function() { return val; },
		count: function(sub) { return (val.match(new RegExp(sub, "g")) || []).length}
	}
}

