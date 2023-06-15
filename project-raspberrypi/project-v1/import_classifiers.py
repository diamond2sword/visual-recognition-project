def main()->int:
	c = classifiers.Classifier(hasPreview=True)
	c.main()
	return 0

import classifiers
if __name__ == "__main__":
	main()
