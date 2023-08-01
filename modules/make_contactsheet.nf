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
  python3 $projectDir/bin/make_contactsheet.py $image --output ${meta.id}.contactsheet.jpeg
  """
}