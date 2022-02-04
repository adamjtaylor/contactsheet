NAME=contactsheet

pull: 
	aws s3 --profile service-catalog sync s3://htan-image-header-db/contactsheet outputs/

he:
	 python run_queue.py --type synid --aws_profile sandbox-developer --gs_profile htan-dcc-gcs for_contactsheet.csv

test:
	 python run_queue.py --type synid --aws_profile sandbox-developer --gs_profile htan-dcc-gcs test_queue.csv

push:
	aws s3 --profile service-catalog sync outputs/ s3://htan-image-header-db/contactsheet