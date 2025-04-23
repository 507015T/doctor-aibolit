generate-openapi:
	mkdir -p openapi/generated/schemas
	datamodel-codegen \
		--input openapi/openapi.yaml \
		--input-file-type openapi \
		--output openapi/generated/schemas/medication_schedule.py
