# Add Leo Translate

Adds Leo Translate, a Python plugin that uses a user-configured Chat Completions-compatible API to translate text and explain English technical/business phrases in context.

- The full translation is always the first result. Subsequent results contain English phrases, Chinese meanings, contextual explanations, and source sentences.
- Users configure their own API endpoint, model, and optional API key; there is no bundled key or hard-coded provider. Requests are sent only to the configured endpoint.
- The plugin itself does not persist source text, translations, or API keys in logs or caches. Flow's own history and the configured provider's retention policies are separate.
- Runtime dependencies: Python standard library only.
- Default action keyword: `tr`.
- Release: https://github.com/Leo-zzl/FlowLauncher_Tr/releases/tag/v1.1.1
- Source: https://github.com/Leo-zzl/FlowLauncher_Tr
- Automated test/build/release workflow: https://github.com/Leo-zzl/FlowLauncher_Tr/actions/workflows/release.yml
- Bilingual setup, configuration, and upgrade documentation is included.

The settings UI and default glossary explanations are Chinese. The endpoint and both prompts are customizable. Long translations use Flow's preview/tooltips and remain a single selectable result.

This submission adds one new file under `plugins/`; it does not edit the generated `plugins.json` or add a `Tested` field. The plugin follows the Plugin Store policy and does not facilitate prohibited activities.
