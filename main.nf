#!/usr/bin/env nextflow

// Enable dsl2
nextflow.enable.dsl=2

if (params.samplesheet) { params.samplesheet = file(params.samplesheet) } else { exit 1, 'Input samplesheet not specified!' }

params.outdir = "outputs"

include { CONTACTSHEET } from './workflows/contactsheet.nf'

workflow NF_CONTACTSHEET {
  CONTACTSHEET ()
}

workflow {
  NF_CONTACTSHEET ()
}