clean:
	rm -f $$(find . | grep "[.]pyc")
	rm -f $$(find . | grep "~$$") 
