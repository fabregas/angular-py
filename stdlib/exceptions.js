
function Exception(msg) {	
	return {
		inspect: function() { return "Exception(" + msg + ")"; },
		toJSON: function() { return msg; },
		valueOf: function() { return msg; },
	}
}
