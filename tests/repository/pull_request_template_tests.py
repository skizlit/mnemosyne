from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PULL_REQUEST_TEMPLATE = REPOSITORY_ROOT / ".github" / "pull_request_template.md"
CONTRIBUTING = REPOSITORY_ROOT / "CONTRIBUTING.md"


class PullRequestTemplateTests:
    def test_template_contains_required_merge_gate_sections(self) -> None:
        template = PULL_REQUEST_TEMPLATE.read_text(encoding="utf-8")

        required_sections = (
            "## Linked ticket",
            "## Change summary",
            "## Test evidence",
            "## Security boundary",
            "## Review and merge gate",
        )

        assert all(section in template for section in required_sections)

    def test_template_records_security_and_coderabbit_decisions(self) -> None:
        template = PULL_REQUEST_TEMPLATE.read_text(encoding="utf-8").casefold()

        required_text = (
            "closes #",
            "fixtures",
            "logs",
            "screenshots",
            "pr description",
            "coderabbit status",
            "dismissed findings and reasons",
            "jonathan has made the final merge decision",
        )

        assert all(text in template for text in required_text)

    def test_contribution_workflow_records_repository_conventions(self) -> None:
        contributing = CONTRIBUTING.read_text(encoding="utf-8")

        required_text = (
            "<type>/<issue-number>-<short_snake_case_name>",
            "[<issue-number>]",
            "Mirror the source layout under `tests/`",
            "CodeRabbit",
            "Jonathan's final approval",
        )

        assert all(text in contributing for text in required_text)
