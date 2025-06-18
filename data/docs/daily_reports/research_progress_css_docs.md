# 科研进度可视化CSS规范 v1.0

> Modern Research Progress Visualization CSS Standards

## 📋 目录

1. [概述](#概述)
2. [设计原则](#设计原则)
3. [颜色系统](#颜色系统)
4. [排版标准](#排版标准)
5. [组件规范](#组件规范)
6. [布局系统](#布局系统)
7. [交互状态](#交互状态)
8. [使用示例](#使用示例)
9. [最佳实践](#最佳实践)

## 概述

这套CSS规范专为科研进度可视化应用设计，提供了一套完整的视觉设计标准和组件库。规范遵循现代化设计原则，确保界面美观、易用且具有良好的可访问性。

### 特性

- 🎨 现代化的视觉设计
- 📱 响应式布局支持
- 🔧 组件化设计思路
- ⚡ 优雅的动画效果
- 🌈 完整的色彩系统
- ♿ 良好的可访问性

## 设计原则

### 1. 一致性 (Consistency)
- 统一的视觉语言和交互模式
- 标准化的间距、圆角、阴影系统

### 2. 清晰性 (Clarity)
- 清晰的视觉层次
- 易于理解的信息架构

### 3. 效率性 (Efficiency)
- 快速的信息获取
- 直观的操作流程

### 4. 美观性 (Aesthetics)
- 现代化的视觉风格
- 平衡的色彩搭配

## 颜色系统

### CSS 自定义属性

```css
:root {
    /* 主色调 - 温暖中性与石青蓝系 */
    --primary-500: #4a5568;
    --primary-400: #718096;
    --primary-600: #2c3340;
    --primary-700: #1a1f2a;
    
    /* 功能色彩 */
    --success-500: #10b981;
    --warning-500: #f59e0b;
    --error-500: #ef4444;
    --info-500: #06b6d4;
    
    /* 温暖中性色彩系统 */
    --warm-50: #fdfcfa;
    --warm-100: #f8f7f4;
    --warm-200: #e6e2dd;
    --warm-300: #d4cfc6;
    --warm-400: #a39a8c;
    --warm-500: #8b8075;
    --warm-600: #6d655a;
    --warm-700: #524c44;
    --warm-800: #3d3831;
    --warm-900: #2a261f;
    
    /* 石青灰色系 */
    --slate-50: #f8fafc;
    --slate-100: #f1f5f9;
    --slate-200: #e2e8f0;
    --slate-300: #cbd5e1;
    --slate-400: #94a3b8;
    --slate-500: #64748b;
    --slate-600: #475569;
    --slate-700: #334155;
    --slate-800: #1e293b;
    --slate-900: #0f172a;
    
    /* 背景色 */
    --bg-primary: #ffffff;
    --bg-secondary: var(--warm-100);    /* #f8f7f4 */
    --bg-tertiary: var(--warm-200);     /* #e6e2dd */
    --bg-accent: var(--warm-50);
    
    /* 文本色 */
    --text-primary: #3d4451;
    --text-secondary: #5a6474;
    --text-tertiary: var(--slate-400);
    --text-accent: var(--primary-500);
}
```

### 颜色使用指南

**配色理念：温暖中性与石青蓝**
- **温暖中性色调**：营造学术研究的专业感和舒适的阅读体验
- **石青蓝系**：提供现代感和科技感，适合数据可视化
- **高对比度**：确保可读性和可访问性

| 颜色类型 | 用途 | 色值 | 示例应用 |
|---------|------|------|----------|
| `primary` | 主要操作、强调内容 | #4a5568 | 按钮、链接、导航高亮 |
| `success` | 成功状态、完成状态 | #10b981 | 成功提示、已完成任务 |
| `warning` | 警告状态、进行中 | #f59e0b | 待处理任务、注意事项 |
| `error` | 错误状态、失败状态 | #ef4444 | 错误提示、失败任务 |
| `info` | 信息提示、中性状态 | #06b6d4 | 一般信息、提示文本 |
| `warm` | 背景、容器、分隔 | #f8f7f4, #e6e2dd | 页面背景、卡片背景 |

## 排版标准

### 字体规范

```css
/* 引入Noto Sans SC中文字体 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

body {
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, "Segoe UI", 
                 Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    background-color: var(--bg-secondary);
    color: var(--text-primary);
}
```

### 标题层级

```css
.typography-h1 {
    font-size: 2.25rem;    /* 36px */
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: var(--space-lg);
}

.typography-h2 {
    font-size: 1.875rem;   /* 30px */
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: var(--space-md);
}

.typography-h3 {
    font-size: 1.5rem;     /* 24px */
    font-weight: 600;
    line-height: 1.4;
    margin-bottom: var(--space-sm);
}

.typography-body {
    font-size: 1rem;       /* 16px */
    line-height: 1.6;
    color: var(--text-secondary);
}

.typography-caption {
    font-size: 0.875rem;   /* 14px */
    color: var(--text-tertiary);
}
```

## 组件规范

### 1. 卡片组件 (Card)

#### 基础卡片

```css
.card {
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    padding: var(--space-lg);
    transition: all var(--transition-normal);
    border: 1px solid var(--warm-200);
}

.card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}

/* 学术风格卡片变体 */
.card--warm {
    background: var(--bg-tertiary);
    border: 1px solid var(--warm-300);
}

.card--accent {
    background: var(--bg-accent);
    border-left: 4px solid var(--primary-500);
}
```

#### 卡片头部

```css
.card-header {
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 1px solid var(--warm-200);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}

.card-subtitle {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: var(--space-xs);
}
```

#### 使用示例

```html
<!-- 基础学术卡片 -->
<div class="card">
    <div class="card-header">
        <h3 class="card-title">研究进展报告</h3>
        <p class="card-subtitle">2025年6月4日更新</p>
    </div>
    <div class="card-content">
        <!-- 卡片内容 -->
    </div>
</div>

<!-- 温暖色调卡片 -->
<div class="card card--warm">
    <div class="card-header">
        <h3 class="card-title">重点关注项目</h3>
    </div>
    <div class="card-content">
        <!-- 卡片内容 -->
    </div>
</div>

<!-- 强调卡片 -->
<div class="card card--accent">
    <div class="card-header">
        <h3 class="card-title">重要通知</h3>
    </div>
    <div class="card-content">
        <!-- 卡片内容 -->
    </div>
</div>
```

### 2. 按钮组件 (Button)

#### 主要按钮

```css
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-sm) var(--space-lg);
    border-radius: var(--radius-md);
    font-weight: 500;
    font-size: 0.875rem;
    transition: all var(--transition-fast);
    cursor: pointer;
    border: none;
    text-decoration: none;
}

.btn-primary {
    background-color: var(--primary-500);
    color: #ffffff;
}

.btn-primary:hover {
    background-color: var(--primary-600);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

.btn-primary:active {
    transform: translateY(0);
}

/* 温暖色调按钮 */
.btn-warm {
    background-color: var(--warm-600);
    color: #ffffff;
}

.btn-warm:hover {
    background-color: var(--warm-700);
}

/* 次要按钮 */
.btn-secondary {
    background-color: transparent;
    color: var(--primary-500);
    border: 1px solid var(--primary-500);
}

.btn-secondary:hover {
    background-color: var(--primary-500);
    color: #ffffff;
}
```

### 3. 进度条组件 (Progress)

#### 基础样式

```css
.progress-container {
    width: 100%;
    height: 8px;
    background-color: var(--warm-200);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin: var(--space-sm) 0;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-500), var(--primary-400));
    border-radius: var(--radius-lg);
    transition: width var(--transition-slow);
    position: relative;
}

/* 温暖色调进度条变体 */
.progress-bar--warm {
    background: linear-gradient(90deg, var(--warm-600), var(--warm-500));
}

.progress-bar--success {
    background: linear-gradient(90deg, var(--success-500), #34d399);
}

.progress-bar--warning {
    background: linear-gradient(90deg, var(--warning-500), #fbbf24);
}
```

#### 动画效果

```css
.progress-bar::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
```

#### 使用示例

```html
<!-- 标准进度条 -->
<div class="progress-container">
    <div class="progress-bar" style="width: 75%"></div>
</div>

<!-- 温暖色调进度条 -->
<div class="progress-container">
    <div class="progress-bar progress-bar--warm" style="width: 60%"></div>
</div>

<!-- 成功状态进度条 -->
<div class="progress-container">
    <div class="progress-bar progress-bar--success" style="width: 100%"></div>
</div>
```

### 3. 状态徽章 (Status Badge)

#### 基础样式

```css
.status-badge {
    display: inline-flex;
    align-items: center;
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-md);
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
```

#### 状态变体

```css
.status-badge--success {
    background-color: rgba(16, 185, 129, 0.1);
    color: var(--success-500);
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.status-badge--warning {
    background-color: rgba(245, 158, 11, 0.1);
    color: var(--warning-500);
    border: 1px solid rgba(245, 158, 11, 0.2);
}

.status-badge--error {
    background-color: rgba(239, 68, 68, 0.1);
    color: var(--error-500);
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.status-badge--info {
    background-color: rgba(6, 182, 212, 0.1);
    color: var(--info-500);
    border: 1px solid rgba(6, 182, 212, 0.2);
}
```

#### 使用示例

```html
<span class="status-badge status-badge--success">已完成</span>
<span class="status-badge status-badge--warning">进行中</span>
<span class="status-badge status-badge--error">失败</span>
<span class="status-badge status-badge--info">计划中</span>
```

### 5. 导航组件 (Navigation)

```css
/* 顶部导航栏 */
.navbar {
    background-color: rgba(248, 247, 244, 0.8);
    backdrop-filter: blur(12px);
    position: sticky;
    top: 0;
    z-index: 50;
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-normal);
}

.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-sm) var(--space-lg);
}

.navbar-brand {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-accent);
    text-decoration: none;
}

.navbar-nav {
    display: flex;
    gap: var(--space-xl);
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    padding-bottom: var(--space-xs);
    border-bottom: 2px solid transparent;
    transition: all var(--transition-fast);
}

.nav-link:hover,
.nav-link.active {
    color: var(--primary-600);
    border-bottom-color: var(--primary-600);
}

/* 移动端导航 */
.mobile-menu {
    display: none;
    flex-direction: column;
    padding: var(--space-md) var(--space-lg);
    background-color: var(--bg-secondary);
    border-top: 1px solid var(--warm-200);
}

.mobile-menu .nav-link {
    display: block;
    padding: var(--space-sm) 0;
    text-align: center;
    border-bottom: none;
}

@media (max-width: 768px) {
    .navbar-nav {
        display: none;
    }
    
    .mobile-menu.show {
        display: flex;
    }
}
```

#### 使用示例

```html
<nav class="navbar">
    <div class="navbar-container">
        <a href="#" class="navbar-brand">科研进度仪表板</a>
        <ul class="navbar-nav">
            <li><a href="#overview" class="nav-link active">概览</a></li>
            <li><a href="#tasks" class="nav-link">任务</a></li>
            <li><a href="#progress" class="nav-link">进度</a></li>
            <li><a href="#reports" class="nav-link">报告</a></li>
        </ul>
        <button class="mobile-menu-button md:hidden">☰</button>
    </div>
    <div class="mobile-menu">
        <a href="#overview" class="nav-link">概览</a>
        <a href="#tasks" class="nav-link">任务</a>
        <a href="#progress" class="nav-link">进度</a>
        <a href="#reports" class="nav-link">报告</a>
    </div>
</nav>
```

```css
.stat-item {
    text-align: center;
    padding: var(--space-md);
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-600);
    display: block;
}

.stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: var(--space-xs);
}

.stat-change {
    font-size: 0.75rem;
    margin-top: var(--space-xs);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-xs);
}

.stat-change--positive {
    color: var(--success-500);
}

.stat-change--negative {
    color: var(--error-500);
}
### 6. 统计数据组件 (Statistics)

```css
.stat-item {
    text-align: center;
    padding: var(--space-md);
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-600);
    display: block;
}

.stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: var(--space-xs);
}

.stat-change {
    font-size: 0.75rem;
    margin-top: var(--space-xs);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-xs);
}

.stat-change--positive {
    color: var(--success-500);
}

.stat-change--negative {
    color: var(--error-500);
}

/* 学术风格统计卡片 */
.stat-card {
    background: var(--bg-primary);
    border: 1px solid var(--warm-200);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    text-align: center;
    transition: all var(--transition-normal);
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary-400);
}

.stat-card .stat-value {
    color: var(--primary-500);
    font-size: 2.5rem;
    margin-bottom: var(--space-sm);
}
```

#### 使用示例

```html
<!-- 基础统计项 -->
<div class="stat-item">
    <span class="stat-value">24</span>
    <span class="stat-label">已完成任务</span>
    <div class="stat-change stat-change--positive">
        ↗ +12% 比上周
    </div>
</div>

<!-- 统计卡片 -->
<div class="stat-card">
    <div class="stat-value">8.5h</div>
    <div class="stat-label">平均每日研究时间</div>
    <div class="stat-change stat-change--positive">
        ↗ +0.8h 比上周
    </div>
</div>
```

## 布局系统

### 网格系统

```css
.grid {
    display: grid;
    gap: var(--space-lg);
}

.grid--1 { grid-template-columns: 1fr; }
.grid--2 { grid-template-columns: repeat(2, 1fr); }
.grid--3 { grid-template-columns: repeat(3, 1fr); }
.grid--4 { grid-template-columns: repeat(4, 1fr); }

@media (max-width: 768px) {
    .grid--2, .grid--3, .grid--4 {
        grid-template-columns: 1fr;
    }
}
```

### 容器系统

```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--space-xl);
}

.section {
    margin-bottom: var(--space-2xl);
}
```

### 间距系统

```css
:root {
    --space-xs: 0.5rem;    /* 8px */
    --space-sm: 0.75rem;   /* 12px */
    --space-md: 1rem;      /* 16px */
    --space-lg: 1.5rem;    /* 24px */
    --space-xl: 2rem;      /* 32px */
    --space-2xl: 3rem;     /* 48px */
}
```

## 交互状态

### 基础交互

```css
.interactive {
    cursor: pointer;
    transition: all var(--transition-fast);
}

.interactive:hover {
    transform: translateY(-1px);
}

.interactive:active {
    transform: translateY(0);
}
```

### 过渡动画

```css
:root {
    --transition-fast: 150ms ease-in-out;
    --transition-normal: 250ms ease-in-out;
    --transition-slow: 350ms ease-in-out;
}
```

### 阴影系统

```css
:root {
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
                 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 
                 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 
                 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
```

## 使用示例

### 完整的科研进度卡片

```html
<div class="card">
    <div class="card-header">
        <h3 class="card-title">今日任务进度</h3>
        <p class="card-subtitle">2025年6月4日 - 周三</p>
    </div>
    
    <div class="task-item">
        <div class="task-info">
            <h4>文献阅读 - 机器学习算法</h4>
            <div class="task-meta">
                <span class="status-badge status-badge--success">已完成</span>
                <span class="typography-caption">3小时</span>
            </div>
        </div>
    </div>

    <div class="task-item">
        <div class="task-info">
            <h4>实验数据分析</h4>
            <div class="progress-container">
                <div class="progress-bar" style="width: 75%"></div>
            </div>
            <div class="task-meta">
                <span class="status-badge status-badge--warning">进行中</span>
                <span class="typography-caption">75% 完成</span>
            </div>
        </div>
    </div>
</div>
```

### 统计概览面板

```html
<div class="grid grid--4">
    <div class="card stat-item">
        <span class="stat-value">24</span>
        <span class="stat-label">已完成任务</span>
        <div class="stat-change stat-change--positive">
            ↗ +12% 比上周
        </div>
    </div>
    <!-- 更多统计项... -->
</div>
```

## 最佳实践

### 1. 颜色使用
- 优先使用CSS自定义属性
- 保持色彩的语义化使用
- 确保足够的对比度
- **温暖色调指南**：在学术和研究环境中，温暖的中性色调能营造专业而舒适的阅读体验

### 2. 学术风格设计原则
- **可读性优先**：使用Noto Sans SC确保中文内容的最佳显示效果
- **层次清晰**：通过色彩深浅和间距营造清晰的信息层次
- **温馨专业**：温暖色调与现代设计相结合，适合长时间使用

### 3. 间距规范
- 使用标准化的间距变量
- 保持一致的视觉节奏
- 避免随意的边距设置

### 4. 动画效果
- 使用统一的过渡时间
- 避免过度的动画效果
- 确保动画的性能优化

### 5. 响应式设计
- 移动端优先的设计思路
- 合理的断点设置
- 灵活的网格系统

### 6. 可访问性
- 保证足够的色彩对比度（特别注意温暖色调的对比度）
- 提供语义化的HTML结构
- 支持键盘导航

### 7. 性能优化
- 避免复杂的CSS选择器
- 优化动画性能
- 合理使用GPU加速

### 8. 中文界面优化
- 使用Noto Sans SC保证中文字体的最佳渲染
- 考虑中文文本的行高和字间距
- 为中文内容预留足够的空间

## 扩展指南

### 主题定制

可以通过修改CSS自定义属性来定制主题：

```css
:root {
    /* 自定义主色调 */
    --primary-500: #8b5cf6;  /* 紫色主题 */
    --primary-400: #a78bfa;
    --primary-600: #7c3aed;
    
    /* 自定义圆角 */
    --radius-lg: 1rem;       /* 更圆润的设计 */
}
```

### 新组件开发

遵循以下原则开发新组件：

1. 使用现有的设计系统变量
2. 保持命名的一致性
3. 提供hover和active状态
4. 确保响应式兼容性
5. 添加适当的过渡动画

---

**版本**: v1.0  
**最后更新**: 2025年6月4日  
**维护者**: 科研效率工具团队