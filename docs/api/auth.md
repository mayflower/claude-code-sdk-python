# Authentication

The Claude Code SDK supports multiple authentication methods, which are handled by the `AuthProvider` class and the `AuthType` enum.

## AuthType Enum

The `AuthType` enum defines the available authentication types:

```python
from claude_code import AuthType

# Authentication with direct Anthropic API
auth_type = AuthType.ANTHROPIC_API

# Authentication with AWS Bedrock
auth_type = AuthType.AWS_BEDROCK

# Authentication with Google Vertex AI
auth_type = AuthType.GOOGLE_VERTEX
```

## Authentication Details

### Anthropic API

When using `AuthType.ANTHROPIC_API`, you need to provide an API key:

```python
from claude_code import ClaudeCode, AuthType

claude = ClaudeCode(
    auth_type=AuthType.ANTHROPIC_API,
    api_key="your-api-key"
)
```

You can also set the API key in the environment:

```bash
export ANTHROPIC_API_KEY=your-api-key
```

```python
from claude_code import ClaudeCode, AuthType

# Will use API key from environment
claude = ClaudeCode(auth_type=AuthType.ANTHROPIC_API)
```

### AWS Bedrock

When using `AuthType.AWS_BEDROCK`, you need to provide an AWS region:

```python
from claude_code import ClaudeCode, AuthType

claude = ClaudeCode(
    auth_type=AuthType.AWS_BEDROCK,
    region="us-west-2",
    model="anthropic.claude-3-7-sonnet-20250219-v1:0"
)
```

> **Note**: AWS credentials are taken from the environment or AWS configuration files.

### Google Vertex AI

When using `AuthType.GOOGLE_VERTEX`, you need to provide a region and project ID:

```python
from claude_code import ClaudeCode, AuthType

claude = ClaudeCode(
    auth_type=AuthType.GOOGLE_VERTEX,
    region="us-central1",
    project_id="your-project-id",
    model="claude-3-7-sonnet@20250219"
)
```

> **Note**: Google Cloud credentials are taken from the environment or Google Cloud configuration files.

## Model Formats

When specifying the model parameter, use the format appropriate for the authentication type:

| Auth Type | Model Format | Example |
|-----------|--------------|---------|
| `ANTHROPIC_API` | `{model}-{version}` | `claude-3-7-sonnet-20250219` |
| `AWS_BEDROCK` | `anthropic.{model}-{version}:{revision}` | `anthropic.claude-3-7-sonnet-20250219-v1:0` |
| `GOOGLE_VERTEX` | `{model}@{version}` | `claude-3-7-sonnet@20250219` |

## Environment Variables

The SDK recognizes the following environment variables:

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `AWS_REGION` | AWS region |
| `CLOUD_ML_REGION` | Google Cloud region |
| `ANTHROPIC_VERTEX_PROJECT_ID` | Google Cloud project ID |
| `ANTHROPIC_MODEL` | Model ID |

These environment variables will be used if the corresponding parameters are not provided.