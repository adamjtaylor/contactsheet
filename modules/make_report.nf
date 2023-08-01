process make_report {
  input:
    file(input) 
  output:
    file('report.pdf')
  publishDir "$params.outdir/"
  stub: 
  """
  touch report.pdf
  """
  script:
  """
  magick $input report.pdf
  """
}