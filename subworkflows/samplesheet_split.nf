workflow SAMPLESHEET_SPLIT {
    take:
    samplesheet
    main:
    Channel
        .fromPath(samplesheet)
        .splitCsv (header:true, sep:',' )
        // Make meta map from the samplesheet
        .map { 
            row -> 
            def meta = [:]
            meta.id = file(row.image).simpleName
            image = file(row.image)
            [meta, image]
        }
        .set {images }
        
    emit: 
    images
}