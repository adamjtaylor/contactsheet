NAME=contactsheet

pull: 
	aws s3 --profile service-catalog sync s3://htan-image-header-db/contactsheet outputs/

release1:
	 python run_queue.py --type synid --aws_profile sandbox-developer --gs_profile htan-dcc-gcs for_contactsheet.csv

release2:
	 python run_queue.py --type synid --aws_profile sandbox-developer --gs_profile htan-dcc-gcs release2_ometiffs.csv

push:
	aws s3 --profile service-catalog sync outputs/ s3://htan-image-header-db/contactsheet