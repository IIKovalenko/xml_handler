init:
	python -m pip install -r requirements.txt

run:
	python -m xml_handler

test:
	python -m unittest discover tests

test2:
	tox

clean:
	rm *.zip
	rm *.csv

benchmark:
	time python -m xml_handler
