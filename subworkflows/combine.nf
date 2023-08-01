include { make_report } from "../modules/make_report.nf"

workflow COMBINE {
    take:
    contactsheets

    main:
    contactsheets
        .collect()
        .set {collected }
    make_report(collected)
    make_report.out.set{report}
        
    emit: 
    report
}