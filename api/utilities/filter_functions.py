
def like(column, value):
	return column.ilike('%{}%'.format(value))


def is_equal(column, value):
	return column == value


def not_equal(column, value):
	return column != value


def greater_than(column, value):
	return column > value


def greater_or_equal(column, value):
	return column >= value


def less_than(column, value):
	return column < value


def less_or_equal(column, value):
	return column <= value
