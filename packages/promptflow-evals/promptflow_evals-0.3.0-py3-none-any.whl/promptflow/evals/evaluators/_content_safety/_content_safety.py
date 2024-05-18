from concurrent.futures import ThreadPoolExecutor, as_completed

from ._hate_unfairness import HateUnfairnessEvaluator
from ._self_harm import SelfHarmEvaluator
from ._sexual import SexualEvaluator
from ._violence import ViolenceEvaluator


class ContentSafetyEvaluator:
    def __init__(self, project_scope: dict, parallel: bool = True, credential=None):
        """
        Initialize an evaluator configured to evaluate content safetry metrics for QA scenario.

        :param project_scope: The scope of the Azure AI project.
            It contains subscription id, resource group, and project name.
        :type project_scope: dict
        :param parallel: If True, use parallel execution for evaluators. Else, use sequential execution.
            Default is True.
        :param credential: The credential for connecting to Azure AI project.
        :type credential: TokenCredential
        :return: A function that evaluates content-safety metrics for "question-answering" scenario.
        :rtype: function

        **Usage**

        .. code-block:: python

            project_scope = {
                "subscription_id": "<subscription_id>",
                "resource_group_name": "<resource_group_name>",
                "project_name": "<project_name>",
            }
            eval_fn = ContentSafetyEvaluator(project_scope)
            result = eval_fn(
                question="What is the capital of France?",
                answer="Paris.",
            )
        """
        self._parallel = parallel
        self._evaluators = [
            ViolenceEvaluator(project_scope, credential),
            SexualEvaluator(project_scope, credential),
            SelfHarmEvaluator(project_scope, credential),
            HateUnfairnessEvaluator(project_scope, credential),
        ]

    def __call__(self, *, question: str, answer: str, **kwargs):
        """Evaluates content-safety metrics for "question-answering" scenario.

        :param question: The question to be evaluated.
        :type question: str
        :param answer: The answer to be evaluated.
        :type answer: str
        :param parallel: Whether to evaluate in parallel.
        :type parallel: bool
        :return: The scores for content-safety.
        :rtype: dict
        """
        results = {}
        if self._parallel:
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(evaluator, question=question, answer=answer, **kwargs): evaluator
                    for evaluator in self._evaluators
                }

                for future in as_completed(futures):
                    results.update(future.result())
        else:
            for evaluator in self._evaluators:
                results.update(evaluator(question=question, answer=answer, **kwargs))

        return results
