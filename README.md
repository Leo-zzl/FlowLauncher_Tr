# Leo Translate

**Flow Launcher 大模型翻译插件：完整译文在第一项，专业词组与语境解释从第二项开始。**

**An LLM-powered translation plugin for Flow Launcher: one result for the full translation, followed by English phrases explained in context.**

[简体中文](#简体中文) · [English](#english) · [下载 / Downloads](https://github.com/Leo-zzl/FlowLauncher_Tr/releases) · [版本记录 / Release notes](docs/release-notes)

**当前版本 / Current version: 1.1.0** · Windows · Python 3.9+ · Chat Completions-compatible API

| 版本 / Version | 安装包 / Plugin package | 更新说明 / Release notes |
| --- | --- | --- |
| **1.1.0 — 推荐 / Recommended** | [LeoTranslate-1.1.0.zip](https://github.com/Leo-zzl/FlowLauncher_Tr/releases/download/v1.1.0/LeoTranslate-1.1.0.zip) | [v1.1.0](https://github.com/Leo-zzl/FlowLauncher_Tr/releases/tag/v1.1.0) |
| 1.0.0 — 初始版本 / Initial release | [LeoTranslate-1.0.0.zip](https://github.com/Leo-zzl/FlowLauncher_Tr/releases/download/v1.0.0/LeoTranslate-1.0.0.zip) | [v1.0.0](https://github.com/Leo-zzl/FlowLauncher_Tr/releases/tag/v1.0.0) |

> 安装请下载上表中的插件 ZIP；GitHub 自动生成的 **Source code** 压缩包包含仓库目录，不能直接当作插件安装包使用。每个 Release 均附有 `SHA256SUMS.txt`。
>
> Install the plugin ZIP linked above. GitHub's automatically generated **Source code** archives contain the repository layout and are not ready-to-install plugin packages. Each release includes `SHA256SUMS.txt`.

## 简体中文

### 功能与效果

- **完整译文只占第一项**：`Alt+1` 或回车复制全文，长句不再拆成多个选项。
- **词组结合原句解释**：后续项展示专业英文词组、中文释义、本句语境及所在英文句，默认最多 5 个。
- **自选模型与提示词**：可配置 API URL、模型、密钥、翻译要求和词组解释风格。
- **中英互译与指定语言**：支持自动中英互译，也可指定英语、简体中文或阿拉伯语。
- **一次请求返回两类内容**：译文和词组解释通过同一次模型调用返回。
- **长文本预览与复制**：支持 F1 预览、鼠标悬停提示、回车和 Ctrl+C 复制。

输入示例：

```text
tr en 扩大上行容量，保障高密度场景下的用户体验。
tr zh Uplink capacity improves assured experience in high-density scenarios.
```

结果示意（具体措辞由模型生成）：

| 选项 | 内容 | 执行后 |
| --- | --- | --- |
| **Alt+1** | 原文的完整译文 | 复制完整译文，不包含词组解释 |
| **Alt+2** | uplink capacity — 上行容量；解释本句中的上行业务承载能力 | 复制该词组、释义、语境和所在英文句 |
| **Alt+3** | assured experience — 有保障的体验；解释本句强调的体验保障 | 复制该词组的完整解释 |

简单句可能没有值得解释的专业词组，此时只显示译文。快捷键遵循 Flow 的配置；默认排序为译文在前、词组在后，人工置顶仍可能覆盖这一顺序。

### 安装与首次配置

1. 安装并启动 [Flow Launcher](https://www.flowlauncher.com/)，下载 **LeoTranslate-1.1.0.zip**。
2. 在 Flow 搜索框输入 `Flow Launcher UserData Folder`，打开实际使用的用户数据目录，再退出 Flow。
3. 在该目录的 `Plugins` 下新建 `LeoTranslate-1.1.0`，将 ZIP 内文件解压到此处。确认路径为 `Plugins\LeoTranslate-1.1.0\plugin.json`，避免多套一层目录。
4. 重启 Flow，进入 **设置 → 插件 → Leo Translate**，填写完整 API URL、模型名称和 API Key。
5. 按 `Alt+Space` 唤起 Flow，输入 `tr 需要翻译的内容`。

插件仅使用 Python 标准库，无需 `pip install`。首次加载 Python 插件时，Flow 通常会准备运行环境；如果下载受阻，请在 Flow 设置中配置可用的 Python 路径。

### 使用方法

| 输入 | 行为 |
| --- | --- |
| `tr 需要翻译的内容` | 使用默认方向：中文译英语，其他语言译简体中文 |
| `tr en 需要翻译的内容` | 译成英语 |
| `tr zh Text to translate` | 译成简体中文 |
| `tr ar 需要翻译的内容` | 译成阿拉伯语 |
| `tr auto Text to translate` | 使用自动中英互译规则 |

`tr` 是默认触发词；`en`、`zh`、`ar`、`auto` 是插件识别的语言前缀。默认停止输入约 **800 毫秒**后调用接口。

**长文本查看：**Flow 默认列表有固定行高，标题可能省略显示，但完整译文仍属于同一项。选中第一项按 **F1** 打开预览，也可开启 **Always Preview / 始终预览**。鼠标悬停可看全文提示；如果仍超出面板可视范围，复制全文查看。复制时保留原有段落和换行。

**手动发送：**在设置中开启“仅在原文末尾输入 `;;` 时发送”，然后输入：

```text
tr en 请确认明天会议的时间。;;
```

两个英文分号会在发送前去除。自动模式下，分号只是原文的一部分。已发送的请求无法撤销，继续修改可能产生额外调用；手动模式适合长句或按量计费接口。

### 设置说明

| 设置项 | 默认值 / 配置要求 |
| --- | --- |
| API URL | 必填完整端点，例如 `https://api.example.com/v1/chat/completions`；不自动补路径 |
| 模型名称 | 必填服务商提供的准确模型 ID |
| API Key | 使用 Bearer 鉴权；留空时读取 `LEO_TRANSLATE_API_KEY` 环境变量，本机免密接口也可留空 |
| 默认翻译方向 | 自动中英互译；可改为英语、简体中文或阿拉伯语 |
| 系统提示词 | 翻译要求；`{target}` 会替换为目标语言指令 |
| 专业词组数量 | 默认最多 5 个；范围 0–8；设为 0 仅返回译文 |
| 词组与语境解释提示词 | 默认优先电信、技术和商务表达，用中文解释本句含义；可自定义 |
| 停止输入后的等待时间 | 默认 800 毫秒；范围 0–5000 |
| 仅在末尾输入 `;;` 时发送 | 默认关闭 |
| 请求超时 | 默认 45 秒；范围 1–120 |

API URL 应为 **Chat Completions 兼容端点**，不是聊天网页。原生 Anthropic Messages、Gemini、Responses 或 Azure 专用协议需先通过兼容网关转换。远程接口要求 HTTPS；本机 `localhost`、`127.0.0.1`、`[::1]` 可使用 HTTP。不跟随重定向。

修改 Windows 环境变量后，请完全退出并重启 Flow。密钥框仅遮挡显示，不代表加密存储；环境变量也不是加密存储。请勿把真实密钥提交到仓库。

### 从 1.0.0 升级

1. 打开原插件目录并退出 Flow。
2. 将 **1.1.0 安装 ZIP 内的文件覆盖到原插件文件夹**，保留用户自己的配置文件。
3. 重启 Flow，确认插件页显示 1.1.0。目录名可以仍为 `LeoTranslate-1.0.0`。

插件 ID、触发词和已有设置字段未改变，原接口配置应继续使用。不要同时保留两个启用的插件目录。旧翻译提示词可以保留，程序会追加新版所需的结构化输出约定。

### 常见问题与限制

| 问题 | 处理方式 |
| --- | --- |
| 第一项文字显示不全 | F1 打开预览，或悬停 / 复制全文；默认结果行不会自动无限增高 |
| 仍出现“译文 1/2、2/2” | 检查是否仍运行旧版；退出后覆盖原目录，并确认没有重复插件 |
| 词组跑到第一项 | 取消 Flow 对该词组的人工置顶 |
| 没有词组解释 | 检查数量是否为 0；简单句或只返回普通译文的模型也可能没有词组项 |
| HTTP 401 / 404 / 429 | 分别检查密钥、完整 URL / 模型、余额及限流 |
| 返回 JSON 不完整 | 重试、缩短原文，或使用更能遵循 JSON 指令的模型 |
| 回车复制失败 | 尝试 Ctrl+C，并检查 PowerShell 或剪贴板是否受系统策略限制 |

单次原文最多 **12000 字符**，还可能受 Windows 命令行长度限制，适合句子和短段落。暂不支持流式显示、自定义鉴权头或额外请求字段。模型释义仍需按业务语境核对。

插件自身不保存原文、译文或密钥日志，不建立译文缓存；防抖临时文件只包含随机请求 ID。Flow 的搜索历史与日志、API 服务商的数据保留策略由各自管理。

## English

### Features and result layout

- **One result for the full translation:** press `Alt+1` or Enter to copy it. Long translations no longer occupy several result slots.
- **English phrases explained in context:** subsequent results contain a phrase, its Chinese meaning, a Chinese explanation of its role in the sentence, and the English source sentence. Up to five phrases are shown by default.
- **Your API and prompts:** configure the endpoint, model, API key, translation instructions, and glossary instructions.
- **Automatic or explicit language selection:** translate between Chinese and English automatically, or select English, Simplified Chinese, or Arabic.
- **One model request:** the translation and phrase explanations are returned together.
- **Full-text access:** use F1 previews, hover tooltips, Enter, or Ctrl+C.

Examples:

```text
tr en 扩大上行容量，保障高密度场景下的用户体验。
tr zh Uplink capacity improves assured experience in high-density scenarios.
```

Illustrative results; wording depends on the model:

| Result | Content | Action |
| --- | --- | --- |
| **Alt+1** | Full translation of the input | Copy only the complete translation |
| **Alt+2** | uplink capacity — 上行容量, with an explanation of its meaning in this sentence | Copy the phrase, meaning, context, and source sentence |
| **Alt+3** | assured experience — 有保障的体验, with a sentence-specific explanation | Copy the complete phrase explanation |

Simple sentences may produce no glossary entries. Shortcuts follow your Flow configuration. Translations rank above phrases by default; manually pinned results can override this order. The settings UI and default glossary explanations are currently in Chinese.

### Installation and initial setup

1. Install and launch [Flow Launcher](https://www.flowlauncher.com/), then download **LeoTranslate-1.1.0.zip**.
2. Search for `Flow Launcher UserData Folder` in Flow to open the active user data directory, then exit Flow.
3. Create `LeoTranslate-1.1.0` inside its `Plugins` directory and extract the ZIP contents there. Check that the path is `Plugins\LeoTranslate-1.1.0\plugin.json`, without an extra nested directory.
4. Restart Flow. Open **Settings → Plugins → Leo Translate** and enter the full API URL, model ID, and API key.
5. Press `Alt+Space` and type `tr Text to translate`.

The plugin uses only the Python standard library; no `pip install` is required. Flow normally prepares its Python runtime when loading a Python plugin for the first time. If the download is blocked, configure a working Python executable in Flow settings.

### Usage

| Query | Behavior |
| --- | --- |
| `tr Text to translate` | Default rule: Chinese input → English; other input → Simplified Chinese |
| `tr en 需要翻译的内容` | Translate into English |
| `tr zh Text to translate` | Translate into Simplified Chinese |
| `tr ar Text to translate` | Translate into Arabic |
| `tr auto Text to translate` | Apply the automatic Chinese/English rule |

`tr` is the default action keyword. The plugin recognizes `en`, `zh`, `ar`, and `auto` as language prefixes. By default, it calls the API after you stop typing for about **800 ms**.

**Reading long translations:** Flow's default list has a fixed row height, so the title may be clipped. The complete translation still belongs to one result. Select it and press **F1** to open the preview, or enable **Always Preview**. Hover over the result for its full-text tooltip. If the content exceeds the visible preview area, copy the full text to read it elsewhere. Copying preserves paragraphs and line breaks.

**Manual submission:** enable the setting that requires trailing `;;`, then type:

```text
tr zh Please confirm tomorrow's meeting time.;;
```

The two semicolons are removed before submission. In automatic mode, they remain part of the input. Requests already sent cannot be cancelled, and further edits may cause additional calls. Manual mode is useful for longer input or metered APIs.

### Configuration

| Setting | Default / requirement |
| --- | --- |
| API URL | Required full endpoint, e.g. `https://api.example.com/v1/chat/completions`; no path is appended |
| Model | Required model ID supplied by your provider |
| API key | Bearer authentication; when blank, reads `LEO_TRANSLATE_API_KEY`. Local services without authentication may leave it blank |
| Default target | Automatic Chinese/English; alternatively English, Simplified Chinese, or Arabic |
| System prompt | Translation instructions; `{target}` is replaced with the target-language instruction |
| Phrase count | Up to 5 by default; range 0–8; set to 0 for translation only |
| Glossary prompt | Defaults to telecom, technical, and business expressions explained in Chinese in the context of the sentence; customizable |
| Debounce delay | 800 ms by default; range 0–5000 |
| Require trailing `;;` | Off by default |
| Request timeout | 45 seconds by default; range 1–120 |

Use a **Chat Completions-compatible API endpoint**, not a chat website. Native Anthropic Messages, Gemini, Responses, and Azure-specific protocols require a compatible gateway. Remote endpoints must use HTTPS; local `localhost`, `127.0.0.1`, and `[::1]` endpoints may use HTTP. Redirects are not followed.

Completely exit and restart Flow after changing Windows environment variables. Masked password inputs and environment variables do not imply encrypted storage. Never commit real API keys to the repository.

### Upgrading from 1.0.0

1. Locate the existing plugin directory and exit Flow.
2. **Extract the 1.1.0 plugin ZIP into that same directory**, replacing plugin files while preserving your own configuration files.
3. Restart Flow and confirm that the plugin settings show 1.1.0. The directory may keep its old `LeoTranslate-1.0.0` name.

The plugin ID, action keyword, and existing setting keys are unchanged, so your API configuration should remain available. Keep only one enabled installation. Existing translation prompts can be retained; the plugin appends the structured-output instructions required by 1.1.0.

### Troubleshooting and limitations

| Issue | What to check |
| --- | --- |
| The first result is clipped | Press F1, hover, or copy the full text; the default result row does not grow indefinitely |
| The translation still occupies several slots | Check for an old or duplicate installation; exit Flow and replace the files in the original directory |
| A phrase appears before the translation | Remove any manual pin applied to that result in Flow |
| No phrase explanations | Check that phrase count is above 0; simple sentences or plain-text-only model responses may produce no glossary |
| HTTP 401 / 404 / 429 | Check the key, endpoint/model, or quota/rate limit, respectively |
| Incomplete JSON response | Retry, shorten the input, or use a model that follows JSON instructions more reliably |
| Enter does not copy | Try Ctrl+C and check whether PowerShell or clipboard access is restricted |

Input is limited to **12,000 characters** and may also encounter Windows command-line length limits. Use sentences and short passages rather than entire documents. Streaming, custom authentication headers, and extra request fields are not supported. Review model-generated definitions for accuracy in your domain.

The plugin itself does not log source text, translations, or keys, and does not cache translations. Its debounce file stores only a random request ID. Flow's own history/logging and your API provider's retention policies are separate.

## 开发与验证 / Development and validation

无需真实 API 密钥即可运行本地模拟接口测试。/ Run the mock-API tests without a real API key:

```bash
python -m unittest discover -s tests -v
```

| 文件 / File | 用途 / Purpose |
| --- | --- |
| `main.py` | 查询处理、API 请求、结果解析与复制 / Query handling, API requests, response parsing, and copying |
| `plugin.json` | 插件身份、版本和入口 / Plugin identity, version, and entry point |
| `SettingsTemplate.yaml` | Flow 插件设置表单 / Settings form in Flow |
| `tests/test_plugin.py` | 模拟 API 与边界测试 / Mock-API and edge-case tests |
| `.github/scripts/package.py` | 生成安装包和校验文件 / Build the plugin ZIP and checksum file |
| `.github/workflows/release.yml` | 测试、打包与发布 / Test, package, and publish |

**验证范围 / Validation scope:** 1.0.0 包含 16 项测试，1.1.0 包含 20 项测试；两版均已通过 GitHub Actions。测试覆盖模拟 API 往返、中文与长文本、JSON-RPC、防抖及异常处理；1.1.0 另覆盖单项译文、排序和词组过滤。未在 Windows Flow 图形界面或真实付费模型接口上完成验证。

Version 1.0.0 has 16 tests and 1.1.0 has 20; both passed GitHub Actions. Tests cover mock-API round trips, Unicode and long text, JSON-RPC, debouncing, and error handling. Version 1.1.0 also tests single-result translations, ordering, and glossary filtering. Windows Flow GUI behavior and live paid-model endpoints have not been validated.

模型请求与输出协议的说明见源码。/ See the source for the model request and structured-output contract. 标准输出仅用于 JSON-RPC 响应。/ Keep standard output reserved for JSON-RPC responses.

[Flow 官方文档 / Flow documentation](https://www.flowlauncher.com/docs/#/) · [发布工作流 / Release workflow](https://github.com/Leo-zzl/FlowLauncher_Tr/actions/workflows/release.yml)

本插件通过 Release 手动安装，尚未上架 Flow 插件商店。/ Install manually from Releases; the plugin is not currently listed in the Flow Plugin Store.
