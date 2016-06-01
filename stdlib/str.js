

function PyStr(val) {
	return {
		inspect: function() { return val; },
		toJSON: function() { return val; },
		valueOf: function() { return val; },
		toString: function() { return val; }
	}
}

