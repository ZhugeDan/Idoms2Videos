# 成语故事短视频生成系统 - DeepSeek调用流程图

## 整体流程图

```mermaid
graph TD
    A[用户输入成语] --> B[初始化DeepSeek故事生成器]
    B --> C[检查缓存]
    C --> D{缓存存在?}
    D -->|是| E[返回缓存故事]
    D -->|否| F[创建故事生成提示词]
    F --> G[调用DeepSeek API]
    G --> H[API响应处理]
    H --> I[提取故事文本]
    I --> J[验证故事质量]
    J --> K{验证通过?}
    K -->|否| L[重试机制]
    L --> G
    K -->|是| M[保存到缓存]
    M --> N[返回故事文本]
    E --> O[场景提取]
    N --> O
    O --> P[生成插画]
    P --> Q[生成音频]
    Q --> R[合成视频]
    R --> S[输出最终视频]
```

## 详细调用流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant M as 主程序
    participant D as DeepSeek生成器
    participant C as 缓存管理器
    participant API as DeepSeek API
    participant S as 场景提取器
    participant I as 图像生成器
    participant A as 音频生成器
    participant V as 视频合成器

    U->>M: 输入成语
    M->>D: 初始化故事生成器
    M->>C: 检查缓存
    C-->>M: 缓存结果
    
    alt 缓存不存在
        M->>D: generate_story(idiom)
        D->>D: _create_story_prompt(idiom)
        D->>API: POST /v1/chat/completions
        Note over API: 模型: deepseek-chat<br/>温度: 0.8<br/>最大token: 1000
        API-->>D: 返回JSON响应
        D->>D: _extract_story_from_response()
        D->>D: _validate_story()
        
        alt 验证失败
            D->>D: 重试机制(最多3次)
            D->>API: 重新调用API
        end
        
        D-->>M: 返回故事文本
        M->>C: 保存到缓存
    else 缓存存在
        C-->>M: 返回缓存故事
    end
    
    M->>S: extract_scenes_from_story()
    S-->>M: 返回场景列表
    M->>I: generate_story_images()
    I-->>M: 返回图片列表
    M->>A: generate_story_audio()
    A-->>M: 返回音频文件
    M->>V: create_video()
    V-->>M: 返回视频文件
    M-->>U: 显示最终结果
```

## DeepSeek API调用详情

```mermaid
graph LR
    A[成语输入] --> B[构建提示词]
    B --> C[API请求参数]
    C --> D[HTTP POST请求]
    D --> E[DeepSeek API]
    E --> F[JSON响应]
    F --> G[提取故事内容]
    G --> H[质量验证]
    H --> I{验证结果}
    I -->|通过| J[返回故事]
    I -->|失败| K[重试/错误处理]
    K --> D
```

## 提示词构建流程

```mermaid
graph TD
    A[输入成语] --> B[构建基础提示词]
    B --> C[添加故事要求]
    C --> D[添加场景描述要求]
    D --> E[添加教育意义要求]
    E --> F[添加语言要求]
    F --> G[最终提示词]
    G --> H[发送给DeepSeek API]
```

## 错误处理和重试机制

```mermaid
graph TD
    A[API调用] --> B{请求成功?}
    B -->|是| C[解析响应]
    B -->|否| D[记录错误]
    C --> E{解析成功?}
    E -->|是| F[验证故事质量]
    E -->|否| G[记录解析错误]
    F --> H{质量验证通过?}
    H -->|是| I[返回故事]
    H -->|否| J[记录质量错误]
    D --> K{重试次数<3?}
    G --> K
    J --> K
    K -->|是| L[等待指数退避时间]
    L --> M[重新调用API]
    M --> A
    K -->|否| N[抛出最终错误]
```

## 缓存机制

```mermaid
graph TD
    A[请求故事] --> B[生成缓存键]
    B --> C[检查缓存文件]
    C --> D{缓存存在?}
    D -->|是| E[读取缓存内容]
    D -->|否| F[调用DeepSeek API]
    E --> G[返回缓存故事]
    F --> H[生成新故事]
    H --> I[保存到缓存]
    I --> J[返回新故事]
```

## 技术参数配置

### DeepSeek API参数
- **模型**: `deepseek-chat`
- **温度**: `0.8` (控制创造性)
- **最大Token**: `1000`
- **Top-p**: `0.9` (核采样)
- **频率惩罚**: `0.1`
- **存在惩罚**: `0.1`
- **超时时间**: `30秒`

### 重试机制
- **最大重试次数**: `3次`
- **退避策略**: 指数退避 (2^attempt秒)
- **错误类型**: 网络错误、JSON解析错误、质量验证失败

### 缓存策略
- **缓存键格式**: `story_{idiom}_{hash}`
- **缓存位置**: `./cache/`
- **缓存格式**: Pickle文件
- **缓存有效期**: 永久（手动清理）

## 故事质量验证标准

1. **长度检查**: 不超过500字
2. **内容检查**: 包含基本故事元素
3. **结构检查**: 有明确的开始、发展、结尾
4. **语言检查**: 符合儿童阅读水平
5. **场景检查**: 包含丰富的视觉描述

## 输出格式

- **故事文本**: 纯文本格式
- **场景列表**: JSON数组格式
- **图片文件**: JPG格式，保存在`output_pic/`
- **音频文件**: MP3格式
- **视频文件**: MP4格式，保存在`output/`


