gen: spec router schema

# fmt:
# 	yapf -r -i --style='{based_on_style: chromium, indent_width: 4}' app

spec:
	cp ../swagger/swagger.yml .
	gsed -i 's/operationId: /operationId: views./g' swagger.yml

router:
	pyramid-swagger-router --driver=./driver.py:Driver --logging=DEBUG ./swagger.yml app

schema:
	swagger-marshmallow-codegen --full --logging=DEBUG ./swagger.yml > app/schema.py

run:
	PYTHONPATH=. python app/__init__.py
