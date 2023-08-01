process make_contactsheet {
  input:
    tuple val(meta), file(image) 
  output:
    file('*.jpeg')
  publishDir "$params.outdir/"
  stub: 
  """
  touch contactsheet.jpeg
  """
  script:
  """
  contactsheet.py $image --output ${meta.id}.contactsheet.jpeg
  """
}