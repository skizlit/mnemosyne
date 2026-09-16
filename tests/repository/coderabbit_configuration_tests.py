from pathlib import Path

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CODERABBIT_CONFIGURATION = REPOSITORY_ROOT / ".coderabbit.yaml"


class CoderabbitConfigurationTests:
    def test_reviews_are_automatic_for_non_draft_default_branch_pull_requests(self) -> None:
        configuration = self._load_configuration()
        auto_review = configuration["reviews"]["auto_review"]

        assert auto_review["enabled"] is True
        assert auto_review["auto_incremental_review"] is True
        assert auto_review["drafts"] is False
        assert auto_review["base_branches"] == ["main"]

    def test_review_instructions_cover_repository_priorities(self) -> None:
        configuration = self._load_configuration()
        reviews = configuration["reviews"]
        instructions = reviews["path_instructions"][0]["instructions"].casefold()

        assert reviews["profile"] == "quiet"
        assert reviews["path_filters"] == []
        assert all(
            priority in instructions
            for priority in (
                "correctness",
                "data loss",
                "public/private boundary",
                "regressions",
                "tests",
                "unnecessary complexity",
            )
        )

    def test_automated_code_writing_features_are_disabled(self) -> None:
        configuration = self._load_configuration()
        finishing_touches = configuration["reviews"]["finishing_touches"]

        assert all(
            feature["enabled"] is False
            for feature in finishing_touches.values()
        )

    def test_irrelevant_docstring_coverage_check_is_disabled(self) -> None:
        configuration = self._load_configuration()
        pre_merge_checks = configuration["reviews"]["pre_merge_checks"]

        assert pre_merge_checks["docstrings"]["mode"] == "off"

    def test_external_context_and_retained_knowledge_are_disabled(self) -> None:
        configuration = self._load_configuration()
        knowledge_base = configuration["knowledge_base"]

        assert knowledge_base["opt_out"] is True
        assert knowledge_base["web_search"]["enabled"] is False
        assert knowledge_base["automatic_linking_mode"] == "disabled"
        assert knowledge_base["linked_repositories"] == []

    @staticmethod
    def _load_configuration() -> dict[str, object]:
        configuration = yaml.safe_load(CODERABBIT_CONFIGURATION.read_text(encoding="utf-8"))

        assert isinstance(configuration, dict)
        return configuration
