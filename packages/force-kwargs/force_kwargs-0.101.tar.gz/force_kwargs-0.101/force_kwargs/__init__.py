def force_kwargs(n_allowed_args=0):
	def wrapped_func(original_func):
		def inner_wrapped_func(*args, **kwargs):
			if len(args) > n_allowed_args:
				raise SyntaxError("[force_kwargs] More than allowed num of positional arguments.")
			return original_func(*args, **kwargs)
		return inner_wrapped_func
	return wrapped_func

