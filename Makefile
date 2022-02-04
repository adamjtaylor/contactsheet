NAME=contactsheet

pull: 
	aws s3 --profile service-catalog sync s3://htan-image-header-db/contactsheet outputs/

release1:
	 python run_queue.py --type synid --aws_profile sandbox_developer --gs_profile htan-dcc-gcs release1_images.csv

release1:
	 python run_queue.py --type synid --aws_profile sandbox_developer --gs_profile htan-dcc-gcs release2_ometiffs.csv

push:
	aws s3 --profile service-catalog sync outputs/ s3://htan-image-header-db/contactsheet