process synapse_get {

    conda "bioconda::synapseclient=2.6.0"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/synapseclient:2.6.0--pyh5e36f6f_0' :
        'quay.io/biocontainers/synapseclient:2.6.0--pyh5e36f6f_0' }"

    input:
    val meta

    secret 'SYNAPSE_AUTH_TOKEN'

    output:
    tuple val(meta), path('*')

    script:
    def args = task.ext.args ?: ''
    """
    synapse \\
        -p \$SYNAPSE_AUTH_TOKEN \\
        get \\
        $args \\
        $meta.id
    shopt -s nullglob
    for f in *\\ *; do mv "\${f}" "\${f// /_}"; done
    """
}