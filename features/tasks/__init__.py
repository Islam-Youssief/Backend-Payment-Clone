import features.tasks.server_script as server_tasks
import features.tasks.wiremock as wiremock
import features.tasks.one_dir_test as one_dir_test


def register_tasks(registry):
    registry.register_task('startup-server', server_tasks.StartServerServiceTask())
    registry.register_task('start-wiremock', wiremock.StartWiremockTask())
    registry.register_task('one-dir-test', one_dir_test.OneDirTestTask())
