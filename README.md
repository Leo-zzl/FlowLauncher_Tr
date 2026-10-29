# Leo Translate 1.1.0

Windows / Flow Launcher · Python 3.9+ · 仅使用标准库 · OpenAI 兼容 Chat Completions API

## 本次变化

| 结果项 | 内容 | 快捷操作 |
| --- | --- | --- |
| 第 1 项（Alt+1） | 原文的完整翻译，始终只占一个选项 | Alt+1 / 回车复制完整译文，Ctrl+C 也可复制 |
| 第 2 项起（Alt+2…） | 专业英文词组 — 中文释义；副标题为本句语境解释 | 复制该词组、释义、语境及所在英文句 |

删除了 1.0.0 的“每 60 字符拆成一条结果”逻辑。长译文不再占用 Alt+2、Alt+3。返回结果设置不同分数并关闭 AddSelectedCount，使使用次数不改变译文和词组的顺序。不要手动把词组置顶；Flow 的人工置顶设置仍可能覆盖排序。

### 长文本如何查看

Flow 默认的结果列表有固定行高；Python JSON-RPC 插件不能给某一个结果项注入自定义的多行界面。**本版保证完整译文属于同一个结果项，但不会让默认结果行无限增高。**

- 选中第一项，按 **F1** 打开 Flow 的全文预览；也可以在设置中开启 **Always Preview / 始终预览**。
- 鼠标悬停在第一项标题或副标题上，可查看完整译文提示。
- 如果正文仍超出预览面板可视范围，Alt+1 或回车复制全文查看；原有段落、换行会保留。
- 后续词组也都有自己的预览和提示，显示“中文释义 → 本句语境 → 所在英文句”。

本实现使用已核对的 Flow v2.1.4 Result.Preview.Description、TitleToolTip、CopyText 等接口；没有依赖仅开发版支持的自定义 Markdown 预览字段。原生列表仍可能截短一行文字，这与译文缺失不同：预览、提示和复制数据均保留全文。

## 从 1.0.0 升级（保留配置）

1. 在 Flow 搜索框输入 `Flow Launcher UserData Folder`，打开当前用户数据目录，找到已安装的 `Plugins\LeoTranslate-1.0.0`。
2. 退出 Flow Launcher。
3. 把本 ZIP 内文件解压并覆盖到**原插件文件夹**。目录名可以仍叫 `LeoTranslate-1.0.0`，实际版本由 plugin.json 中的 1.1.0 决定。
4. 不要删除或覆盖用户自行创建的配置文件；本 ZIP 不含真实密钥或用户配置文件。不要同时保留两个启用的 Leo Translate 插件目录。
5. 重新启动 Flow，确认插件页显示 1.1.0，原 API URL、模型、密钥和自定义提示词应继续使用。
6. 新增“专业词组数量”和“词组与语境解释提示词”两个设置，首次未保存时使用程序内置默认值。
7. 按 F1 开启预览，或开启 Always Preview。

插件 ID、触发词和已有设置字段名称未改变。不要为了升级去创建另一个插件 ID。仍可保留原翻译提示词，程序会在其后追加 1.1.0 所需的 JSON 输出约定。

## 第一次安装

1. 在 Flow 中搜索 `Flow Launcher UserData Folder`，执行相应结果。
2. 退出 Flow。在其 `Plugins` 目录下新建 `LeoTranslate-1.1.0`，将 ZIP 内文件放入。
3. 确保是 `Plugins\LeoTranslate-1.1.0\plugin.json`，不要多套一层目录。
4. 重启 Flow，在“设置 → 插件 → Leo Translate”填写 API URL、模型和密钥。
5. 首次使用 Python 插件时，Flow 通常自动准备运行环境；如果下载被网络阻止，需在 Flow 设置中配置可用的 Python 路径。无需 pip install。

## 使用方法

```text
tr 请确认明天会议的时间。
tr en 扩大上行容量，保障高密度场景下的用户体验。
tr zh Uplink capacity improves assured experience in high-density scenarios.
tr ar 请问账单什么时候到期？
```

默认停止输入约 0.8 秒后发送请求。`en`、`zh`、`ar`、`auto` 是保留的语言前缀；不指定则使用设置中的翻译方向。自动模式为中文译英文，其他语言译简体中文。

示意结果（由模型生成，措辞依实际返回而定）：

| 快捷键 | 标题 | 本句解释 |
| --- | --- | --- |
| Alt+1 | 上行容量可改善高密度场景下的体验保障。 | 完整译文，复制时不包含词组解释 |
| Alt+2 | uplink capacity — 上行容量 | 本句指网络承载终端向基站发送数据的能力 |
| Alt+3 | assured experience — 有保障的体验 | 本句强调网络在负载较高时仍能提供稳定的业务体验 |
| Alt+4 | high-density scenarios — 高密度场景 | 本句指大量用户集中接入的场馆、展会等环境 |

简单句未必包含值得解释的专业词组，允许只显示译文。模型输出的术语会经过校验：必须出现在英文原文或译文中、不得重复、必须包含中文释义与语境解释；例句必须摘自原文或译文，否则不展示该例句。规则校验不能替代人工核对模型释义。

## 设置

