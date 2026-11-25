# 第6回 解答

## 演習

- STEP 1 のツールの名前：直接登録は `search_materials`、MCP経由は `glossary_search_glossary`
- STEP 2 の [tool call]：`[tool call]   glossary_search_glossary({'query': '3レベル'})`
- STEP 3 の [tool call]：`[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})`
- STEP 4 のツール呼び出し（Codex CLIによる代替実行）：`aws___search_documentation({"search_phrase":"Amazon S3 versioning","limit":2})`

教材の手順ではAWS Knowledgeのツール一覧を取得できた。Geminiで同じ質問を計5回実行したところ、毎回503エラーで、教材の `[tool call]` は取得できなかった。

同じ質問と接続先で、Codex CLI（`gpt-6.2-sol`）からAWS KnowledgeのMCP検索ツールを1回呼んだ。AWSの検索結果に基づき、バージョニングを有効にすると同じキーの旧バージョンが保持され、バージョンIDで以前の内容を取得・復元できると回答した。[AWS公式解説](https://aws.amazon.com/blogs/aws/amazon-s3-enhancement-versioning/)

## 宿題

- 取り組んだレベル：発展（Codex CLI）
- やったこと：2026年11月25日にOpenAIの公式ドキュメントと手元の `codex mcp add --help` を確認し、演習で使った `app/mcp_servers.json` と比較した。
- 結果：

  | 観点 | 演習の学習支援エージェント | Codex CLI |
  |---|---|---|
  | 設定を書く場所 | `app/mcp_servers.json` の `mcpServers` 以下にサーバーを書く | `config.toml` の `[mcp_servers.サーバー名]` に書く。CLIの `codex mcp add` でも登録できる |
  | コマンドで起動 | `command` に実行プログラム、`args` に引数を書く。用語集は `uv run python -m app.mcp_server` で起動した | 同様に `command` と `args` を書く。CLIの登録では `codex mcp add glossary -- uv run python -m app.mcp_server` と指定する |
  | URLで接続 | `url` にAWS Knowledgeの接続先を書く | 同様に `url` を書く。CLIでは `codex mcp add aws --url https://knowledge-mcp.global.api.aws` と指定する |
  | 有効になる範囲 | この設定ファイルを読み込む教材のエージェントに適用される | `~/.codex/config.toml` はユーザー共通。信頼済みのプロジェクトに限定する場合は、そのプロジェクトの `.codex/config.toml` に置く |

  参照：[OpenAI公式ドキュメント「Model Context Protocol」](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

- 気づき・疑問：教材のJSONとCodexのTOMLには、どちらも `command`・`args`・`url` がある。Codexでは、複数のプロジェクトで共通に使うツールと、特定のプロジェクトでだけ使うツールを設定の置き場所で分けられる。
