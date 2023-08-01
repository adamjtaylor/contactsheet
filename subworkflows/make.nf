include { make_contactsheet } from "../modules/make_contactsheet.nf"

workflow MAKE {
  take:
  images
  
  main:
  make_contactsheet(images)
  make_contactsheet.out.set{contactsheets}

  emit: 
  contactsheets
}