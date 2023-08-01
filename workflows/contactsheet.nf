include { SAMPLESHEET_SPLIT } from '../subworkflows/samplesheet_split.nf'
include { MAKE } from '../subworkflows/make.nf'
include { COMBINE } from '../subworkflows/combine.nf'

workflow CONTACTSHEET {
    SAMPLESHEET_SPLIT ( params.input )
    MAKE( SAMPLESHEET_SPLIT.out.images )
    MAKE.out.contactsheets.set{contactsheets}
    COMBINE( contactsheets )
}