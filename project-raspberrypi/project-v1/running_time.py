class Time:
	def is_up(self):
		current = get_time()
		isUp = current >= self.end
		return isUp

	def remaining(self):
		current = get_time()
		remaining = self.end - current
		return remaining

	def spent(self):
		current = get_time()
		spent = self.until - self.remaining()
		return spent

    def reset(self):
		now = get_time()
		self.end = now + self.until

    def __str__(self):
		return self.remaining()

	def __init__(self, until):
		self.until = until
		self.reset()
		

from timeit import default_timer as get_time
if __name__ == "__main__":
	pass
