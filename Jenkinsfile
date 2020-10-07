pipeline {
    agent none
    stages {
        stage('Trigger model generation') {
            agent { label 'master' }
            when {
                tag pattern: "v\\d+\\.\\d+\\.\\d+(-\\w+-\\d+)?", comparator: "REGEXP"
            }
            steps {
                script {
                    VERSION = TAG_NAME[1..-1]
                }
                sh "echo Version is ${VERSION}"
                build job: '/FINTLabs/fint-devops-model-release/master', parameters: [
                    string(name: 'MODEL_VERSION', value: "${VERSION}"),
                    string(name: 'VERSION', value: "${VERSION}")]
                build job: '/FINTLabs/fint-jsonschema/master', parameters: [
                    string(name: 'MODEL_VERSION', value: "${VERSION}")]
            }
        }
    }
}
