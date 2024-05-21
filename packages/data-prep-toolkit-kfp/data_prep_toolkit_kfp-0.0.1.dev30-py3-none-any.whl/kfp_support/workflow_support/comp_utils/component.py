import kfp.dsl as dsl
from kfp import kubernetes


class CompileComponentUtils:
    """
    Class containing methods supporting building pipelines
    """

    @staticmethod
    def add_settings_to_component(
            task: dsl.PipelineTask,
            timeout: int,
            image_pull_policy: str = "IfNotPresent",
            cache_strategy: bool = False,
    ) -> None:
        """
        Add settings to kfp task
        :param task: kfp task
        :param timeout: timeout to set to the component in seconds
        :param image_pull_policy: pull policy to set to the component
        :param cache_strategy: cache strategy
        """

        kubernetes.use_field_path_as_env(task, env_name=RUN_NAME,
                                         field_path="metadata.annotations['pipelines.kubeflow.org/run_name']")
        # Set cashing
        task.set_caching_options(enable_caching=cache_strategy)
        # image pull policy
        kubernetes.set_image_pull_policy(task, image_pull_policy)
        # Set the timeout for the task to one day (in seconds)
        kubernetes.set_timeout(task, seconds=timeout)
