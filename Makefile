generate-openapi:
	mkdir -p openapi/generated/schemas
	datamodel-codegen \
		--input openapi/openapi.yaml \
		--input-file-type openapi \
		--output openapi/generated/schemas/medication_schedule.py

generate-proto:
	# Не справился
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. medication_schedule.proto
