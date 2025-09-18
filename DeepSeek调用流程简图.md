# DeepSeek API调用流程简图

## 核心调用流程

```mermaid
flowchart TD
    Start([用户输入成语]) --> Init[初始化DeepSeek生成器]
    Init --> Cache{检查缓存}
    Cache -->|存在| ReturnCache[返回缓存故事]
    Cache -->|不存在| BuildPrompt[构建提示词]
    
    BuildPrompt --> CallAPI[调用DeepSeek API]
    CallAPI --> ParseResponse[解析API响应]
    ParseResponse --> Validate[验证故事质量]
    
    Validate -->|通过| SaveCache[保存到缓存]
    Validate -->|失败| Retry{重试次数<3?}
    
    Retry -->|是| Wait[等待退避时间]
    Retry -->|否| Error[抛出错误]
    
    Wait --> CallAPI
    SaveCache --> ReturnStory[返回故事文本]
    ReturnCache --> NextStep[后续处理]
    ReturnStory --> NextStep
    
    NextStep --> SceneExtract[场景提取]
    SceneExtract --> ImageGen[图像生成]
    ImageGen --> AudioGen[音频生成]
    AudioGen --> VideoGen[视频合成]
    VideoGen --> End([输出最终视频])
    
    Error --> End
```

## DeepSeek API调用详情

```mermaid
sequenceDiagram
    participant App as 应用程序
    participant DS as DeepSeek生成器
    participant API as DeepSeek API
    participant Cache as 缓存系统

    App->>DS: generate_story(idiom)
    DS->>Cache: 检查缓存
    Cache-->>DS: 缓存结果
    
    alt 缓存未命中
        DS->>DS: _create_story_prompt()
        Note over DS: 构建包含以下要求的提示词:<br/>- 300字以内<br/>- 丰富场景描述<br/>- 儿童友好语言<br/>- 教育意义
        DS->>API: POST请求
        Note over API: 模型: deepseek-chat<br/>温度: 0.8<br/>最大token: 1000
        API-->>DS: JSON响应
        DS->>DS: _extract_story_from_response()
        DS->>DS: _validate_story()
        
        alt 验证失败
            DS->>DS: 重试机制
            DS->>API: 重新请求
        end
        
        DS->>Cache: 保存缓存
        DS-->>App: 返回故事
    else 缓存命中
        Cache-->>DS: 返回缓存故事
        DS-->>App: 返回故事
    end
```

## 提示词构建过程

```mermaid
graph LR
    A[成语输入] --> B[基础模板]
    B --> C[添加字数限制]
    C --> D[添加场景描述要求]
    D --> E[添加语言风格要求]
    E --> F[添加教育意义要求]
    F --> G[添加视觉描述要求]
    G --> H[最终提示词]
```

## 错误处理流程

```mermaid
graph TD
    A[API调用] --> B{HTTP状态码}
    B -->|200| C[解析JSON]
    B -->|其他| D[网络错误处理]
    
    C --> E{JSON有效?}
    E -->|是| F[提取内容]
    E -->|否| G[JSON解析错误]
    
    F --> H[质量验证]
    H --> I{验证通过?}
    I -->|是| J[成功返回]
    I -->|否| K[质量验证失败]
    
    D --> L{重试次数<3?}
    G --> L
    K --> L
    
    L -->|是| M[指数退避等待]
    L -->|否| N[最终失败]
    
    M --> A
```

## 关键代码调用链

```
main.py:process_single_idiom()
  └── main.py:generate_story_text()
      └── story_generator.py:generate_story()
          ├── _create_story_prompt()
          ├── _call_api()
          ├── _extract_story_from_response()
          └── _validate_story()
```

## API请求参数详解

```json
{
  "model": "deepseek-chat",
  "messages": [
    {
      "role": "user", 
      "content": "请为成语'守株待兔'创作一个适合3-8岁儿童阅读的故事..."
    }
  ],
  "temperature": 0.8,
  "max_tokens": 1000,
  "top_p": 0.9,
  "frequency_penalty": 0.1,
  "presence_penalty": 0.1
}
```

## 响应处理流程

```
API响应 → JSON解析 → 提取choices[0].message.content → 去除首尾空白 → 质量验证 → 返回故事文本
```

## 缓存机制

- **缓存键**: `story_{idiom}_{md5_hash}`
- **存储位置**: `./cache/`
- **文件格式**: `.pkl`
- **生命周期**: 永久存储，手动清理