| 设置项 | 说明 |
| --- | --- |
| API URL | 完整端点，例如 `https://你的服务域名/v1/chat/completions`，不自动补路径 |
| 模型名称 | 服务商提供的准确模型 ID |
| API Key | 通过 Authorization: Bearer 发送；可留空读取环境变量 LEO_TRANSLATE_API_KEY |
| 默认翻译方向 | 自动中英互译 / 英语 / 简体中文 / 阿拉伯语 |
| 系统提示词 | 翻译要求，支持 `{target}` 目标语言占位符 |
| 专业词组数量 | 默认最多 5 个，范围 0–8；0 表示只返回译文 |
| 词组与语境解释提示词 | 自定义选词偏好及解释风格，默认优先电信、技术和商务表达 |
| 停止输入后的等待时间 | 默认 800 毫秒，范围 0–5000 |
| 仅在末尾输入 ;; 时发送 | 长文或按量计费接口建议开启 |
| 请求超时 | 默认 45 秒，范围 1–120 |

手动模式示例：

```text
tr en 请确认明天会议的时间。;;
```

原文末尾两个英文分号会被去除后发送。默认自动模式下分号只是原文的一部分。已经发出的 API 请求无法撤销，继续编辑可能产生额外调用；旧请求结果会被抑制，不覆盖新查询。本版不自动重试、不保存译文缓存。

API URL 必须是服务商的 API 地址，而不是聊天网页。支持 Chat Completions 兼容接口，不支持原生 Anthropic Messages、Gemini、Responses 或 Azure 专用协议；若网关转换为支持的格式则可接入。远程 URL 要求 HTTPS，本机 localhost / 127.0.0.1 / [::1] 可以 HTTP；不跟随重定向。

密钥只在本机填写。密码框仅遮挡显示，不代表加密存储；环境变量也不是加密存储。如通过环境变量配置，设置后需完全退出并重启 Flow。

## 实现说明

Flow 查询 → 解析语言 → 防抖 → 一次 HTTP POST → 解析完整译文与词组 JSON → 第一项译文 / 后续项词组。

- `plugin.json`：固定插件 ID、触发词 tr、版本和 Python 入口。
- `SettingsTemplate.yaml`：配置表单；升级保留已有字段名。
- `main.py`：所有运行逻辑，仅使用标准库。
- `Images/app.png`：插件图标。
- `tests/test_plugin.py`：模拟 API 端到端与边界测试。

原文以独立 user 消息发送；自定义翻译提示词、语境提示词及输出协议放入 system 消息。不会把文本拼在 URL 上。

模型输出的 content 预期为以下 JSON 字符串：

```json
{
  "translation": "原文的完整译文",
  "terms": [
    {
      "term": "uplink capacity",
      "meaning": "上行容量",
      "context": "结合当前句子的业务场景解释词组的具体含义。",
      "example": "Uplink capacity improves assured experience."
    }
  ]
}
```

为兼容不同供应商，没有强制添加 response_format 参数；通过提示词要求 JSON。兼容带 ```json 围栏的返回值。如果模型仍只返回普通译文，本版保留一个完整译文项，不杜撰词组。若返回的是损坏 JSON 或缺失 translation 的 JSON，则显示可读错误，而非把原始 JSON 当译文复制。

回车复制通过 PowerShell 执行，文本由 stdin 输入，不作为 PowerShell 源码执行。Ctrl+C 使用 Flow 原生 CopyText 字段。标准输出只写 JSON-RPC 响应，不输出调试日志。

## 验证与限制

```powershell
python -m unittest discover -s tests -v
```

20 项测试通过：模拟 HTTP 请求/响应、真实进程 JSON-RPC 入口、中文/多行/长文本、词组字段解析、重复和不存在的术语过滤、例句校验、始终只有一个译文项、固定排序、独立复制、鉴权/重定向/非 JSON 错误、防抖、旧响应抑制等。测试不调用真实付费模型。

本构建环境不是 Windows：本版尚未在 Windows Flow 界面或你的真实 API 上实测。列表固定行高、预览面板尺寸、快捷键映射和人工置顶由 Flow 管理。原文最多 12000 字符；长输入还可能受 Windows 进程命令行长度限制，不建议用作整篇文档翻译。若模型返回 finish_reason: length，会提示译文被截断。暂不支持流式显示、自定义鉴权头或额外请求字段。

插件自身不记录原文、译文和密钥；临时防抖文件只含随机请求 ID。Flow 自身的历史/日志及 API 服务商的数据保留策略由各自管理。

## 常见问题

| 问题 | 处理 |
| --- | --- |
| 第一项仍是一行省略显示 | 这是默认列表的布局；选中后 F1 看预览，或悬停 / 复制全文 |
| 仍出现“译文 1/2、2/2” | 旧版仍在运行；退出 Flow，覆盖原目录，确认只启用一个插件目录 |
| 词组跑到了第一项 | 检查 Flow 是否对该项设置了人工置顶并取消 |
| 没有词组解释 | 简单句可能无专业词组；检查数量是否为 0，模型是否只返回了普通译文 |
| HTTP 401 / 404 / 429 | 分别检查 Key、完整 URL/模型、额度和限流 |
| 模型 JSON 不完整 | 重试或改用遵循 JSON 输出指令的模型；适当缩短输入 |
| 复制失败 | 可尝试 Flow 的 Ctrl+C，检查 PowerShell / 剪贴板是否被系统策略限制 |

官方参考：

- https://www.flowlauncher.com/docs/#/json-rpc-settings
- https://github.com/Flow-Launcher/Flow.Launcher/blob/v2.1.4/Flow.Launcher.Plugin/Result.cs
- https://github.com/Flow-Launcher/Flow.Launcher/blob/v2.1.4/Flow.Launcher/ResultListBox.xaml
- https://github.com/Flow-Launcher/Flow.Launcher/blob/v2.1.4/Flow.Launcher/MainWindow.xaml

本插件为本地手工安装插件，未提交 Flow 插件商店。
