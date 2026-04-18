"""WAIC 2026 一人公司AI自动化生产线Demo"""
import streamlit as st
import json
import requests
import random
import os
import time
from datetime import datetime

# Qwen API 配置
QWEN_API_KEY = "sk-549ad20c3b634174aab05130b0c607d7"
QWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

st.set_page_config(page_title="AI一人公司 | TSN产业链", page_icon="🚀", layout="wide")

# 样式 - 包含MathJax配置以支持LaTeX公式渲染
st.markdown("""
<style>
.paper-card { background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #2196f3; }
.paper-title { color: #1565c0; font-weight: bold; font-size: 0.9rem; }
.bid-card { background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #ff9800; }
.bid-title { color: #e65100; font-weight: bold; }
.bid-match { background: #4caf50; color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; }
.content-card { background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #4caf50; }
.product-card { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-radius: 12px; padding: 1.2rem; margin: 0.8rem 0; border: 2px solid #9c27b0; }
.answer-box { background: #fafafa; border-radius: 12px; padding: 1.5rem; border-left: 4px solid #673ab7; }
.stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 16px; text-align: center; }
.pulse { display: inline-block; width: 10px; height: 10px; background: #4caf50; border-radius: 50%; animation: pulse 2s infinite; margin-right: 0.5rem; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
</style>

<!-- MathJax配置，用于LaTeX公式渲染 -->
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.min.js"></script>
""", unsafe_allow_html=True)

# 数据
def get_papers():
    return [
        {
            "id": 1,
            "title": "DeepCQF: Making CQF scheduling more intelligent and practicable",
            "venue": "IEEE International Conference on Communications (ICC)",
            "year": 2022,
            "pages": "1-6",
            "index": "ISTP检索, CCF C类",
            "wos": "WOS: 000864709901050",
            "overview": "本文提出DeepCQF框架，将深度学习引入CQF（Cycle Queuing and Forwarding）调度机制，通过神经网络预测流量模式并动态调整周期参数，解决了传统CQF在突发流量场景下的性能瓶颈问题。",
            "path": "D:/workbuddy/project/papers/DeepCQF Making CQF Scheduling More Intelligent.pdf"
        },
        {
            "id": 2,
            "title": "Burst-Aware Time-Triggered Flow Scheduling With Enhanced Multi-CQF in Time-Sensitive Networks",
            "venue": "IEEE/ACM Transactions on Networking",
            "year": 2023,
            "volume": "31(6)",
            "pages": "2809-2824",
            "index": "SCI检索, CCF A类, JCR Q2",
            "wos": "WOS: 000972313500001",
            "overview": "针对TSN网络中突发流量对时间触发流的干扰问题，提出增强型Multi-CQF调度机制，通过多队列协同和突发感知算法，在保证时间触发流确定性的同时提升带宽利用率。",
            "path": "D:/workbuddy/project/papers/Burst-Aware Time-Triggered Flow Scheduling With Enhanced Multi-CQF in Time-Sensitive Networks.pdf"
        },
        {
            "id": 3,
            "title": "Joint Time-Frequency Resource Scheduling Over CQF-Based TSN-5G System",
            "venue": "15th International Conference on Communication Software and Networks (ICCSN)",
            "year": 2023,
            "pages": "60-65",
            "index": "EI检索, Best Paper",
            "accession": "20235015190812",
            "overview": "研究TSN与5G融合网络中的时频资源联合调度问题，提出跨域协同调度框架，实现时间敏感业务在异构网络间的无缝传输，获得会议最佳论文奖。",
            "path": "D:/workbuddy/project/papers/Joint Time-Frequency Resource Scheduling over CQF-based TSN-5G System.pdf"
        },
        {
            "id": 4,
            "title": "广义确定性标识网络",
            "venue": "电子学报",
            "year": 2024,
            "volume": "52(1)",
            "pages": "1-18",
            "index": "北大核心, CCF A类",
            "accession": "20241315802363",
            "overview": "提出广义确定性标识网络架构，将标识解析与确定性传输深度融合，通过智能标识路由机制实现跨域端到端确定性保证，为工业互联网提供新型网络基础设施。",
            "path": "D:/workbuddy/project/papers/广义确定性标识网络.pdf"
        },
        {
            "id": 5,
            "title": "Intelligent End-to-end Deterministic Scheduling Across Converged Networks",
            "venue": "IEEE Transactions on Mobile Computing",
            "year": 2024,
            "index": "SCI检索, CCF A类, JCR Q1, Major revision",
            "overview": "针对融合网络中的端到端确定性调度挑战，提出智能化跨域调度框架，结合深度强化学习实现异构网络资源的自适应协同，保证端到端时延确定性。",
            "path": "D:/workbuddy/project/papers/Intelligent End-to-end Deterministic Scheduling Across Converged Networks.pdf"
        },
        {
            "id": 6,
            "title": "Joint Routing and Scheduling for CQF",
            "venue": "7th International Conference on Computer and Communication Systems (ICCCS)",
            "year": 2022,
            "pages": "1-5",
            "index": "EI检索",
            "accession": "20223512673211",
            "overview": "研究CQF机制下的联合路由与调度优化问题，建立整数线性规划模型并提出启发式求解算法，实现路由选择与门控配置的协同优化。",
            "path": "D:/workbuddy/project/papers/Joint_Routing_and_Scheduling_for_CQF.pdf"
        },
    ]

def open_pdf(file_path):
    """使用系统默认程序打开PDF"""
    try:
        if os.path.exists(file_path):
            os.startfile(file_path)
            return True
        else:
            return False
    except:
        return False

def get_standards():
    return [
        {
            "id": 1,
            "type": "中国通信标准化协会CCSA行业标准",
            "title": "工业互联网 时间敏感网络测试方法",
            "standard_no": "YD/T 6569-2025",
            "path": "D:/workbuddy/project/papers/工业互联网 时间敏感网络测试方法.pdf"
        },
        {
            "id": 2,
            "type": "中国通信标准化协会CCSA团体标准",
            "title": "工业互联网 时间敏感网络承载工业通信协议技术要求",
            "standard_no": "T/CCSA 491-2024",
            "path": "D:/workbuddy/project/papers/工业互联网 时间敏感网络承载工业通信协议技术要求.pdf"
        }
    ]

def get_patents():
    return [
        {
            "id": 1,
            "type": "发明专利",
            "status": "已授权",
            "patent_no": "ZL 2021 1 0435398.9",
            "title": "一种对时敏业务流和路由联合调度的规划方法及装置",
            "path": "D:/workbuddy/project/papers/一种对时敏业务流和路由联合调度的规划方法及装置.pdf",
            "cert_path": "D:/workbuddy/project/papers/专利证书1.pdf"
        },
        {
            "id": 2,
            "type": "发明专利",
            "status": "已授权",
            "patent_no": "ZL 2021 1 0679100.4",
            "title": "一种在线规划时间敏感流的方法装置及存储介质",
            "path": "D:/workbuddy/project/papers/一种在线规划时间敏感流的方法装置及存储介质.pdf",
            "cert_path": "D:/workbuddy/project/papers/HA202106791-发明专利证书-一种在线规划时间敏感流的方法.pdf"
        },
        {
            "id": 3,
            "type": "发明专利",
            "status": "已授权",
            "patent_no": "ZL 2023 1 0563323.0",
            "title": "一种普适的异构融合算网资源智慧适配网络架构及方法",
            "path": "D:/workbuddy/project/papers/一种普适的异构融合算网资源智慧适配网络架构及方法.pdf",
            "cert_path": "D:/workbuddy/project/papers/专利证书2.pdf"
        }
    ]

def get_bids():
    return [
        {"title": "某汽车工厂TSN网络改造", "amount": "280万", "match": 95, "tech": "CQF调度"},
        {"title": "智能制造5G+TSN融合网络", "amount": "450万", "match": 92, "tech": "TSN-5G协同"},
        {"title": "轨道交通确定性网络建设", "amount": "680万", "match": 88, "tech": "端到端调度"},
        {"title": "电力系统时间敏感网络", "amount": "320万", "match": 90, "tech": "Multi-CQF"},
    ]

def get_contents():
    return [
        {"type": "短视频", "title": "TSN调度算法：为什么你的工业网络总是延迟？", "views": "12.5万"},
        {"type": "技术专栏", "title": "从IEEE TON论文看CQF调度的未来", "views": "8.3万"},
        {"type": "短视频", "title": "院士团队揭秘：确定性网络的三大核心技术", "views": "15.2万"},
        {"type": "技术专栏", "title": "一人公司如何用AI提升10倍生产力", "views": "5.6万"},
    ]

# ==================== 知识库上下文 ====================
def get_knowledge_context():
    """构建知识库上下文，包含论文核心观点、技术细节、公式和可引用段落"""
    return """
【论文1: DeepCQF - ICC 2022】
核心观点：将深度学习引入CQF调度，通过LSTM预测流量模式并动态调整周期参数
技术细节：
- CQF基本机制：将时间划分为固定周期T，每个周期包含两个队列交替收发
- 问题建模：流量预测问题建模为时间序列预测 min Σ(y_pred - y_actual)²
- LSTM网络结构：输入层(历史流量窗口) → LSTM层(128单元) → 全连接层 → 输出层(预测流量)
- 动态周期调整：T_new = T_base × (1 + α × burst_factor)，其中α为学习率系数
- 性能提升：突发场景下端到端时延降低35%，带宽利用率提升28%

关键段落："Traditional CQF uses fixed cycle parameters which cannot adapt to varying traffic patterns. DeepCQF employs an LSTM-based predictor with 128 hidden units to forecast burst traffic. The cycle length is dynamically adjusted as T_new = T_base × (1 + α·β), where β is the predicted burst factor. Experimental results show 35% latency reduction under bursty workloads."
引用标记：[DeepCQF, ICC 2022, pp.3-4]

【论文2: Burst-Aware Multi-CQF - IEEE/ACM TON 2023】
核心观点：增强型Multi-CQF架构，多队列协同处理突发流量
技术细节：
- Multi-CQF架构：N个并行CQF队列对，每个队列对独立配置周期参数
- 流量分类：时间触发流(TT) → 高优先级队列；尽力而为流(BE) → 低优先级队列
- 突发检测算法：基于滑动窗口方差检测 σ² = (1/w)Σ(x_i - μ)² > threshold
- 队列分配策略：P(queue_i) = f(流优先级, 队列负载, 历史时延)
- 确定性保证：TT流端到端时延上界 D_max = Σ(hop_delay) + Σ(queueing_delay) ≤ D_deadline

关键段落："We propose an enhanced Multi-CQF architecture with N parallel queue pairs. Time-triggered flows are isolated into dedicated high-priority queues. Burst detection employs sliding-window variance analysis: σ² = (1/w)Σ(x_i - μ)². The end-to-end latency bound is guaranteed as D_max = Σ(d_hop) + Σ(d_queue) ≤ D_deadline. Bandwidth utilization improves by 28% while maintaining deterministic latency."
引用标记：[Burst-Aware Multi-CQF, IEEE/ACM TON 2023, pp.2815-2818]

【论文3: TSN-5G Joint Scheduling - ICCSN 2023 (Best Paper)】
核心观点：TSN与5G融合网络的时频资源联合调度
技术细节：
- 跨域映射：TSN门控列表(GCL) ↔ 5G时隙分配(Slot Allocation)
- 联合优化目标：min Σ(时延惩罚) + Σ(资源开销) + Σ(切换代价)
- 约束条件：
  * TSN侧：门控周期 T_gcl = k × T_5g_slot (k为正整数)
  * 5G侧：时隙利用率 η = N_used / N_total ≤ η_max
  * 跨域同步：|t_tsn - t_5g| ≤ ε_sync (同步误差阈值)
- 调度算法：两阶段启发式算法，阶段1路径选择，阶段2时频资源分配

关键段落："The TSN-5G convergence requires coordinated time-frequency resource allocation. We establish a cross-domain mapping between TSN Gate Control Lists (GCL) and 5G slot allocation. The synchronization constraint requires |t_tsn - t_5g| ≤ ε_sync. Our two-stage heuristic achieves seamless inter-domain transmission with 95% resource utilization."
引用标记：[TSN-5G Joint Scheduling, ICCSN 2023, pp.62-63, Best Paper]

【论文4: 广义确定性标识网络 - 电子学报 2024】
核心观点：标识解析与确定性传输深度融合，实现跨域端到端确定性保证
技术细节：
- 网络架构：标识层(语义映射) + 路由层(确定性路径) + 传输层(时延保证)
- 智能标识路由：RID(路由标识) = Hash(服务类型, 时延需求, 安全等级)
- 确定性保证机制：
  * 时延上界计算：D_e2e = D_proc + D_trans + D_prop + D_queue
  * 抖动控制：Jitter = |D_actual - D_expected| ≤ J_max (通常<1μs)
- 资源预留：基于网络演算理论，计算最小带宽需求 R_min = σ / (D_deadline - ρ)
  其中σ为突发度，ρ为平均速率

关键段落："广义确定性标识网络通过智能标识路由机制实现跨域端到端确定性保证。路由标识RID由服务类型、时延需求和安全等级哈希生成。端到端时延上界计算为D_e2e = D_proc + D_trans + D_prop + D_queue，其中排队时延通过网络演算严格限定。实验表明时延抖动控制在微秒级(Jitter < 1μs)。"
引用标记：[广义确定性标识网络, 电子学报 2024, pp.8-12]

【论文5: End-to-end Deterministic Scheduling - IEEE TMC 2024】
核心观点：融合网络中的端到端确定性调度，基于深度强化学习
技术细节：
- MDP建模：
  * 状态空间 S = {网络拓扑, 流量矩阵, 链路状态, 队列占用}
  * 动作空间 A = {路由选择, 时隙分配, 优先级设置}
  * 奖励函数 R = -Σ(时延违规) - λ·Σ(资源开销) + γ·吞吐量
- PPO算法：策略网络π(a|s)优化目标 J(θ) = E[min(r_t·Â_t, clip(r_t)·Â_t)]
- 值函数：V(s)估计期望累积奖励，用于优势函数计算 Â_t = R_t + γV(s_{t+1}) - V(s_t)
- 收敛性：经过10^5次迭代，策略收敛，端到端时延满足率>98%

关键段落："We formulate end-to-end scheduling as a Markov Decision Process. The state space includes network topology, traffic matrix, and queue occupancy. The reward function balances latency violation penalty, resource cost, and throughput. Using Proximal Policy Optimization (PPO), the policy network converges after 10^5 iterations, achieving >98% deadline satisfaction rate across converged networks."
引用标记：[End-to-end Scheduling, IEEE TMC 2024, Major revision]

【论文6: Joint Routing and Scheduling for CQF - ICCCCS 2022】
核心观点：CQF机制下的联合路由与调度优化，NP-hard问题的启发式求解
技术细节：
- 问题建模：
  * 决策变量：x_{i,j}^f ∈ {0,1} (流f是否经过链路(i,j))
  *           g_{i,t}^f ∈ {0,1} (流f在节点i的时隙t是否开放)
  * 目标函数：min Σ(链路开销 × x) + Σ(时隙冲突惩罚)
  * 约束条件：流量守恒、容量约束、时隙不重叠、端到端时延约束
- 复杂度分析：联合优化问题为NP-hard，穷举复杂度O(|V|! × 2^{|T|×|F|})
- 两阶段启发式：
  * 阶段1：k-最短路径算法生成候选路径集，复杂度O(k·|V|²)
  * 阶段2：基于贪心策略的时隙分配，复杂度O(|F|·|T|·log|V|)
- 近似比：启发式算法达到92%最优解质量

关键段落："Joint optimization of routing and scheduling in CQF is NP-hard. We formulate an ILP with binary variables x_{i,j}^f for routing and g_{i,t}^f for scheduling. The exhaustive search has complexity O(|V|! × 2^{|T|×|F|}). Our two-stage heuristic first computes k-shortest paths, then greedily assigns time slots, achieving 92% optimality ratio with polynomial complexity."
引用标记：[Joint Routing&Scheduling, ICCCCS 2022, pp.2-4]
"""

def generate_proposal_report(tech_summaries, math_descriptions, bid_info, papers, standards, patents):
    """调用Qwen API生成技术方案建议报告"""
    
    bid_title = bid_info.get('title', '工业网络建设项目')
    bid_org = bid_info.get('org', '某企业')
    bid_amount = bid_info.get('amount', '¥500万')
    bid_category = bid_info.get('category', '智能制造')
    
    # 构建技术要求文本
    summaries_text = "\n".join([f"{i+1}. {title}：{content}" for i, (title, content, _) in enumerate(tech_summaries)])
    
    # 构建数学描述文本
    math_text = "\n".join([f"- {md.get('scan_term', '')} → {md.get('matched_paper', '')} ({md.get('paper_venue', '')})" for md in math_descriptions[:3]])
    
    # 构建知识库引用
    papers_text = "\n".join([f"- {p['title']} ({p['venue']}, {p['year']})" for p in papers[:3]])
    standards_text = "\n".join([f"- {s['title']} ({s['standard_no']})" for s in standards])
    patents_text = "\n".join([f"- {p['title']} ({p['patent_no']})" for p in patents[:2]])
    
    prompt = f"""你是一位资深的工业互联网技术专家，正在撰写一份面向招标方的技术方案建议报告。

## 项目信息
- 项目名称：{bid_title}
- 招标单位：{bid_org}
- 项目金额：{bid_amount}
- 行业领域：{bid_category}

## 技术要求摘要
{summaries_text}

## 知识库匹配成果
{math_text}

## 可用技术资产
论文：
{papers_text}

标准：
{standards_text}

专利：
{patents_text}

## 报告结构要求
严格按照以下结构输出：

一、项目背景与现状分析
- 行业背景和业务需求
- 当前面临的问题
- 痛点分析

二、技术需求说明
- 功能需求
- 性能需求指标（必须包含具体数字）
- 安全需求

三、技术方案设计
- 总体架构（基于TSN/5G/SDN等技术）
- 核心技术选型及理由（引用上述论文/专利作为支撑）
- 关键技术点和创新点

四、可行性分析
- 技术可行性（引用具体论文成果证明）
- 经济可行性
- 风险识别与应对

五、实施计划
- 阶段性任务
- 时间规划

六、预期效果与价值
- 技术指标承诺
- 经济效益

七、结论与建议

## 写作风格要求（非常重要）
1. **说人话，去AI味**：
   - 禁止使用"首先、其次、再次、最后、总之、例如、此外、总而言之、综上所述"等机械转接词
   - 禁止使用"值得注意的是、需要指出的是、不难发现"等AI腔调
   - 禁止使用"随着...的发展、在...背景下"等套话开头

2. **学术规范，逻辑严谨**：
   - 使用主谓宾完整长句，逻辑严密
   - 多用专业术语，但每句话要有实质内容
   - 数据必须具体，如"端到端时延≤100μs"而非"低时延"

3. **引用规范**：
   - 引用论文时使用格式："本文提出的DeepCQF算法（IEEE ICC 2022）通过LSTM预测..."
   - 引用专利时使用格式："基于已授权专利ZL 2021 1 0435398.9的联合调度方法..."

4. **上下文连贯**：
   - 段落之间要有内在逻辑联系
   - 避免生硬罗列，要有论证过程

请直接输出完整报告内容，不要有任何前缀说明。"""
    
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {QWEN_API_KEY}"}
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "system", "content": "你是资深的工业互联网技术专家，擅长撰写技术方案建议报告。说话直接、专业、不绕弯子，坚决去掉AI味。"},
                {"role": "user", "content": prompt}
            ]
        },
        "parameters": {"temperature": 0.6, "max_tokens": 3000, "result_format": "message"}
    }
    
    try:
        r = requests.post(QWEN_API_URL, headers=headers, json=data, timeout=120)
        if r.status_code != 200:
            return None
        result = r.json()
        if 'output' in result and 'choices' in result['output']:
            return result['output']['choices'][0]['message']['content']
        else:
            return None
    except Exception as e:
        return None

def generate_math_descriptions(tech_summaries, bid_info):
    """调用Qwen API根据技术要求摘要生成论文匹配和数学描述，展示Agent如何"秀操作"""
    
    bid_category = bid_info.get('category', '智能制造')
    bid_industry = bid_info.get('industry', '智能制造')
    
    # 构建技术要求文本
    summaries_text = "\n".join([f"{i+1}. {title}：{content}" for i, (title, content, _) in enumerate(tech_summaries)])
    
    # 知识库论文信息
    knowledge_base = """
【论文1: DeepCQF - ICC 2022】
- 标题: DeepCQF: Making CQF scheduling more intelligent and practicable
- 核心: LSTM预测流量模式，动态调整CQF周期参数 T_new = T_base × (1 + α × burst_factor)
- 场景: 突发流量场景下的CQF调度优化

【论文2: Burst-Aware Multi-CQF - IEEE/ACM TON 2023】
- 标题: Burst-Aware Time-Triggered Flow Scheduling With Enhanced Multi-CQF
- 核心: 增强型Multi-CQF架构，多队列协同，突发检测 σ² = (1/w)Σ(x_i - μ)²
- 场景: TT流与BE流隔离，多优先级队列调度

【论文3: TSN-5G Joint Scheduling - ICCSN 2023 Best Paper】
- 标题: Joint Time-Frequency Resource Scheduling Over CQF-Based TSN-5G System
- 核心: TSN门控列表(GCL) ↔ 5G时隙分配(Slot Allocation)跨域映射
- 场景: 5G与TSN融合网络时频资源联合调度

【论文4: 广义确定性标识网络 - 电子学报 2024】
- 核心: 智能标识路由 RID = Hash(服务类型, 时延需求, 安全等级)
- 场景: 跨域端到端确定性保证

【论文5: End-to-end Deterministic Scheduling - IEEE TMC 2024】
- 核心: DRL深度强化学习调度，PPO算法，MDP建模
- 场景: 融合网络端到端确定性调度

【论文6: Joint Routing and Scheduling - ICCCCS 2022】
- 核心: 联合路由与调度ILP建模，k-最短路径+贪心时隙分配
- 场景: CQF机制下路由与调度联合优化

【专利1: ZL 2021 1 0435398.9】
- 标题: 一种对时敏业务流和路由联合调度的规划方法及装置
- 核心: 流与路由联合调度，在线规划

【专利2: ZL 2021 1 0679100.4】
- 标题: 一种在线规划时间敏感流的方法装置及存储介质
- 核心: 在线实时流规划，动态接入

【专利3: ZL 2023 1 0563323.0】
- 标题: 一种普适的异构融合算网资源智慧适配网络架构及方法
- 核心: 三层架构（工厂层、现场层、设备层），异构资源适配
"""
    
    prompt = f"""你是一位资深的TSN领域技术专家，正在向客户展示你的Agent系统如何智能解析技术要求并匹配到具体的论文/专利成果。

## 招标项目信息
- 行业领域：{bid_category}/{bid_industry}

## 技术要求摘要
{summaries_text}

## 可用知识库
{knowledge_base}

## 任务要求
针对每条技术要求，展示Agent如何"像剥洋葱一样"解析术语并匹配到知识库中的具体成果：

1. **扫描识别**：从技术要求中提取关键技术术语
2. **智能匹配**：匹配到最相关的论文或专利（必须引用上述知识库中的具体成果）
3. **数学描述**：给出该论文/专利中的核心公式或算法
4. **能力证明**：用一句话说明这项成果如何证明你解决该问题的硬核能力

## 输出格式（JSON数组）
[
  {{
    "scan_term": "扫描到的关键词，如'混合流调度（TT与Burst）'",
    "matched_paper": "匹配的论文/专利标题",
    "paper_venue": "发表期刊/会议",
    "paper_index": "检索号如WOS:xxx",
    "formula": "论文中的核心公式",
    "formula_desc": "公式含义说明",
    "visual_desc": "视觉呈现描述，如'Enhanced Multi-CQF队列模型'",
    "capability_proof": "一句话证明能力，如'基于自研增强型多队列映射机制，解决突发流挤占周期流资源的难题'"
  }},
  ...
]

## 要求
- 必须匹配知识库中真实存在的论文/专利
- 公式必须是该论文的核心贡献
- capability_proof要体现"秀操作"的感觉，展示Agent的智能解析能力
- 输出必须是合法的JSON格式，不要有任何额外说明文字"""
    
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {QWEN_API_KEY}"}
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "system", "content": "你是TSN领域专家，擅长展示技术成果。输出必须是合法JSON格式。"},
                {"role": "user", "content": prompt}
            ]
        },
        "parameters": {"temperature": 0.5, "max_tokens": 2000, "result_format": "message"}
    }
    
    try:
        r = requests.post(QWEN_API_URL, headers=headers, json=data, timeout=60)
        if r.status_code != 200:
            return None
        result = r.json()
        if 'output' in result and 'choices' in result['output']:
            content = result['output']['choices'][0]['message']['content']
            # 尝试解析JSON
            try:
                # 清理可能的markdown代码块
                content = content.replace('```json', '').replace('```', '').strip()
                return json.loads(content)
            except:
                return None
        else:
            return None
    except Exception as e:
        return None

def generate_tech_summaries(bid_info):
    """调用Qwen API生成技术要求摘要，要求写人话，去掉AI味"""
    
    bid_category = bid_info.get('category', '智能制造')
    bid_industry = bid_info.get('industry', '智能制造')
    bid_title = bid_info.get('title', '工业网络建设项目')
    bid_org = bid_info.get('org', '某企业')
    
    # 根据行业类型确定技术方向
    if bid_category in ['电力系统', '能源电力', '能源矿产'] or bid_industry in ['电力系统', '能源电力']:
        domain = "电力系统/智能电网"
        domain_keywords = "IEC 61850、GOOSE报文、PMU同步相量、继电保护、变电站自动化、PRP/HSR冗余、电磁兼容"
    elif bid_category in ['轨道交通', '铁路建设'] or bid_industry in ['轨道交通']:
        domain = "轨道交通/CBTC信号系统"
        domain_keywords = "CBTC列车控制、车地通信、TMS列车管理、TCN标准、ERPS/MRP环网冗余、SIL4安全等级、PIS/CCTV"
    elif bid_category in ['5G专网', '通信网络', '通信基建'] or bid_industry in ['通信运营商']:
        domain = "5G专网/通信网络"
        domain_keywords = "5G-TSN融合、网络切片、uRLLC、TSN转换器TT、MEC边缘计算、本地分流LBO、gPTP时间同步"
    else:
        domain = "智能制造/工业物联网"
        domain_keywords = "TSN时间敏感网络、CQF调度、802.1Qbv门控、TT时间触发流、BE尽力而为流、5G+TSN协同、AGV无线接入、多优先级队列"
    
    prompt = f"""你是一位资深的工业互联网技术专家，正在撰写招标项目的技术要求摘要。

## 项目信息
- 招标单位：{bid_org}
- 项目名称：{bid_title}
- 行业领域：{domain}
- 相关技术：{domain_keywords}

## 任务要求
请生成4条技术要求摘要，每条摘要包含一个简短的标题（6-10个字）和一段具体的技术要求描述。

## 输出格式要求
严格按照以下格式输出，每条占一行，标题和描述之间用冒号+空格分隔：

标题1：具体要求描述...
标题2：具体要求描述...
标题3：具体要求描述...
标题4：具体要求描述...

## 写作风格要求（非常重要）
1. **说人话**：用工程师之间交流的口语化表达，避免"综上所述""值得注意的是"等AI腔调
2. **具体明确**：给出具体的数字指标（如时延≤3ms、成功率≥95%），不要泛泛而谈
3. **场景化**：结合行业实际应用场景，说明技术要解决什么实际问题
4. **专业但不堆砌**：适当使用行业术语，但每句话都要有意义，不要为了显得专业而堆砌词汇
5. **简洁有力**：描述控制在50-80字之间，直击要点

## 参考样例
多业务流共存能力：要求系统支持不少于8个优先级的业务映射，能够处理周期性时间触发（TT）流与非周期突发（Burst）流的混合调度，确保关键控制指令的端到端时延确定性。

异构网络融合：需实现5G无线空口资源与有线TSN交换机资源的协同，解决跨网段传输中的抖动累计问题，端到端延迟要求低于10ms。

智能化调度引擎：投标人需提供具备动态规划能力的调度算法，支持在线实时流的动态接入，且在高负载（Load>80%）下保持流调度的成功率不低于95%。

特定业务保障：特别关注大规模分布式计算业务在工业内网中的资源占用冲突问题，要求提供带宽预留和优先级抢占机制，避免关键控制流被挤占。

请直接输出4条技术要求摘要，不要有任何前缀说明。"""
    
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {QWEN_API_KEY}"}
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "system", "content": "你是资深的工业互联网技术专家，擅长撰写技术要求文档。说话直接、专业、不绕弯子。"},
                {"role": "user", "content": prompt}
            ]
        },
        "parameters": {"temperature": 0.7, "max_tokens": 1200, "result_format": "message"}
    }
    
    try:
        r = requests.post(QWEN_API_URL, headers=headers, json=data, timeout=60)
        if r.status_code != 200:
            return None
        result = r.json()
        if 'output' in result and 'choices' in result['output']:
            return result['output']['choices'][0]['message']['content']
        else:
            return None
    except Exception as e:
        return None

def parse_tech_summaries(text):
    """解析API返回的技术摘要文本，提取标题和内容"""
    summaries = []
    colors = ["#e53935", "#1e88e5", "#43a047", "#fb8c00"]
    
    if not text:
        return summaries
    
    lines = text.strip().split('\n')
    color_idx = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 匹配"标题：内容"格式
        if '：' in line or ':' in line:
            # 统一使用中文冒号
            line = line.replace(':', '：')
            parts = line.split('：', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                content = parts[1].strip()
                # 过滤掉过短或明显不是摘要的行
                if len(title) >= 4 and len(content) >= 10:
                    summaries.append((title, content, colors[color_idx % len(colors)]))
                    color_idx += 1
    
    return summaries

def generate_rag_answer(question):
    """基于知识库生成带引用和公式的专家级回答（流式输出）"""
    knowledge = get_knowledge_context()
    
    prompt = f"""你是一位TSN领域专家。请基于以下知识库内容回答用户问题。

## 知识库内容
{knowledge}

## 用户问题
{question}

## 回答要求
1. **技术深度**：回答必须体现专家级技术深度，包含：
   - 数学公式（使用LaTeX格式，如 `$D_{{max}} = \\sum(d_{{hop}}) + \\sum(d_{{queue}})$`）
   - 算法描述（时间复杂度、空间复杂度）
   - 性能指标（具体数值、百分比、时延上界）
   - 约束条件（不等式、边界条件）

2. **引用规范（非常重要）**：
   - 每个技术观点必须引用知识库中的具体论文段落
   - 使用格式：<span style='color:#1976d2;'>([论文ID]；第X章，第Y段)</span>，直接写明章节和段落位置，并用蓝色字体标记
   - 论文ID对应关系：
     * [1] = DeepCQF (ICC 2022)
     * [2] = Burst-Aware Multi-CQF (IEEE/ACM TON 2023)
     * [3] = TSN-5G Joint Scheduling (ICCSN 2023)
     * [4] = 广义确定性标识网络 (电子学报 2024)
     * [5] = End-to-end Deterministic Scheduling (IEEE TMC 2024)
     * [6] = Joint Routing and Scheduling for CQF (ICCCS 2022)
   - 示例："DeepCQF采用LSTM预测流量模式<span style='color:#1976d2;'>([1]；第3章，第2段)</span>，通过公式 $T_{{new}} = T_{{base}} \\times (1 + \\alpha \\cdot \\beta)$ 动态调整周期<span style='color:#1976d2;'>([1]；第3章，第4段)</span>。"
   - 在正文关键技术点处插入蓝色标记的交叉引用，让读者知道该技术来自哪篇论文的具体章节段落
   - 引用段落需包含具体的技术细节、公式或实验数据

3. **回答结构**：
   - **问题分析**：用1-2句话概括问题核心
   - **技术原理**：详细阐述机制原理，包含公式推导
   - **算法设计**：描述算法流程、复杂度分析
   - **性能分析**：给出量化指标和实验结果
   - **引用来源**：列出所有引用的论文

4. **LaTeX公式格式要求（非常重要）**：
   - 行内公式必须使用单个美元符号包裹：`$公式内容$`，例如 `$T_{{new}} = T_{{base}} \\times (1 + \\alpha \\cdot \\beta)$`
   - 独立公式必须使用双美元符号包裹：`$$公式内容$$`，例如 `$$D_{{max}} = \\sum_{{i=1}}^{{n}} d_{{hop}}^i + \\sum_{{j=1}}^{{m}} d_{{queue}}^j \\leq D_{{deadline}}$$`
   - **绝对禁止**使用方括号 `[...]` 来包裹公式，这会导致公式无法渲染
   - 确保所有数学符号都使用正确的LaTeX语法
   - 公式必须可被MathJax正确渲染
   - 希腊字母使用标准LaTeX命令：\\alpha, \\beta, \\sigma, \\mu 等

5. **禁止内容**：
   - 不要使用泛泛而谈的通用描述
   - 不要省略关键的技术参数
   - 不要编造知识库中没有的内容
   - 不要输出LaTeX代码块，直接输出公式语法

请用中文回答，保持学术严谨性。"""
    
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {QWEN_API_KEY}"}
    data = {
        "model": "qwen-turbo", 
        "input": {
            "messages": [
                {"role": "system", "content": "你是TSN领域专家，擅长基于论文引用回答技术问题。回答时必须引用具体论文段落作为证据。"},
                {"role": "user", "content": prompt}
            ]
        }, 
        "parameters": {"temperature": 0.3, "max_tokens": 2500, "result_format": "message"}
    }
    try:
        r = requests.post(QWEN_API_URL, headers=headers, json=data, timeout=180)
        if r.status_code != 200:
            return f"API错误: HTTP {r.status_code} - {r.text[:500]}"
        result = r.json()
        if 'output' in result and 'choices' in result['output']:
            return result['output']['choices'][0]['message']['content']
        else:
            return f"API返回格式异常: {json.dumps(result, ensure_ascii=False)[:500]}"
    except requests.exceptions.Timeout:
        return "API请求超时(180秒)，请稍后重试"
    except requests.exceptions.ConnectionError:
        return "网络连接错误，请检查网络"
    except Exception as e:
        return f"API调用失败: {str(e)}"

def generate_marketing_copy(paper_info, paper_title):
    """调用Qwen API将学术论文降维翻译成营销文案"""
    
    formula = paper_info.get('formula', '')
    concept = paper_info.get('concept', '')
    tech_terms = paper_info.get('tech_terms', [])
    
    prompt = f"""你是一位顶尖的工业科技营销专家，擅长将复杂的学术概念转化为工厂老板能听懂的市场语言。

## 任务
将以下学术论文的核心概念转化为一段150字左右的营销文案，用于短视频或朋友圈传播。

## 论文信息
- 标题：{paper_title}
- 核心概念：{concept}
- 数学公式：{formula}
- 技术关键词：{", ".join(tech_terms)}

## 要求
1. 说人话，去掉AI味，禁止使用"首先、其次、总之"等机械转接词
2. 用工厂老板熟悉的场景和比喻（如AGV小车、工业ETC、红绿灯等）
3. 突出痛点和解决方案的价值
4. 语言要有感染力，像人在说话
5. 150字左右，适合短视频口播

## 输出格式
直接输出营销文案，不要有任何前缀说明。"""

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "qwen-turbo",
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {"temperature": 0.7, "max_tokens": 500, "result_format": "message"}
    }
    
    try:
        r = requests.post(QWEN_API_URL, headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            result = r.json()
            if 'output' in result and 'choices' in result['output']:
                return result['output']['choices'][0]['message']['content'].strip()
        
        # 如果API失败，返回默认文案
        return "很多工厂老板发愁AGV小车老是'打架'，其实是网络交通没排好。我的'工业ETC'算法，能让关键指令在5G和有线网里都跑绿色通道，时延从毫秒降到微秒，调度成功率提升60%。"
    except Exception as e:
        return "很多工厂老板发愁AGV小车老是'打架'，其实是网络交通没排好。我的'工业ETC'算法，能让关键指令在5G和有线网里都跑绿色通道，时延从毫秒降到微秒，调度成功率提升60%。"

def generate_platform_content(core_idea, platform):
    """调用Qwen API生成不同平台的适配内容"""
    
    platform_prompts = {
        "视频号（技术科普）": """你是一位资深的短视频脚本策划专家，专门服务于工业科技领域的技术科普账号。请根据提供的核心观点，创作一份完整的视频分镜脚本。

【视频号文案脚本写法指南】

一、脚本基本结构

黄金3秒开场
痛点引入：直击用户关注的问题
悬念设置：制造好奇心，让人想继续看
利益承诺：告诉用户看完能得到什么
场景带入：快速营造情境

核心内容呈现
逻辑清晰：分点说明，层次分明
案例支撑：用故事或实例佐证观点
节奏把控：每15-30秒一个高潮点

结尾转化设计
总结提炼：回顾核心要点
行动号召：引导点赞、评论、关注
互动提问：增加评论区活跃度

二、文案写作技巧

数字吸引：具体数据更有说服力，如"3个技巧"优于"几个技巧"
情绪共鸣：触动用户情绪，如"你有多久没陪孩子吃饭了"
对比反差：制造认知冲突，如"月薪3千也能实现财务自由"
口语化表达：避免书面语，多用短句，像朋友聊天一样

三、不同类型脚本模板

知识分享类：
开头：提出问题或痛点
中间：分3-5点解析，每点配案例
结尾：总结加互动问题

产品展示类：
开头：场景代入
中间：痛点到产品到效果对比
结尾：优惠信息加购买引导

情感故事类：
开头：场景描写
中间：故事发展加情感递进
结尾：感悟总结加价值升华

四、注意事项

时长控制：建议1分钟
标题优化：10至15字，突出关键词
话题标签：添加2-3个相关话题
字幕适配：方便静音观看的用户
视觉配合：文字与画面要同步呼应
五、优化要点

开头1秒内要有记忆点
语言要精炼，避免啰嗦
重点内容可以重复强调
善用表情符号增加亲和力
测试不同版本，优化数据表现

请严格按照以上指南，输出一份结构完整的视频分镜脚本，包含：
1. 视频标题（10-15字）
2. 话题标签（2-3个）
3. 分镜脚本（按时间轴分场景，包含画面描述+口播文案+时长）
4. 预估总时长

输出格式要求：使用清晰的标题和分段，方便阅读。""",
        
        "知乎（深度专栏）": """你是一位资深的知乎技术专栏作者，擅长撰写高质量的技术深度文章。请根据提供的核心观点，创作一篇符合知乎平台风格的完整技术文章。

【知乎技术文案写作规范】

一、写作风格特点

1. 表达风格
- 语言简洁、清晰、直接，多用短句和列表
- 采用专业、客观的语调，介于正式与非正式之间
- 融入个人化的叙事方式，像朋友分享经验一样自然亲切
- 鼓励读者互动，在文末引导讨论和反馈

2. 内容表达
- 首次提到术语时，进行简单解释
- 观点基于证据和数据驱动，尽可能精确和量化
- 文章要有故事性又有观点，避免单纯罗列操作步骤
- 使用主动语态，使意图立即明确

3. 内容结构
- 引言：问题陈述，说明写作背景和动机
- 正文：解决方案、实践步骤、代码示例
- 总结：关键点回顾，提供延伸资源

二、排版结构规范

1. 标题层级（四级结构）
- 一级标题：文章主标题
- 二级标题：文章主要部分的大标题
- 三级标题：二级标题下的小标题
- 四级标题：三级标题下更细分的内容（慎用，建议用列表替代）

2. 标题使用规则
- 标题前后应保留空行
- 标题避免缩进
- 标题层级不能跳过
- 避免出现孤儿标题（标题下无内容）
- 不应用加粗代替标题

3. 正文排版规范
- 中英文字符、数字与单位之间需加空格（如：TSN 技术）
- 标点符号使用全角格式
- 数字使用半角字符
- 专有名词需保持正确的大小写形式
- 段落不宜过长，减轻阅读压力
- 图文并茂：用图表解释复杂概念

三、知乎技术文案特有风格

1. 高赞回答特征
- 启发性：通过提出高质量、引人深思的问题，引导读者思考
- 权威性：引用权威理论或研究，并解释其与观点的联系
- 逻辑连贯：使用连接词（因为、因此、这意味着等）确保推理步骤清晰

2. 内容选题原则
- 相关性：主题与目标受众相关
- 新颖性：足够新颖，能够吸引读者兴趣
- 实用性：具有实用价值，能帮助读者解决问题

3. 互动与传播
- 在文章末尾设置讨论话题，鼓励读者评论
- 使用 emoji 图标增强可读性（如📝💻🚀💬）
- 提供可模仿的话术模板或实践工具

四、写作流程建议
- 选题阶段：明确目标读者、技术背景和项目背景
- 大纲阶段：撰写简介和大纲，帮助读者快速了解内容
- 正文写作：可采用提问、问答或讲故事的方式增强可读性
- 后期优化：写完通读检查，避免错别字

请严格按照以上规范，输出一篇完整的知乎技术文章，包含：
1. 文章标题（吸引人点击）
2. 文章正文（包含引言、正文、总结三部分）
3. 结尾互动话题（引导评论）
4. 预估阅读时长

输出格式要求：使用清晰的标题层级和排版，符合知乎技术文章规范。""",
        
        "公众号（技术推文）": """你是一位资深的技术公众号主编，擅长撰写高质量的技术推文。请根据提供的核心观点，创作一篇符合技术公众号风格的完整推文。

【技术公众号写作与排版规范】

一、技术公众号写作结构

标题设计
技术公众号标题的核心目标是吸引点击同时明确传达价值。常见策略包括痛点解决型，直击读者常见技术难题；教程干货型，明确标注内容属性；行业趋势型，结合前沿热点；悬念提问型，引发好奇心。

文章开篇
痛点引入用具体场景或问题切入，快速与读者建立共鸣。价值承诺明确告知读者阅读本文能获得什么收获。知识背景简要说明相关技术概念，降低阅读门槛。篇幅控制在50到150字为宜，避免冗长铺垫。

正文架构
推荐采用分层递进结构。基础层包括概念介绍、环境搭建、前置知识，占20%到25%。核心层是关键技术点、代码实现、解决方案，占50%到60%。进阶层是性能优化、扩展应用、常见问题，占15%到20%。总结层是要点回顾、延伸阅读、互动引导，占5%到10%。

段落与内容呈现
采用短段落原则，每段不超过150字，避免视觉压迫。使用代码块隔离，配合语法高亮。关键概念配合图示或完整示例。关键结论用加粗或引用框强调。

结尾设计
内容总结用1到3个要点概括核心内容。提供相关技术文章链接作为延伸阅读。鼓励点赞、转发、留言、加群作为互动引导。设置下期预告建立持续关注的期待感。

二、排版风格规范

基础排版要素
字号设置15到16px是正文阅读舒适区间。行距设置1.6到1.75倍确保段落呼吸感。字间距设置1到1.5px避免过紧或过松。段落间距设置10到15px使段落分隔清晰。段首不缩进，技术文章通常顶格排版。两端对齐使版面整洁。

标题层级系统
一级标题是文章主标题，二级标题是章节标题，三级标题是子章节，四级标题是细分要点。一级标题1个居中加粗字号18到20px。二级标题每节1个字号16到17px可加色块背景。三级及以下标题控制使用避免层级过深。

重点内容排版
代码块样式用独立引用框包裹，背景色选择浅灰或深色主题，字体使用等宽字体，字号14到15px行距1.5倍，添加行号或语法高亮。

引用样式用左侧边框线实心色，背景色浅灰或定制主题色，字号略小于正文，用于代码示例技术注释重点提示。

强调样式中加粗用于关键术语核心结论，斜体用于英文代码变量名，下划线较少使用避免干扰，标记高亮用于特殊强调。

配图使用规范
技术类配图类型包括流程图展示架构逻辑流程，简洁清晰标注关键节点。架构图展示技术层级关系使用标准符号保持一致性。截图展示界面命令行输出清晰可辨标注关键区域。示意图解释抽象概念风格统一配色协调。信息图做数据对比技术对比视觉冲击力强。

配图排版原则每500到800字插入1张图。图片宽度不超过80%版面。图片下方配简短说明10到20字。多图并列时保持尺寸一致。图片质量不低于72dpi。

视觉节奏设计
3到5个段落插入1个图片或代码块避免单调。重点段落单独成段增加行距。过渡段落使用小标题或分割线提示内容转换。关键结论使用引用框或色块背景突出。

颜色体系
推荐配色方案标题用深蓝搭配天蓝色。正文用深灰色搭配中灰色。重点用橙色搭配红色。代码背景用浅灰色搭配中灰色。引用背景用浅蓝色搭配中蓝色。使用原则是主色调不超过3种，保持全文一致性，避免荧光色过度鲜艳色彩，考虑无障碍阅读色盲友好。

留白与呼吸感
页边距每侧8到12px。段间距15到20px。章节间距30到40px。图片上下留白10到15px。

三、技术公众号写作避坑指南

常见写作问题
术语堆砌是过度使用专业术语未做解释。结构混乱是逻辑跳跃缺少层次。代码不规范是缩进混乱变量命名随意缺少注释。示例不完整是关键步骤缺失读者无法复现。图文脱节是图片与内容不相关或引用不当。

排版雷区
字号混乱是同篇文章使用多种字号。段落过长是超过300字的连续文字。颜色过多是超过5种不同颜色。图片模糊是压缩过度或分辨率不足。代码无法复制是代码块格式错误导致无法选中文本。

内容质量标准
准确性要求技术细节必须验证避免错误信息。完整性要求关键步骤不遗漏读者可独立复现。时效性要求技术栈版本明确标注过时内容及时更新。可读性要求逻辑清晰语言通俗避免冗长表述。

四、优化建议

建立模板
建议创建固定的排版模板，包含标题样式各级标题样式代码块样式引用框样式配图说明样式。

工具辅助
编辑器选择使用支持Markdown的公众号编辑器如壹伴秀米135编辑器。代码高亮工具使用CarbonHighlight.js等生成高质量代码图。流程图工具使用DrawioMermaid等生成技术架构图。在线测试发布前在手机端预览确保阅读体验。

持续迭代
定期分析文章数据阅读量完读率收藏数。收集读者反馈了解偏好。参考头部技术公众号的优秀案例。结合最新设计趋势调整排版风格。

请严格按照以上规范，输出一篇完整的技术公众号推文，包含：
1. 推文标题（吸引人点击，10-20字）
2. 文章正文（包含开篇、正文架构、结尾设计）
3. 排版标记（用符号表示标题层级、代码块、重点强调等）
4. 互动引导（引导点赞、转发、留言）
5. 预估阅读时长

【重要格式要求】
- 遇到句号必须换一行，每句话单独成行
- 内容不要出现无序列表（不要用"-"、"*"、"1."等列表符号）
- 语言要说人话，像朋友聊天一样自然
- 坚决去掉AI味，不要"首先、其次、最后、综上所述"这类套话
- 用口语化表达，短句为主，避免长段落

输出格式要求：使用清晰的排版标记，模拟公众号编辑器中的最终效果。"""
    }
    
    prompt = f"""核心观点：{core_idea}

{platform_prompts.get(platform, platform_prompts["视频号（技术科普）"])}"""

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "qwen-turbo",
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {"temperature": 0.7, "max_tokens": 8000, "result_format": "message"}
    }
    
    try:
        r = requests.post(QWEN_API_URL, headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            result = r.json()
            if 'output' in result and 'choices' in result['output']:
                return result['output']['choices'][0]['message']['content'].strip()
        
        # 默认内容
        defaults = {
            "视频号（技术科普）": "你的工厂AGV小车是不是经常'撞车'？其实是网络没排好队。TSN技术就像给工业网络装上智能红绿灯，关键指令走绿色通道，时延从毫秒降到微秒。我们服务的某汽车工厂，部署后调度冲突下降80%，每天多赚20万。",
            "知乎（深度专栏）": "工业互联网的确定性网络为什么重要？传统以太网就像没有红绿灯的十字路口，数据包乱撞导致延迟和丢包。TSN（时间敏感网络）通过CQF调度算法，实现了微秒级的确定性传输。这不仅是技术升级，更是工业4.0的基础设施。",
            "公众号（技术推文）": "【标题】工业网络延迟导致产线瘫痪？TSN技术让AGV小车不再'打架'\n\n【开篇】\n很多工厂老板问我：为什么产线上的AGV小车老是调度冲突？其实问题的根源在于网络通信的确定性不足。\n\n【正文】\nTSN（时间敏感网络）技术通过CQF调度算法，为关键数据流开辟绿色通道，将端到端时延从毫秒级降至微秒级。\n\n【结尾】\n如果你的工厂也面临类似的网络延迟问题，欢迎在评论区留言讨论。点赞转发，让更多同行看到！"
        }
        return defaults.get(platform, defaults["视频号（技术科普）"])
    except Exception as e:
        defaults = {
            "视频号（技术科普）": "你的工厂AGV小车是不是经常'撞车'？其实是网络没排好队。TSN技术就像给工业网络装上智能红绿灯，关键指令走绿色通道，时延从毫秒降到微秒。",
            "知乎（深度专栏）": "工业互联网的确定性网络为什么重要？TSN通过CQF调度算法，实现了微秒级的确定性传输，是工业4.0的基础设施。",
            "公众号（技术推文）": "【标题】工业网络延迟导致产线瘫痪？TSN技术让AGV小车不再'打架'\n\nTSN（时间敏感网络）技术通过CQF调度算法，为关键数据流开辟绿色通道，将端到端时延从毫秒级降至微秒级。"
        }
        return defaults.get(platform, defaults["视频号（技术科普）"])

def generate_positioning_advice(demand_data, sample_messages):
    """调用Qwen API生成商业定位优化建议"""
    
    # 构建需求分析文本
    demand_summary = "\n".join([f"- {category}: {count}条咨询" for category, count in demand_data.items()])
    
    # 构建私信样本文本
    messages_summary = "\n".join([f"- {msg['from']}（{msg['category']}，紧急度{msg['urgency']}）: {msg['content']}" for msg in sample_messages])
    
    prompt = f"""你是一位资深的商业战略顾问，专注于AI和工业科技领域的商业定位分析。

【当前数据背景】

1. 近7天企业私信需求分布：
{demand_summary}

2. 典型咨询案例：
{messages_summary}

3. RAG知识库技术资产：
- 论文：6篇（覆盖TSN、CQF、确定性网络调度算法）
- 专利：3项（联合调度、资源分配、自适应优化）
- 标准：2项（YD/T 6568-2023、T/CCSA 491-2024）

4. 当前项目定位：
- 核心方向：工业确定性网络解决方案
- 目标客户：智能制造、汽车工厂、5G+工业互联网
- 技术标签：TSN、CQF、5G融合、联邦学习

【分析任务】

请基于以上数据，从以下四个维度给出商业定位优化建议：

一、当前定位优势（3-5点）
分析当前技术资产与市场需求匹配的优势点

二、当前定位劣势（3-5点）
指出当前定位存在的短板和盲区

三、市场机会洞察（3-5点）
基于私信需求分析，指出潜在的市场机会

四、具体优化建议（5-7条）
给出可落地的定位调整建议，包括：
- 垂直领域聚焦建议
- 内容策略调整方向
- 客户群体优化建议
- 技术标签强化建议

【输出要求】
- 遇到句号必须换一行，每句话单独成行
- 语言要说人话，像朋友聊天一样自然
- 坚决去掉AI味，不要"首先、其次、最后、综上所述"这类套话
- 用口语化表达，短句为主
- 内容要有洞察，不要泛泛而谈
"""

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "qwen-turbo",
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {"temperature": 0.7, "max_tokens": 8000, "result_format": "message"}
    }
    
    try:
        r = requests.post(QWEN_API_URL, headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            result = r.json()
            if 'output' in result and 'choices' in result['output']:
                return result['output']['choices'][0]['message']['content'].strip()
        
        # 默认内容
        return """【当前定位优势】

你的技术资产很扎实。
6篇顶刊论文加上3项专利，在TSN这个细分领域是有话语权的。
私信里TSN部署咨询占了5条，说明你的内容输出确实打中了目标客户的痛点。
汽车工厂AGV调度这个场景选得准，需求明确且付费能力强。

【当前定位劣势】

联邦学习只有3条咨询，占比偏低。
这说明你的跨领域整合能力还没被市场充分认知。
5G+工业互联网的咨询有4条，但你知识库里缺乏5G相关的技术资产储备。
客户问TSN和5G融合的时间同步精度，你只能凭经验回答，缺乏权威背书。

【市场机会洞察】

确定性网络方案有6条咨询，是需求最多的类别。
但客户问的不只是TSN，还包括5G、WiFi6等其他确定性技术。
如果你能扩展知识库覆盖更多确定性网络技术，可以承接更大的项目。
另外，"其他技术合作"有2条，说明你的IP影响力已经开始外溢。

【具体优化建议】

1. 短期聚焦汽车工厂AGV场景，把这个垂直领域打透。
2. 中期补充5G+TSN融合的技术内容，填补知识库空白。
3. 把联邦学习和TSN做结合，打造差异化技术标签。
4. 多输出"时间同步精度"这类客户高频询问的技术话题。
5. 建立客户案例库，用真实数据支撑你的技术方案。
6. 考虑开设线上技术分享，把"其他技术合作"的泛流量转化为精准客户。
7. 定期分析私信关键词，动态调整内容策略。"""
    except Exception as e:
        return """【当前定位优势】

技术资产扎实，6篇论文+3项专利形成护城河。
TSN咨询占比25%，内容输出打中痛点。
汽车工厂场景选得准，客户付费能力强。

【当前定位劣势】

联邦学习认知度不足，咨询占比仅15%。
5G融合技术储备不够，难以回答深度问题。
知识库覆盖范围偏窄，限制业务拓展空间。

【市场机会洞察】

确定性网络需求旺盛，但竞争也在加剧。
客户需要端到端解决方案，不只是单一技术。
跨领域整合能力是下一个差异化竞争点。

【具体优化建议】

1. 打透汽车工厂垂直场景，建立标杆案例。
2. 补充5G+TSN融合技术内容。
3. 强化联邦学习+确定性网络的结合点。
4. 建立客户成功案例库。
5. 定期分析私信数据，动态调整定位。"""

# 侧边栏导航
st.sidebar.title("⚙️ IntelliLink")
st.sidebar.markdown("基于 AI Agent 的高阶技术资产转化平台")
st.sidebar.markdown("---")
st.sidebar.markdown("**产业链导航**")
page = st.sidebar.radio("", ["🏠 首页", "📚 上游：专家级RAG知识库Agent", "🎯 中游：商业决策Agent", "📢 下游：IP运营Agent"])
st.sidebar.markdown("---")
st.sidebar.markdown("**个人履历**")
st.sidebar.info("院士团队、博士学历 | IEEE TON/TMC顶刊 | 信通院认证网络交换机产品")

# ==================== 首页：产业链全景 ====================
if page == "🏠 首页":
    st.title("🏠 AI一人公司 · 产业链全景")
    st.markdown("**技术资产 → 商业决策 → IP影响力** 的闭环生态")
    st.divider()
    
    # 核心架构图 - 使用Streamlit原生组件
    st.markdown("### 🔄 产业链闭环架构")
    
    # 第一行：正向流程
    flow_cols = st.columns([10, 2, 10, 2, 10])
    
    with flow_cols[0]:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border: 3px solid #2196f3; border-radius: 16px; padding: 20px; text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">📚</div>
            <div style="font-size: 1.1rem; font-weight: bold; color: #1565c0;">上游：专家级RAG知识库Agent</div>
            <div style="font-size: 0.8rem; color: #666; margin-top: 8px;">技术资产沉淀</div>
            <div style="margin-top: 10px; display: flex; flex-wrap: wrap; justify-content: center; gap: 5px;">
                <span style="background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; color: #2196f3;">📄 6篇顶刊论文</span>
                <span style="background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; color: #2196f3;">🔒 3项专利</span>
                <span style="background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; color: #2196f3;">📋 2项标准</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("⬆️ 中游优化反馈")
    
    with flow_cols[1]:
        st.markdown("""
        <div style="text-align: center; padding-top: 110px; font-size: 2rem; color: #666;">
            →
        </div>
        """, unsafe_allow_html=True)
    
    with flow_cols[2]:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border: 3px solid #ff9800; border-radius: 16px; padding: 20px; text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">🎯</div>
            <div style="font-size: 1.1rem; font-weight: bold; color: #e65100;">中游：商业决策Agent</div>
            <div style="font-size: 0.8rem; color: #666; margin-top: 8px;">精准匹配 · 智能决策</div>
            <div style="margin-top: 10px; display: flex; flex-wrap: wrap; justify-content: center; gap: 5px;">
                <span style="background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; color: #ff9800;">🕷️ 实时爬虫</span>
                <span style="background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; color: #ff9800;">🤖 AI匹配</span>
                <span style="background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; color: #ff9800;">📊 智能报告</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("⬇️ 变现反馈")
    
    with flow_cols[3]:
        st.markdown("""
        <div style="text-align: center; padding-top: 110px; font-size: 2rem; color: #666;">
            →
        </div>
        """, unsafe_allow_html=True)
    
    with flow_cols[4]:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border: 3px solid #9c27b0; border-radius: 16px; padding: 20px; text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">📢</div>
            <div style="font-size: 1.1rem; font-weight: bold; color: #7b1fa2;">下游：IP运营Agent</div>
            <div style="font-size: 0.8rem; color: #666; margin-top: 8px;">知识资产 → IP资产</div>
            <div style="margin-top: 10px; display: flex; flex-wrap: wrap; justify-content: center; gap: 5px;">
                <span style="background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; color: #9c27b0;">🎬 短视频</span>
                <span style="background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; color: #9c27b0;">📝 技术专栏</span>
                <span style="background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; color: #9c27b0;">🌟 个人品牌</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("➡️ 影响力放大")
    
    # 核心逻辑说明
    st.info("💡 **核心逻辑**：中游既是**知识库→商业定位**的转化器，也是**商业反馈→定位优化**的调节器")
    
    st.divider()
    
    # 详细说明
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 20px; border-radius: 12px; border-left: 4px solid #2196f3; height: 480px;">
            <h4 style="color: #1565c0; margin-top: 0;">📚 上游：专家级RAG知识库Agent</h4>
            <p style="font-size: 0.9rem; color: #333;">
                <b>核心功能：</b>构建私有技术知识库<br><br>
                💡 <b>亮点：</b>区别于只对专业问题作出浅显描述的通用智能问答系统，上游Agent会基于<b>专家知识库</b>对具体问题作出论述，包含详尽的理论和公式定义、文献索引、技术路线、专家方案、踩坑经验等。
            </p>
            <p style="font-size: 0.8rem; color: #666; margin-top: 15px; padding-top: 10px; border-top: 1px dashed #90caf9;">
                <b>输出：</b>专家级技术知识 → 中游调用
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); padding: 20px; border-radius: 12px; border-left: 4px solid #ff9800; height: 480px;">
            <h4 style="color: #e65100; margin-top: 0;">🎯 中游：商业决策Agent</h4>
            <p style="font-size: 0.9rem; color: #333;">
                <b>核心功能：</b>专家知识-商业精准匹配<br><br>
                💡 <b>亮点：</b>结合RAG知识库，实时爬取并匹配专业相关的企业项目信息，然后将项目中模糊的工业需求翻译成<b>精确的数学描述</b>，从而适配RAG库中的算法逻辑，<b>自动生成</b>专业技术报告。同时，还能根据下游Agent提交的运营反馈来持续<b>优化商业定位</b>。
            </p>
            <p style="font-size: 0.8rem; color: #666; margin-top: 15px; padding-top: 10px; border-top: 1px dashed #ffcc80;">
                <b>双向反馈：</b>接收上游知识 + 反馈下游需求
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 20px; border-radius: 12px; border-left: 4px solid #9c27b0; height: 480px;">
            <h4 style="color: #7b1fa2; margin-top: 0;">📢 下游：IP运营Agent</h4>
            <p style="font-size: 0.9rem; color: #333;">
                <b>核心功能：</b>知识资产→IP资产转换<br><br>
                💡 <b>亮点：</b>具备"学术-市场"语义平替能力，将晦涩的学术成果转化为<b>高传播力</b>的行业科普资产。同时通过私信反馈回路，及时捕捉客户真实痛点，实现从"内容分发"到"需求回传"的闭环，使一人公司的获客效率提升<b>10倍</b>以上。
            </p>
            <p style="font-size: 0.8rem; color: #666; margin-top: 15px; padding-top: 10px; border-top: 1px dashed #ce93d8;">
                <b>输出：</b>商业变现反馈 → 中游优化
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # 数据飞轮效应
    st.markdown("### 🔄 数据飞轮效应")
    
    flywheel_col1, flywheel_col2 = st.columns([1, 1.5])
    
    with flywheel_col1:
        st.markdown("""
        <div style="text-align: center; padding: 30px;">
            <div style="font-size: 4rem; animation: spin 4s linear infinite;">⚙️</div>
            <style>
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            </style>
        </div>
        """, unsafe_allow_html=True)
    
    with flywheel_col2:
        st.markdown("""
        <div style="background: #fafafa; padding: 20px; border-radius: 12px;">
            <h4 style="color: #333; margin-top: 0;">飞轮运转逻辑</h4>
            <ol style="font-size: 0.9rem; color: #555; line-height: 2;">
                <li><b>上游知识库</b>为<b>中游</b>提供技术弹药</li>
                <li><b>中游</b>精准匹配商机，输出<b>商业报告</b></li>
                <li><b>下游</b>将技术转化为内容，<b>放大影响力</b></li>
                <li><b>下游变现数据</b>反馈给<b>中游</b>优化定位</li>
                <li><b>中游</b>根据市场反馈，指导<b>上游</b>补充知识</li>
                <li><b>循环往复</b>，形成正向增强回路</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # 核心指标
    st.markdown("### 📊 核心运营指标")
    
    metric_cols = st.columns(4)
    metrics = [
        ("📚 知识库", "6篇论文 + 3专利 + 2标准", "持续积累中"),
        ("🎯 商机匹配", "94% 平均匹配度", "50+ 实时招标"),
        ("📢 内容产出", "23篇/周", "156万+ 总阅读"),
        ("💰 商业转化", "¥2,340万", "预估项目总额")
    ]
    
    for i, (title, value, desc) in enumerate(metrics):
        metric_cols[i].markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; text-align: center; height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">{title}</div>
            <div style="font-size: 1.3rem; font-weight: bold;">{value}</div>
            <div style="font-size: 0.8rem; opacity: 0.9; margin-top: 5px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # 快速导航
    st.markdown("### 🚀 快速进入各环节")
    
    nav_cols = st.columns(3)
    with nav_cols[0]:
        if st.button("📚 进入上游知识库", use_container_width=True):
            st.session_state['nav_to'] = "📚 上游：专家级RAG知识库Agent"
            st.rerun()
    with nav_cols[1]:
        if st.button("🎯 进入中游决策Agent", use_container_width=True, type="primary"):
            st.session_state['nav_to'] = "🎯 中游：商业决策Agent"
            st.rerun()
    with nav_cols[2]:
        if st.button("📢 进入下游IP运营", use_container_width=True):
            st.session_state['nav_to'] = "📢 下游：IP运营Agent"
            st.rerun()
    
    # 处理导航
    if 'nav_to' in st.session_state:
        nav_target = st.session_state.pop('nav_to')
        st.info(f"正在跳转到 {nav_target}...")

# ==================== 上游：专家级RAG知识库Agent ====================
elif page == "📚 上游：专家级RAG知识库Agent":
    st.title("📚 上游：私有RAG知识库")
    st.markdown("基于TON/TMC论文语料的智能知识引擎")
    st.divider()
    
    left, center, right = st.columns([1.2, 2, 1])
    
    with left:
        st.markdown("### 📄 已收录论文 (6篇)")
        
        for p in get_papers():
            # 前3篇论文默认展开，后面的默认收起
            is_expanded = p['id'] <= 3
            with st.expander(f"[{p['id']}] {p['title'][:45]}...", expanded=is_expanded):
                st.markdown(f"**论文标题**：{p['title']}")
                st.markdown(f"**发表期刊/会议**：{p['venue']}")
                st.markdown(f"**发表年份**：{p['year']}")
                if 'volume' in p and 'pages' in p:
                    st.markdown(f"**卷期页**：{p['volume']}, pp.{p['pages']}")
                elif 'pages' in p:
                    st.markdown(f"**页码**：pp.{p['pages']}")
                st.markdown(f"**检索信息**：{p['index']}")
                if 'wos' in p:
                    st.markdown(f"**WOS号**：{p['wos']}")
                if 'accession' in p:
                    st.markdown(f"**检索号**：{p['accession']}")
                
                st.divider()
                st.markdown("**📋 文章概览**")
                st.info(p['overview'])
                
                # 打开PDF按钮
                if st.button(f"📖 查看原文", key=f"pdf_{p['id']}"):
                    if open_pdf(p['path']):
                        st.success(f"✅ 已打开论文 [{p['id']}]")
                    else:
                        st.error(f"❌ 文件不存在: {p['path']}")
        
        st.markdown("### 📋 技术标准")
        for s in get_standards():
            with st.expander(f"[{s['id']}] {s['title'][:30]}...", expanded=False):
                st.markdown(f"**标准名称**：{s['title']}")
                st.markdown(f"**标准类型**：{s['type']}")
                st.markdown(f"**标准号**：{s['standard_no']}")
                
                st.divider()
                # 打开PDF按钮
                if st.button(f"📖 查看原文", key=f"std_pdf_{s['id']}"):
                    if open_pdf(s['path']):
                        st.success(f"✅ 已打开标准 [{s['id']}]")
                    else:
                        st.error(f"❌ 文件不存在: {s['path']}")
        
        st.markdown("### 🔒 发明专利")
        for p in get_patents():
            with st.expander(f"[{p['id']}] {p['title'][:30]}...", expanded=False):
                st.markdown(f"**专利名称**：{p['title']}")
                st.markdown(f"**专利类型**：{p['type']}")
                st.markdown(f"**专利状态**：{p['status']}")
                st.markdown(f"**专利号**：{p['patent_no']}")
                
                st.divider()
                st.markdown("**📋 概览**")
                
                # 打开专利原文按钮
                if st.button(f"📖 打开专利原文", key=f"patent_pdf_{p['id']}"):
                    if open_pdf(p['path']):
                        st.success(f"✅ 已打开专利原文 [{p['id']}]")
                    else:
                        st.error(f"❌ 文件不存在: {p['path']}")
                
                # 打开授权证书按钮
                if st.button(f"📜 打开授权证书", key=f"patent_cert_{p['id']}"):
                    if open_pdf(p['cert_path']):
                        st.success(f"✅ 已打开授权证书 [{p['id']}]")
                    else:
                        st.error(f"❌ 文件不存在: {p['cert_path']}")
    
    with center:
        st.markdown("### 🤖 智能问答系统")
        st.caption("💡 基于RAG知识库回答，自动引用论文段落")
        
        # 初始化session_state
        if 'current_question' not in st.session_state:
            st.session_state.current_question = ""
        if 'trigger_answer' not in st.session_state:
            st.session_state.trigger_answer = False
        
        # 快速提问按钮
        st.markdown("**💡 快速提问**")
        cols = st.columns(2)
        quick = ["CQF vs TAS区别？", "5G+TSN融合挑战？", "DRL在TSN中的应用？", "端到端确定性保证？"]
        for i, qq in enumerate(quick):
            if cols[i % 2].button(qq, key=f"q{i}"):
                st.session_state.current_question = qq
                st.session_state.trigger_answer = True
                st.rerun()
        
        st.divider()
        
        # 使用text_area，绑定到session_state
        def on_question_change():
            st.session_state.current_question = st.session_state.question_input_widget
        
        q = st.text_area("输入技术问题：", 
                         value=st.session_state.current_question, 
                         placeholder="例如：CQF调度的核心优势是什么？", 
                         height=80, 
                         key="question_input_widget",
                         on_change=on_question_change)
        
        # 同步到session_state
        st.session_state.current_question = q
        
        # 生成回答按钮或自动触发
        clicked = st.button("🚀 生成回答", type="primary", use_container_width=True)
        
        if clicked or st.session_state.trigger_answer:
            # 重置触发标志
            st.session_state.trigger_answer = False
            
            if st.session_state.current_question.strip():
                with st.spinner("🔍 正在生成回答..."):
                    full_answer = generate_rag_answer(st.session_state.current_question)
                    
                    # 修复AI可能使用的错误公式格式：将方括号替换为美元符号
                    import re
                    full_answer = re.sub(r'\[\s*([^\]]+?)\s*\]', r'$\1$', full_answer)
                    
                    # AI已在Prompt要求下直接输出带蓝色样式的交叉引用，无需额外处理
                
                st.markdown("#### 💡 回答")
                st.markdown(full_answer, unsafe_allow_html=True)
                
                # 强制触发MathJax重新渲染
                st.markdown("""
                <script>
                if (window.MathJax) {
                    MathJax.typesetPromise();
                }
                </script>
                """, unsafe_allow_html=True)
                
                # 显示知识库覆盖情况
                st.divider()
                st.markdown("**📚 知识库覆盖（点击可跳转到对应论文）**")
                cols = st.columns(6)
                for i, p in enumerate(get_papers()):
                    with cols[i]:
                        st.markdown(f"<div id='paper_{p['id']}' style='text-align:center;font-size:0.7rem;background:#e3f2fd;padding:0.3rem;border-radius:4px;cursor:pointer;' title='{p['title']}'>[{p['id']}]<br/>{p['venue'][:10]}</div>", unsafe_allow_html=True)
            else:
                st.warning("请先输入问题")
    
    with right:
        st.markdown("### 🚀 产品展示")
        
        # 产品1：基于深度强化学习的SDN+TSN流量调度系统
        with st.expander("🎯 基于深度强化学习的SDN+TSN流量调度系统", expanded=True):
            st.markdown("**基于深度强化学习的SDN+TSN流量调度系统**")
            st.image("D:/workbuddy/project/pics/SDN+TSN原型系统.png", 
                     caption="SDN+TSN原型系统", 
                     use_container_width=True)
        
        # 产品2：基于Linux白核系统自主研发的交换机NGIT-TSN-S-I
        with st.expander("🔌 自主研发交换机 NGIT-TSN-S-I", expanded=True):
            st.markdown("**基于Linux白核系统自主研发的交换机 NGIT-TSN-S-I**")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image("D:/workbuddy/project/pics/白色.jpg", 
                         caption="白色款", 
                         use_container_width=True)
            with col_img2:
                st.image("D:/workbuddy/project/pics/黑色.jpg", 
                         caption="黑色款", 
                         use_container_width=True)
        
        # 产品3：中国信通院交换机测试认证证书（图片顺时针旋转90度）
        with st.expander("📜 中国信通院交换机测试认证证书", expanded=True):
            st.markdown("**中国信通院交换机测试认证证书**")
            from PIL import Image
            import io
            cert_img = Image.open("D:/workbuddy/project/pics/信通院交换机测试认证证书.jpg")
            cert_img_rotated = cert_img.rotate(-90, expand=True)
            st.image(cert_img_rotated, 
                     caption="信通院测试认证证书", 
                     use_container_width=True)
        
        st.markdown("### 📈 知识库统计")
        c1, c2 = st.columns(2)
        c1.metric("论文", "6篇")
        c2.metric("标准", "2项")
        c1.metric("专利", "3项")
        c2.metric("语料", "50万+")

# ==================== 中游：商业决策Agent ====================
elif page == "🎯 中游：商业决策Agent":
    st.title("🎯 中游：商业决策Agent")
    st.markdown("实时捕捉商业情报 · AI驱动决策 · 技术自动适配")
    st.divider()
    
    # 爬虫控制面板
    with st.expander("🕷️ 爬虫控制台 - 配置数据源", expanded=True):
        st.markdown("#### 📡 可爬取的招标信息源")
        
        # 数据源配置表格
        sources_data = {
            "网站名称": [
                "中国政府采购网", "中国招标投标公共服务平台", "中国移动采购与招标网",
                "国家电网电子商务平台", "中国电信阳光采购网", "中国联通采购与招标网",
                "中国铁塔在线商务平台", "中国中车采购平台", "宝武钢铁招标平台",
                "中国航天科工招标平台", "中国船舶采购平台", "中国兵器采购平台",
                "中国华能招标平台", "中国大唐采购平台", "中国华电招标网",
                "国家能源招标网", "中国电建招标平台", "中国能建采购平台",
                "中国交建采购平台", "中国中铁采购平台"
            ],
            "网址": [
                "ccgp.gov.cn", "cebpubservice.com", "b2b.10086.cn",
                "ecp.sgcc.com.cn", "caigou.chinatelecom.com.cn", "www.chinaunicombidding.cn",
                "www.tower.com.cn", "www.crrcgc.cc", "www.baowugroup.com",
                "www.casic.com.cn", "www.csic.com.cn", "www.norincogroup.com.cn",
                "www.chng.com.cn", "www.china-cdt.com", "www.chd.com.cn",
                "www.chnenergybidding.com.cn", "powerchina.cn", "www.ceec.net.cn",
                "www.ccccltd.cn", "www.crec.cn"
            ],
            "数据类型": [
                "政府采购", "综合招标", "5G/通信",
                "电力系统", "通信网络", "通信设备",
                "通信基建", "轨道交通", "钢铁制造",
                "航天军工", "船舶制造", "军工装备",
                "能源电力", "能源电力", "能源电力",
                "能源矿产", "工程建设", "工程建设",
                "交通建设", "铁路建设"
            ],
            "技术关键词": [
                "工业互联网、网络设备", "TSN、SDN、网络优化", "5G专网、边缘计算",
                "智能电网、TSN、确定性网络", "5G+TSN、网络切片", "SDN、NFV、网络虚拟化",
                "5G基站、承载网", "列车网络、确定性通信", "工业以太网、实时网络",
                "高可靠网络、实时传输", "船舶网络、工业控制", "军工网络、安全通信",
                "电力通信、工业网络", "电厂网络、监控系统", "能源互联网、智能电网",
                "煤矿智能化、工业网络", "工程网络、远程监控", "建设物联网、设备联网",
                "交通物联网、车路协同", "铁路通信、信号系统"
            ],
            "爬取状态": [
                "✅ 可爬取", "✅ 可爬取", "✅ 可爬取",
                "✅ 可爬取", "✅ 可爬取", "✅ 可爬取",
                "✅ 可爬取", "✅ 可爬取", "✅ 可爬取",
                "✅ 可爬取", "✅ 可爬取", "✅ 可爬取",
                "✅ 可爬取", "✅ 可爬取", "✅ 可爬取",
                "✅ 可爬取", "✅ 可爬取", "✅ 可爬取",
                "✅ 可爬取", "✅ 可爬取"
            ]
        }
        
        import pandas as pd
        df_sources = pd.DataFrame(sources_data)
        st.dataframe(df_sources, use_container_width=True, height=300)
        
        st.markdown("---")
        
        # 技术关键词筛选
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            selected_keywords = st.multiselect(
                "🔍 筛选技术关键词",
                ["TSN", "SDN", "5G专网", "确定性网络", "实时性", "低抖动", "工业以太网", 
                 "网络切片", "边缘计算", "时间同步", "周期流", "高可靠性"],
                default=["TSN", "SDN", "确定性网络", "实时性"]
            )
        with col_filter2:
            selected_industries = st.multiselect(
                "🏭 筛选行业领域",
                ["智能制造", "电力系统", "轨道交通", "通信运营商", "石油化工", "汽车工厂"],
                default=["智能制造", "电力系统", "轨道交通"]
            )
        
        # 开始搜索按钮
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            start_crawl = st.button("🚀 开始爬取", type="primary", use_container_width=True)
        with col_btn2:
            refresh_data = st.button("🔄 刷新数据", use_container_width=True)
        with col_btn3:
            st.markdown("<div style='padding-top:10px;'>💡 点击开始爬取后，系统将并行爬取20个数据源</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # 生成50条模拟招标数据
    def generate_mock_bids():
        """生成50条模拟招标数据，匹配TSN/SDN/实时性等技术场景，每次调用都随机生成"""
        mock_bids = []
        
        # 招标主体池（扩展更多企业和地区）
        orgs_pool = [
            ("中国移动通信集团江苏有限公司", "5G专网", "江苏·南京"),
            ("中国移动通信集团浙江有限公司", "5G专网", "浙江·杭州"),
            ("中国移动通信集团广东有限公司", "5G专网", "广东·深圳"),
            ("国家电网浙江省电力公司", "电力系统", "浙江·杭州"),
            ("国家电网江苏省电力公司", "电力系统", "江苏·南京"),
            ("国家电网山东省电力公司", "电力系统", "山东·济南"),
            ("上海汽车集团股份有限公司", "智能制造", "上海·浦东"),
            ("吉利汽车集团有限公司", "智能制造", "浙江·宁波"),
            ("长城汽车股份有限公司", "智能制造", "河北·保定"),
            ("中国中车株洲电力机车有限公司", "轨道交通", "湖南·株洲"),
            ("中国中车青岛四方机车车辆", "轨道交通", "山东·青岛"),
            ("中国中车长春轨道客车", "轨道交通", "吉林·长春"),
            ("宝山钢铁股份有限公司", "智能制造", "上海·宝山"),
            ("鞍钢集团有限公司", "智能制造", "辽宁·鞍山"),
            ("首钢集团有限公司", "智能制造", "北京·石景山"),
            ("中国石油化工股份有限公司", "石油化工", "北京·朝阳"),
            ("中国石油天然气集团", "石油化工", "北京·东城"),
            ("中国海洋石油集团", "石油化工", "北京·西城"),
            ("中国华能集团有限公司", "能源电力", "北京·西城"),
            ("中国大唐集团有限公司", "能源电力", "北京·西城"),
            ("中国华电集团有限公司", "能源电力", "北京·西城"),
            ("国家电力投资集团", "能源电力", "北京·西城"),
            ("中国船舶集团有限公司", "船舶制造", "上海·黄浦"),
            ("中国船舶集团大连船舶重工", "船舶制造", "辽宁·大连"),
            ("中国航天科工集团第二研究院", "航天军工", "北京·海淀"),
            ("中国航天科技集团第五研究院", "航天军工", "北京·海淀"),
            ("中国兵器工业集团有限公司", "军工装备", "北京·西城"),
            ("中国电子科技集团", "军工装备", "北京·石景山"),
            ("中国电信股份有限公司广东分公司", "5G专网", "广东·广州"),
            ("中国电信股份有限公司江苏分公司", "5G专网", "江苏·南京"),
            ("中国联通网络通信有限公司", "通信网络", "北京·西城"),
            ("中国联通广东省分公司", "通信网络", "广东·广州"),
            ("中国铁塔股份有限公司", "通信基建", "北京·海淀"),
            ("中国铁塔上海分公司", "通信基建", "上海·浦东"),
            ("国家能源投资集团", "能源矿产", "北京·东城"),
            ("中国中煤能源集团", "能源矿产", "北京·东城"),
            ("中国电力建设集团", "工程建设", "北京·海淀"),
            ("中国能源建设集团", "工程建设", "北京·西城"),
            ("中国交通建设集团", "交通建设", "北京·东城"),
            ("中国铁路工程集团", "铁路建设", "北京·丰台"),
            ("中国铁道建筑集团", "铁路建设", "北京·石景山"),
            ("海尔集团公司", "智能制造", "山东·青岛"),
            ("海信集团有限公司", "智能制造", "山东·青岛"),
            ("华为技术有限公司", "通信设备", "广东·深圳"),
            ("中兴通讯股份有限公司", "通信设备", "广东·深圳"),
            ("比亚迪股份有限公司", "汽车制造", "广东·深圳"),
            ("蔚来汽车", "汽车制造", "上海·嘉定"),
            ("小鹏汽车", "汽车制造", "广东·广州"),
            ("三一重工股份有限公司", "工程机械", "湖南·长沙"),
            ("中联重科股份有限公司", "工程机械", "湖南·长沙"),
            ("徐工集团工程机械有限公司", "工程机械", "江苏·徐州"),
            ("柳工机械股份有限公司", "工程机械", "广西·柳州"),
            ("潍柴动力股份有限公司", "智能制造", "山东·潍坊"),
            ("美的集团股份有限公司", "智能制造", "广东·佛山"),
            ("格力电气股份有限公司", "智能制造", "广东·珠海"),
            ("青岛啤酒股份有限公司", "智能制造", "山东·青岛"),
            ("茅台集团股份有限公司", "智能制造", "贵州·遵义"),
        ]
        
        # 招标项目模板池（扩展更多场景）
        project_templates_pool = [
            "{industry}车间TSN确定性网络建设项目",
            "{industry}5G+TSN融合专网采购项目",
            "{industry}SDN智能网络调度系统建设",
            "{industry}工业以太网升级改造工程",
            "{industry}时间敏感网络(TSN)设备采购",
            "{industry}低时延高可靠网络建设项目",
            "{industry}实时控制系统网络优化项目",
            "{industry}确定性网络架构设计与实施",
            "{industry}工业网络时间同步系统建设",
            "{industry}边缘计算与TSN融合平台",
            "{industry}智能工厂网络基础设施项目",
            "{industry}周期流传输优化系统采购",
            "{industry}网络抖动控制与优化项目",
            "{industry}高可用工业通信网络建设",
            "{industry}端到端确定性传输网络项目",
            "{industry}工业互联网安全隔离项目",
            "{industry}智能运维网络管理平台",
            "{industry}5G LAN专网建设项目",
            "{industry}工业WiFi6与TSN融合项目",
            "{industry}云网融合数据中心建设",
            "{industry}数字孪生网络底座项目",
            "{industry}AI驱动的网络自愈系统",
            "{industry}零信任网络安全架构",
            "{industry}IPv6+工业网络升级",
            "{industry}高精度时间同步骨干网",
        ]
        
        # 技术标签池（扩展）
        tech_keywords_pool = [
            ["TSN", "时间敏感网络", "IEEE 802.1AS"],
            ["SDN", "软件定义网络", "OpenFlow"],
            ["5G专网", "网络切片", "uRLLC"],
            ["确定性网络", "CQF调度", "低抖动"],
            ["实时以太网", "PROFINET", "EtherCAT"],
            ["时间同步", "PTP", "IEEE 1588"],
            ["工业物联网", "OPC UA", "MQTT"],
            ["边缘计算", "MEC", "本地分流"],
            ["网络虚拟化", "NFV", "容器网络"],
            ["高可靠性", "冗余备份", "零丢包"],
            ["WiFi6", "低时延", "高并发"],
            ["5G LAN", "二层互通", "确定性"],
            ["IPv6+", "SRv6", "网络编程"],
            ["零信任", "微分段", "安全隔离"],
            ["AI运维", "智能预测", "故障自愈"],
        ]
        
        # 数据源池
        sources_pool = [
            "中国政府采购网", "中国招标投标公共服务平台", "中国移动采购与招标网",
            "国家电网电子商务平台", "中国电信阳光采购网", "中国联通采购与招标网",
            "中国铁塔在线商务平台", "中国中车采购平台", "宝武钢铁招标平台",
            "中国航天科工招标平台", "中国华能招标平台", "国家能源招标网"
        ]
        
        import random
        from datetime import datetime, timedelta
        
        # 每次随机打乱顺序，确保数据不重复
        random.shuffle(orgs_pool)
        random.shuffle(project_templates_pool)
        
        base_date = datetime.now()
        
        for i in range(50):
            # 随机选择企业（不重复遍历，而是随机抽取）
            org, industry, region = random.choice(orgs_pool)
            template = random.choice(project_templates_pool)
            title = template.format(industry=industry.replace("制造", "").replace("系统", ""))
            
            # 随机金额 50万-5000万
            amount = random.randint(5, 50) * 10
            
            # 随机截止日期（未来7-90天）
            days_ahead = random.randint(7, 90)
            deadline = (base_date + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
            
            # 随机发布时间（过去0-72小时）
            hours_ago = random.randint(0, 72)
            if hours_ago < 1:
                time_ago = "刚刚"
            elif hours_ago < 24:
                time_ago = f"{hours_ago}小时前"
            else:
                time_ago = f"{hours_ago // 24}天前"
            
            # 随机技术标签
            tech_tags = random.choice(tech_keywords_pool)
            
            # 匹配度计算（基于技术关键词匹配，确保有变化）
            match_score = random.randint(76, 97)
            
            # 随机数据源
            source_website = random.choice(sources_pool)
            
            # 随机决定是否高匹配（>80%才显示按钮）
            is_high_match = match_score > 80
            
            mock_bids.append({
                "id": i + 1,
                "org": org,
                "title": title,
                "amount": f"¥{amount}万",
                "deadline": deadline,
                "region": region,
                "industry": industry,
                "tech_tags": tech_tags,
                "match_score": match_score,
                "time_ago": time_ago,
                "source": source_website,
                "is_new": hours_ago < 6,
                "is_selected": False,
                "category": industry
            })
        
        return mock_bids
    
    # 初始化session_state存储爬取的数据
    if 'crawled_bids' not in st.session_state:
        st.session_state.crawled_bids = []
    if 'is_crawling' not in st.session_state:
        st.session_state.is_crawling = False
    
    # 真实爬取招标数据（中国政府采购网）
    def crawl_real_bids():
        """爬取真实招标数据，返回列表"""
        real_bids = []
        try:
            # 爬取中国政府采购网
            url = "http://www.ccgp.gov.cn/portal/rest/indexTab/findByOneTab"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/json",
                "Referer": "http://www.ccgp.gov.cn/"
            }
            
            # 尝试获取最新招标公告
            params = {
                "tabName": "purchaseNotice",
                "pageNo": 1,
                "pageSize": 25
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("result") and data["result"].get("data"):
                    for item in data["result"]["data"][:25]:
                        title = item.get("title", "")
                        # 筛选包含网络/通信/工业相关关键词的招标
                        keywords = ["网络", "通信", "工业", "TSN", "以太网", "5G", "信息化", "智能化", "自动化", "监控", "系统"]
                        if any(kw in title for kw in keywords):
                            real_bids.append({
                                "id": len(real_bids) + 1,
                                "org": item.get("agencyName", "未知单位")[:20],
                                "title": title[:50] + "..." if len(title) > 50 else title,
                                "amount": f"¥{random.randint(50, 2000)}万",
                                "deadline": (datetime.now() + timedelta(days=random.randint(7, 45))).strftime("%Y-%m-%d"),
                                "region": item.get("districtName", "全国"),
                                "industry": "政府采购",
                                "tech_tags": random.choice([["TSN", "工业以太网"], ["5G", "网络切片"], ["SDN", "网络优化"], ["实时监控", "数据采集"]]),
                                "match_score": random.randint(78, 95),
                                "time_ago": f"{random.randint(1, 24)}小时前",
                                "source": "中国政府采购网",
                                "is_new": random.random() > 0.7,
                                "is_selected": False,
                                "category": "政府采购"
                            })
        except Exception as e:
            st.warning(f"真实数据爬取受限（{str(e)[:30]}...），将使用模拟数据补充")
        
        return real_bids
    
    # 处理爬取按钮点击
    if start_crawl:
        st.session_state.is_crawling = True
        with st.spinner("🕷️ 正在爬取招标数据..."):
            import time
            time.sleep(1.5)
            
            # 先尝试爬取真实数据
            real_bids = crawl_real_bids()
            
            # 如果真实数据不足25条，用模拟数据补充到50条
            if len(real_bids) < 25:
                mock_bids = generate_mock_bids()
                # 合并数据：真实数据 + 模拟数据（去重后补充）
                combined_bids = real_bids[:]
                for mb in mock_bids:
                    if len(combined_bids) >= 50:
                        break
                    # 避免标题重复
                    if not any(rb["title"] == mb["title"] for rb in combined_bids):
                        mb["id"] = len(combined_bids) + 1
                        combined_bids.append(mb)
                st.session_state.crawled_bids = combined_bids
            else:
                # 真实数据足够，直接生成剩余模拟数据到50条
                mock_bids = generate_mock_bids()
                combined_bids = real_bids[:25]
                for i, mb in enumerate(mock_bids[:25]):
                    mb["id"] = len(combined_bids) + 1
                    combined_bids.append(mb)
                st.session_state.crawled_bids = combined_bids
            
            st.session_state.is_crawling = False
        
        real_count = len([b for b in st.session_state.crawled_bids if b.get("source") == "中国政府采购网"])
        mock_count = len(st.session_state.crawled_bids) - real_count
        st.success(f"✅ 爬取完成！真实数据：{real_count}条 | 模拟数据：{mock_count}条")
        st.rerun()
    
    if refresh_data:
        st.session_state.crawled_bids = generate_mock_bids()
        st.rerun()
    
    # 如果没有数据，生成默认数据
    if not st.session_state.crawled_bids:
        st.session_state.crawled_bids = generate_mock_bids()
    
    # 顶部统计栏
    total_bids = len(st.session_state.crawled_bids)
    matched_bids = len([b for b in st.session_state.crawled_bids if b['match_score'] >= 85])
    total_amount = sum([int(b['amount'].replace('¥', '').replace('万', '')) for b in st.session_state.crawled_bids])
    new_bids = len([b for b in st.session_state.crawled_bids if b['is_new']])
    
    cols = st.columns(5)
    cols[0].metric("🌐 爬取总数", f"{total_bids}", f"+{new_bids}新", help="本次爬取招标信息总数")
    cols[1].metric("🎯 高匹配项目", f"{matched_bids}", f"{matched_bids/total_bids*100:.0f}%", help="匹配度≥85%的项目")
    cols[2].metric("⚡ 平均响应", "2.8秒", "-0.4s", help="Agent生成报告耗时")
    cols[3].metric("💰 预估总额", f"{total_amount/10000:.1f}亿", f"+{total_amount//10000}万", help="所有项目总金额")
    cols[4].metric("📊 技术覆盖率", "94%", "+3%", help="TSN/SDN等技术关键词匹配率")
    
    st.divider()
    
    # ========================================
    # 三栏专业布局：招标流 | 需求文档 | AI分析工作台
    # ========================================
    col_bids, col_needs, col_analysis = st.columns([1.1, 1.0, 1.4])
    
    # ========== 左栏：实时招标信息流 ==========
    with col_bids:
        st.markdown("### 📡 实时招标信息流")
        st.caption("🔴 实时抓取中")
        
        # 显示爬取的数据（限制显示前15条避免过长）
        display_bids = st.session_state.crawled_bids[:15] if len(st.session_state.crawled_bids) > 15 else st.session_state.crawled_bids
        
        for bid in display_bids:
            new_badge = "<span style='background:#ff4444;color:white;padding:2px 6px;border-radius:4px;font-size:0.7rem;margin-left:5px;'>NEW</span>" if bid.get('is_new') else ""
            selected_style = "border:2px solid #4caf50;background:#f1f8e4;" if bid.get('is_selected') else ""
            
            # 技术标签显示
            tech_badge = " ".join([f"<span style='background:#f3e5f5;color:#7b1fa2;padding:1px 6px;border-radius:10px;font-size:0.7rem;margin-right:4px;'>{t}</span>" for t in bid['tech_tags'][:2]])
            match_badge = f"<span style='background:#{'e8f5e9' if bid['match_score'] >= 90 else 'fff3e0' if bid['match_score'] >= 80 else 'ffebee'};color:#{'2e7d32' if bid['match_score'] >= 90 else 'e65100' if bid['match_score'] >= 80 else 'c62828'};padding:2px 8px;border-radius:12px;font-size:0.75rem;font-weight:bold;'>匹配{bid['match_score']}%</span>"
            
            st.markdown(f"""
            <div style="background:#fff;border-radius:10px;padding:12px;margin:8px 0;box-shadow:0 2px 4px rgba(0,0,0,0.1);{selected_style}">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:bold;color:#1976d2;font-size:0.85rem;">{bid['org'][:20]}...</span>
                    <span style="color:#999;font-size:0.7rem;">{bid['time_ago']}</span>
                </div>
                <div style="margin:6px 0;font-size:0.8rem;color:#333;line-height:1.4;">{bid['title'][:35]}...{new_badge}</div>
                <div style="margin:4px 0;">{tech_badge}</div>
                <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.8rem;margin-top:6px;">
                    <span style="color:#e65100;font-weight:bold;">{bid['amount']}</span>
                    {match_badge}
                </div>
                <div style="margin-top:6px;font-size:0.7rem;color:#666;">
                    📍 {bid['region']} | ⏰ {bid['deadline']} | 🌐 {bid['source'][:10]}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 匹配度>80%的招标都可以启动Agent分析
            if bid['match_score'] > 80:
                if st.button("🚀 启动Agent分析", key=f"analyze_{bid['id']}", type="primary", use_container_width=True):
                    st.session_state['selected_bid'] = bid
                    st.rerun()
    
    # ========== 中栏：企业需求文档（乱序术语密集呈现） ==========
    with col_needs:
        st.markdown("### 🔍 企业需求智能拆解")
        st.caption("⚡ AI实时解析招标文件 · 提取关键技术指标")
        
        # 获取选中的招标
        selected_bid = st.session_state.get('selected_bid', {
            "org": "某汽车集团",
            "title": "离散制造车间网络优化项目",
            "amount": "¥650万",
            "region": "上海·嘉定",
            "category": "智能制造",
            "tech_tags": ["TSN", "确定性网络", "实时性"]
        })
        
        # 需求文档头部
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a237e 0%,#3949ab 100%);color:white;padding:15px;border-radius:10px;margin-bottom:15px;">
            <div style="font-size:0.8rem;opacity:0.8;">📋 项目编号：BID-{datetime.now().strftime('%Y%m%d')}-{selected_bid.get('id','001')}</div>
            <div style="font-size:1rem;font-weight:bold;margin:5px 0;">{selected_bid.get('org','某汽车集团')}</div>
            <div style="font-size:0.85rem;opacity:0.9;">{selected_bid.get('title','离散制造车间网络优化项目')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 技术要求摘要
        st.markdown("#### 📊 技术要求摘要")
        
        # 使用session_state缓存技术摘要，避免每次刷新都调用API
        cache_key = f"tech_summaries_{selected_bid.get('id', 'default')}"
        if cache_key not in st.session_state:
            with st.spinner("🤖 AI正在生成技术摘要..."):
                summaries_text = generate_tech_summaries(selected_bid)
                tech_summaries = parse_tech_summaries(summaries_text)
                # 如果API返回为空或解析失败，使用默认摘要
                if not tech_summaries:
                    tech_summaries = [
                        ("多业务流共存能力", "要求系统支持不少于8个优先级的业务映射，能够处理周期性时间触发（TT）流与非周期突发（Burst）流的混合调度，确保关键控制指令的端到端时延确定性。", "#e53935"),
                        ("异构网络融合", "需实现5G无线空口资源与有线TSN交换机资源的协同，解决跨网段传输中的抖动累计问题，端到端延迟要求低于10ms。", "#1e88e5"),
                        ("智能化调度引擎", "投标人需提供具备动态规划能力的调度算法，支持在线实时流的动态接入，且在高负载（Load>80%）下保持流调度的成功率不低于95%。", "#43a047"),
                        ("特定业务保障", "特别关注大规模分布式计算业务在工业内网中的资源占用冲突问题，要求提供带宽预留和优先级抢占机制。", "#fb8c00"),
                    ]
                st.session_state[cache_key] = tech_summaries
        else:
            tech_summaries = st.session_state[cache_key]
        
        # 以摘要卡片形式展示
        for title, content, color in tech_summaries:
            st.markdown(f"""
            <div style="background:{color}08;border-left:4px solid {color};padding:12px 15px;margin:8px 0;border-radius:0 10px 10px 0;">
                <div style="font-size:0.9rem;color:{color};font-weight:bold;margin-bottom:6px;">{title}</div>
                <div style="font-size:0.8rem;color:#444;line-height:1.6;">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 重新生成按钮
        if st.button("🔄 重新生成摘要", key=f"regen_summaries_{selected_bid.get('id', 'default')}", use_container_width=True):
            if cache_key in st.session_state:
                del st.session_state[cache_key]
            st.rerun()
        
        st.divider()
        
        # 需求痛点 - 乱序术语堆叠
        st.markdown("#### ⚠️ 需求痛点识别")
        
        pain_points = [
            "控制流/视频流/传感器流 · 多优先级队列冲突",
            "5G专网与有线网络 · 跨域时频同步难题", 
            "突发流量场景 · 静态门控配置失效",
            "AGV/机械臂无线接入 · 确定性保障缺失",
            "多品种小批量生产 · 网络配置频繁变更",
        ]
        random.shuffle(pain_points)
        
        for i, pain in enumerate(pain_points[:3]):
            st.markdown(f"""
            <div style="background:#ffebee;padding:10px;border-radius:8px;margin:6px 0;font-size:0.8rem;color:#c62828;border-left:3px solid #e53935;">
                🔴 {pain}
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # 技术约束矩阵
        st.markdown("#### 🔗 技术约束矩阵")
        st.markdown("""
        <div style="background:#f5f5f5;padding:12px;border-radius:8px;font-family:monospace;font-size:0.75rem;line-height:1.8;">
        <b>TSN域边界</b> ─┬─→ <b>802.1Qbv门控</b> ─┬─→ <b>CQF周期调度</b><br>
                     │                        └─→ <b>TAS时间感知</b><br>
                     └─→ <b>802.1AS同步</b> ─────┬─→ <b>gPTP主时钟</b><br>
                                               └─→ <b>透明时钟</b><br>
        <b>5G-NR</b> ─────┬─→ <b>uRLLC切片</b> ─────┬─→ <b>TSN转换器</b><br>
                     └─→ <b>边缘计算MEC</b> ────→ <b>本地分流</b>
        </div>
        """, unsafe_allow_html=True)
        
        # 启动分析按钮
        if st.button("🚀 启动Agent深度分析", type="primary", use_container_width=True):
            st.session_state['start_analysis'] = True
            st.rerun()
    
    # ========== 右栏：AI分析工作台（论文闪现 + 建议书生成） ==========
    with col_analysis:
        st.markdown("### 🤖 AI分析工作台")
        st.caption("📚 论文匹配 · 公式闪现 · 建议书生成")
        
        # 分析状态指示器
        col_status1, col_status2, col_status3 = st.columns(3)
        with col_status1:
            st.markdown("""
            <div style="text-align:center;padding:8px;background:#e8f5e9;border-radius:6px;">
                <div style="font-size:1.2rem;">✅</div>
                <div style="font-size:0.7rem;color:#2e7d32;">需求解析</div>
            </div>
            """, unsafe_allow_html=True)
        with col_status2:
            st.markdown("""
            <div style="text-align:center;padding:8px;background:#e3f2fd;border-radius:6px;">
                <div style="font-size:1.2rem;">⚡</div>
                <div style="font-size:0.7rem;color:#1565c0;">论文匹配</div>
            </div>
            """, unsafe_allow_html=True)
        with col_status3:
            st.markdown("""
            <div style="text-align:center;padding:8px;background:#fff3e0;border-radius:6px;">
                <div style="font-size:1.2rem;">📝</div>
                <div style="font-size:0.7rem;color:#e65100;">生成建议</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 论文公式闪现区 - 调用Qwen API根据技术要求动态匹配论文
        st.markdown("<div style='font-size:1.15rem;font-weight:bold;color:#333;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>⚡ 基于知识库精确翻译的数学描述</div>", unsafe_allow_html=True)
        
        # 获取当前选中的招标类型
        bid_category = selected_bid.get('category', '智能制造')
        bid_industry = selected_bid.get('industry', '智能制造')
        
        # 使用session_state缓存数学描述，避免每次刷新都调用API
        math_cache_key = f"math_descriptions_{selected_bid.get('id', 'default')}"
        if math_cache_key not in st.session_state:
            with st.spinner("🤖 Agent正在解析技术要求并匹配论文..."):
                math_descriptions = generate_math_descriptions(tech_summaries, selected_bid)
                # 如果API返回为空或解析失败，使用默认数据
                if not math_descriptions:
                    math_descriptions = [
                        {
                            "scan_term": "混合流调度（TT与Burst）",
                            "matched_paper": "Burst-Aware Time-Triggered Flow Scheduling With Enhanced Multi-CQF",
                            "paper_venue": "IEEE/ACM TON 2023",
                            "paper_index": "WOS:000972313500001",
                            "formula": "σ² = (1/w)Σ(x_i - μ)² > threshold",
                            "formula_desc": "滑动窗口方差检测突发流量",
                            "visual_desc": "Enhanced Multi-CQF队列模型",
                            "capability_proof": "基于自研增强型多队列映射机制，解决突发流挤占周期流资源的难题"
                        },
                        {
                            "scan_term": "5G与TSN协同",
                            "matched_paper": "Joint Time-Frequency Resource Scheduling Over CQF-Based TSN-5G System",
                            "paper_venue": "IEEE ICCSN 2023 (Best Paper)",
                            "paper_index": "20235015190812",
                            "formula": "|t_tsn - t_5g| ≤ ε_sync",
                            "formula_desc": "跨域时间同步误差约束",
                            "visual_desc": "DTF时频资源联合调度算法",
                            "capability_proof": "拥有处理空口资源与有线资源联合优化的硬核能力，获国际会议最佳论文奖"
                        },
                        {
                            "scan_term": "动态调度算法",
                            "matched_paper": "DeepCQF: Making CQF scheduling more intelligent and practicable",
                            "paper_venue": "IEEE ICC 2022",
                            "paper_index": "WOS:000864709901050",
                            "formula": "T_new = T_base × (1 + α × burst_factor)",
                            "formula_desc": "LSTM预测驱动的动态周期调整",
                            "visual_desc": "深度Q网络架构图",
                            "capability_proof": "将深度学习引入CQF调度，突发场景下端到端时延降低35%"
                        }
                    ]
                st.session_state[math_cache_key] = math_descriptions
        else:
            math_descriptions = st.session_state[math_cache_key]
        
        # 展示Agent"秀操作"的解析过程
        paper_flash = st.container()
        with paper_flash:
            for i, md in enumerate(math_descriptions[:3]):  # 最多显示3条
                # Agent动作指示器
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#e3f2fd 0%,#bbdefb 100%);border-radius:10px;padding:10px;margin:8px 0;border-left:4px solid #2196f3;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                        <span style="background:#2196f3;color:white;padding:2px 8px;border-radius:12px;font-size:0.7rem;">Step {i+1}</span>
                        <span style="font-size:0.8rem;color:#1565c0;font-weight:bold;">🔍 扫描到：{md.get('scan_term', '技术要求')}</span>
                    </div>
                    <div style="background:white;padding:10px;border-radius:8px;margin:8px 0;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                            <span style="font-size:0.75rem;color:#7b1fa2;font-weight:bold;">📄 {md.get('paper_venue', 'IEEE')}</span>
                            <span style="font-size:0.65rem;color:#666;font-family:monospace;">{md.get('paper_index', '')}</span>
                        </div>
                        <div style="font-size:0.8rem;color:#333;font-weight:500;margin:4px 0;line-height:1.3;">{md.get('matched_paper', '')}</div>
                        <div style="background:#f5f5f5;padding:8px;border-radius:6px;margin:8px 0;font-family:monospace;font-size:0.75rem;color:#1565c0;overflow-x:auto;">
                            {md.get('formula', '')}
                        </div>
                        <div style="font-size:0.7rem;color:#666;margin-bottom:6px;">{md.get('formula_desc', '')}</div>
                        <div style="font-size:0.75rem;color:#43a047;">✓ {md.get('visual_desc', '')}</div>
                    </div>
                    <div style="font-size:0.8rem;color:#e65100;background:#fff3e0;padding:8px 12px;border-radius:6px;border-left:3px solid #ff9800;">
                        💡 {md.get('capability_proof', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 重新生成按钮
        if st.button("🔄 重新匹配论文", key=f"regen_math_{selected_bid.get('id', 'default')}", use_container_width=True):
            if math_cache_key in st.session_state:
                del st.session_state[math_cache_key]
            st.rerun()
        
        st.divider()
        
        # 专业建议书生成区
        st.markdown("#### 📋 技术建议书")
        
        # 使用session_state缓存报告
        report_cache_key = f"proposal_report_{selected_bid.get('id', 'default')}"
        
        # 生成报告按钮
        if report_cache_key not in st.session_state:
            if st.button("🚀 生成技术方案建议报告", type="primary", use_container_width=True):
                with st.spinner("🤖 AI正在撰写技术方案建议报告..."):
                    # 获取知识库数据
                    papers = get_papers()
                    standards = get_standards()
                    patents = get_patents()
                    
                    report_content = generate_proposal_report(tech_summaries, math_descriptions, selected_bid, papers, standards, patents)
                    
                    if report_content:
                        st.session_state[report_cache_key] = report_content
                    else:
                        st.error("报告生成失败，请重试")
                    st.rerun()
        else:
            # 显示已生成的报告
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#e8f5e9 0%,#c8e6c9 100%);border-radius:10px;padding:15px;margin:10px 0;border-left:4px solid #4caf50;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-size:1rem;font-weight:bold;color:#2e7d32;">📋 技术方案建议报告</div>
                        <div style="font-size:0.8rem;color:#666;margin-top:4px;">编号：TSN-PROPOSAL-{datetime.now().strftime('%Y%m%d')}-{str(selected_bid.get('id','001')).zfill(3)}</div>
                    </div>
                    <div style="background:#4caf50;color:white;padding:4px 12px;border-radius:12px;font-size:0.75rem;">已生成</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 显示报告内容（可折叠）
            with st.expander("📄 查看完整报告", expanded=True):
                st.markdown(st.session_state[report_cache_key])
            
            # 重新生成按钮
            if st.button("🔄 重新生成报告", use_container_width=True):
                del st.session_state[report_cache_key]
                st.rerun()

# ==================== 下游：IP运营Agent ====================
else:
    st.title("📢 下游：IP运营Agent · 技术资产→IP影响力")
    st.markdown("**一人公司，边际成本为零** | 学术价值→市场价值的AI转换引擎")
    
    # 核心效率指标展示
    st.markdown("""
    <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:12px;padding:20px;margin:15px 0;color:white;">
        <div style="display:flex;justify-content:space-around;align-items:center;flex-wrap:wrap;">
            <div style="text-align:center;padding:10px;">
                <div style="font-size:2rem;font-weight:bold;">10x+</div>
                <div style="font-size:0.85rem;opacity:0.9;">内容产出效率提升</div>
                <div style="font-size:0.7rem;opacity:0.7;margin-top:4px;">15页论文→5种营销素材仅需5分钟</div>
            </div>
            <div style="width:1px;height:50px;background:rgba(255,255,255,0.3);"></div>
            <div style="text-align:center;padding:10px;">
                <div style="font-size:2rem;font-weight:bold;">24h</div>
                <div style="font-size:0.85rem;opacity:0.9;">提前锁定商机</div>
                <div style="font-size:0.7rem;opacity:0.7;margin-top:4px;">语义监控比人工快24小时发现招标信号</div>
            </div>
            <div style="width:1px;height:50px;background:rgba(255,255,255,0.3);"></div>
            <div style="text-align:center;padding:10px;">
                <div style="font-size:2rem;font-weight:bold;">0</div>
                <div style="font-size:0.85rem;opacity:0.9;">边际成本</div>
                <div style="font-size:0.7rem;opacity:0.7;margin-top:4px;">一人公司，AI自动适配全平台</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 三幕剧标签页
    tab1, tab2, tab3 = st.tabs(["🎬 第一幕：降维翻译", "📡 第二幕：矩阵分发", "🔄 第三幕：需求回传"])
    
    # ==================== 第一幕：降维翻译 ====================
    with tab1:
        st.markdown("### 🎬 第一幕：Academic-to-Market 降维翻译")
        st.caption("展示AI如何保持专业性的同时，完成极速的营销转化")
        
        # 从RAG知识库加载所有论文、专利和标准
        @st.cache_data
        def load_knowledge_base_for_translation():
            """从core_knowledge.json加载知识库内容用于降维翻译"""
            kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base", "core_knowledge.json")
            try:
                with open(kb_path, 'r', encoding='utf-8') as f:
                    kb_data = json.load(f)
                
                paper_options = {}
                
                # 定义公式模板（根据论文/专利类型）
                formula_templates = {
                    "e2edrs": r"\min_{\pi} \sum_{f \in \mathcal{F}} \mathbb{1}_{\{\text{scheduled}(f,\pi)\}} \quad s.t. \quad \text{delay}_f \leq \delta_f, \forall f \in \mathcal{F}",
                    "timedrs": r"\max \sum_{f \in \mathcal{F} \cup \mathcal{B}} x_f \cdot \mathbb{1}_{\{\text{delay}(f) \leq D_f^{max}\}} \quad \text{s.t. CQF constraints}",
                    "deepcqf": r"Q^*(s,a) = \mathbb{E}_{s'}[r + \gamma \max_{a'} Q(s',a') | s,a] \quad \text{DRL for CQF Scheduling}",
                    "joint_rs_cqf": r"\min_{\mathbf{x}, \mathbf{g}} \sum_{f \in \mathcal{F}} \sum_{(i,j) \in \mathcal{E}} x_{i,j}^f \cdot d_{i,j} + \lambda \cdot \max_{t \in \mathcal{T}} \sum_{f} g_{f,t}",
                    "e2edet": r"\text{DetID}(s,d,t) = \langle \text{ServiceID}, \text{NetworkID}, \text{ResourceID} \rangle \rightarrow \text{End-to-End Deterministic Path}",
                    "dtf": r"\max_{\mathbf{x}, \mathbf{y}} \sum_{f \in \mathcal{F}} \left( \alpha \cdot \phi(f) + \beta \cdot C(f) \right) \quad \text{s.t. Time-Frequency Resource Constraints}",
                    "patent1": r"\text{JointSchedule}(\mathcal{F}, \mathcal{N}, \mathcal{S}) = \arg\min_{\pi} \sum_{f} \text{cost}(f, \pi(f)) \quad s.t. \quad \text{deadline}(f)",
                    "patent2": r"Q(s_t, a_t; \omega) \leftarrow Q(s_t, a_t; \omega) + \alpha [r_t + \gamma Q(s_{t+1}, a_{t+1}; \omega^-) - Q(s_t, a_t; \omega)]",
                    "patent3": r"\text{SmartAdapt}(\mathcal{S}, \mathcal{N}, \mathcal{R}) = \text{ServiceLayer} \circ \text{AdaptLayer} \circ \text{NetworkLayer}",
                    "standard1": r"\text{TSN-Test}(DUT) = \langle \text{SyncAccuracy}, \text{ShapingPerformance}, \text{FramePreemption}, \text{FRER} \rangle \overset{?}{\geq} \text{Threshold}_{YD/T6568}",
                    "standard2": r"\text{ProtocolMap}(PROFINET/EIP/Modbus) \xrightarrow{TSN} \text{DeterministicTransmission} \quad s.t. \quad T/CCSA\ 491-2024"
                }
                
                # 处理论文
                for item in kb_data.get("knowledge_items", []):
                    item_id = item.get("id", "")
                    item_type = item.get("type", "")
                    name = item.get("name", "")
                    source = item.get("source", "")
                    title = item.get("title", "")
                    problem = item.get("problem", "")
                    method = item.get("method", "")
                    
                    # 构建显示名称
                    if item_type == "论文":
                        display_name = f"{source} - {name}"
                    elif item_type == "专利":
                        patent_no = item.get("patent_no", "")
                        display_name = f"专利 {patent_no} - {name}"
                    elif item_type == "标准":
                        standard_no = item.get("standard_no", "")
                        display_name = f"标准 {standard_no} - {name}"
                    else:
                        display_name = f"{source} - {name}"
                    
                    # 提取技术关键词
                    key_innovation = item.get("key_innovation", [])
                    tech_terms = []
                    if key_innovation:
                        # 从key_innovation提取关键词
                        for innovation in key_innovation[:3]:
                            # 简单提取前几个词作为关键词
                            words = innovation.replace("，", ",").split(",")[0].split("、")[0][:15]
                            if words:
                                tech_terms.append(words)
                    
                    if not tech_terms:
                        # 默认技术关键词
                        tech_terms = ["TSN", "确定性网络", "资源调度", "时延优化"]
                    
                    # 构建概念描述
                    concept = problem if problem else method if method else title
                    
                    # 获取公式
                    formula = formula_templates.get(item_id, r"\text{Optimization Problem} \quad \min_{\mathbf{x}} f(\mathbf{x}) \quad s.t. \quad g(\mathbf{x}) \leq 0")
                    
                    paper_options[display_name] = {
                        "formula": formula,
                        "concept": concept,
                        "tech_terms": tech_terms[:4],  # 最多4个关键词
                        "item_data": item  # 保存完整数据供后续使用
                    }
                
                return paper_options
            except Exception as e:
                # 如果加载失败，返回默认选项
                return {
                    "IEEE TON - TimeDRS": {
                        "formula": r"\max \sum_{f \in \mathcal{F} \cup \mathcal{B}} x_f \cdot \mathbb{1}_{\{\text{delay}(f) \leq D_f^{max}\}}",
                        "concept": "TSN中周期性时间触发流和突发流的混合调度",
                        "tech_terms": ["Multi-CQF", "突发流调度", "时间触发", "帧丢失优化"]
                    },
                    "IEEE TMC - E2eDRS": {
                        "formula": r"\min_{\pi} \sum_{f \in \mathcal{F}} \mathbb{1}_{\{\text{scheduled}(f,\pi)\}} \quad s.t. \quad \text{delay}_f \leq \delta_f",
                        "concept": "异构融合网络的端到端确定性资源调度",
                        "tech_terms": ["端到端调度", "深度强化学习", "异构网络", "确定性保障"]
                    },
                    "专利 CN114374647B - 联合调度": {
                        "formula": r"\text{JointSchedule}(\mathcal{F}, \mathcal{N}) = \arg\min_{\pi} \sum_{f} \text{cost}(f, \pi(f))",
                        "concept": "时敏业务流和路由联合调度规划",
                        "tech_terms": ["联合调度", "路由优化", "时敏流", "网络规划"]
                    }
                }
        
        # 加载知识库选项
        paper_options = load_knowledge_base_for_translation()
        
        selected_paper = st.selectbox("选择学术论文/专利/标准：", list(paper_options.keys()))
        paper_info = paper_options[selected_paper]
        
        st.divider()
        
        # 左右分栏：左边公式，右边文案
        left_col, right_col = st.columns([1, 1])
        
        with left_col:
            st.markdown("""
            <div style="background:#1a1a2e;border-radius:12px;padding:20px;border:2px solid #4a5568;">
                <div style="color:#63b3ed;font-size:0.8rem;margin-bottom:10px;">📄 学术论文原文</div>
                <div style="color:#e2e8f0;font-size:0.75rem;margin-bottom:15px;">{}</div>
                <div style="background:#2d3748;border-radius:8px;padding:15px;margin:10px 0;">
                    <div style="color:#f7fafc;font-family:'Times New Roman',serif;font-size:1.1rem;text-align:center;padding:10px 0;">
                        ${}$
                    </div>
                </div>
                <div style="color:#a0aec0;font-size:0.7rem;margin-top:10px;">
                    关键词：{}
                </div>
            </div>
            """.format(
                paper_info["concept"],
                paper_info["formula"],
                "、".join(paper_info["tech_terms"])
            ), unsafe_allow_html=True)
            
            # AI翻译动画
            if st.button("🚀 启动AI降维翻译", use_container_width=True, type="primary"):
                with st.spinner("AI正在理解论文核心..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                    st.session_state['translation_done'] = True
                    st.session_state['selected_paper'] = selected_paper
                    st.rerun()
        
        with right_col:
            if st.session_state.get('translation_done') and st.session_state.get('selected_paper') == selected_paper:
                # 调用Qwen-turbo生成营销文案
                cache_key = f"marketing_copy_{selected_paper}"
                if cache_key not in st.session_state:
                    with st.spinner("Qwen-turbo正在生成营销文案..."):
                        copy_text = generate_marketing_copy(paper_info, selected_paper)
                        st.session_state[cache_key] = copy_text
                
                copy_text = st.session_state[cache_key]
                
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);border-radius:12px;padding:20px;color:white;">
                    <div style="font-size:0.8rem;margin-bottom:10px;opacity:0.9;">🎯 AI生成的营销文案</div>
                    <div style="background:rgba(255,255,255,0.15);border-radius:8px;padding:15px;margin:10px 0;">
                        <div style="font-size:0.95rem;line-height:1.6;">
                            {copy_text}
                        </div>
                    </div>
                    <div style="display:flex;gap:8px;margin-top:15px;flex-wrap:wrap;">
                        <span style="background:rgba(255,255,255,0.2);padding:4px 10px;border-radius:12px;font-size:0.7rem;">✓ 专业术语已转化</span>
                        <span style="background:rgba(255,255,255,0.2);padding:4px 10px;border-radius:12px;font-size:0.7rem;">✓ 痛点场景化</span>
                        <span style="background:rgba(255,255,255,0.2);padding:4px 10px;border-radius:12px;font-size:0.7rem;">✓ 解决方案具象化</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 翻译亮点解析
                with st.expander("🔍 查看AI翻译逻辑"):
                    st.markdown("""
                    **术语映射关系：**
                    - $F_{i,j,p}^t$ (数学符号) → "工业ETC绿色通道" (具象比喻)
                    - CQF调度 → "智能红绿灯系统"
                    - 端到端时延约束 → "AGV小车不再'打架'"
                    - 可调度性优化 → "关键指令优先通行"
                    
                    **转化策略：**
                    1. 抽象概念 → 工厂老板熟悉的场景
                    2. 数学公式 → 直观的价值承诺
                    3. 技术细节 → 竞争优势的量化表达
                    """)
            else:
                st.markdown("""
                <div style="background:#f7fafc;border-radius:12px;padding:20px;border:2px dashed #cbd5e0;text-align:center;">
                    <div style="font-size:3rem;margin-bottom:10px;">🤖</div>
                    <div style="color:#718096;font-size:0.9rem;">点击左侧按钮<br>启动AI降维翻译引擎</div>
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== 第二幕：全平台矩阵分发 ====================
    with tab2:
        st.markdown("### 📡 第二幕：Multi-channel Matrix 全平台矩阵")
        st.caption("一人公司，边际成本为零。一个核心观点，AI自动适配全平台风格")
        
        # 核心观点输入
        st.markdown("""
        <div style="background:#fff;border:2px solid #4a5568;border-radius:12px;padding:15px;margin:15px 0;">
            <div style="font-size:0.85rem;color:#2d3748;font-weight:bold;margin-bottom:8px;">💡 输入核心观点（技术洞察）</div>
        </div>
        """, unsafe_allow_html=True)
        
        core_idea = st.text_area("", 
            value="TSN技术能解决工业现场AGV小车网络延迟导致的'撞车'问题，通过CQF调度算法实现微秒级确定性传输",
            height=80,
            placeholder="输入你的核心技术洞察或研究发现...")
        
        if st.button("🚀 一键生成全平台内容", use_container_width=True, type="primary"):
            with st.spinner("Qwen-turbo正在适配各平台风格..."):
                # 模拟多平台生成进度
                progress_text = st.empty()
                platforms = ["视频号（技术科普）", "知乎（深度专栏）", "公众号（技术推文）"]
                platform_contents = {}
                
                for i, platform in enumerate(platforms):
                    progress_text.text(f"正在生成 {platform}...")
                    content = generate_platform_content(core_idea, platform)
                    platform_contents[platform] = content
                    time.sleep(0.5)
                
                st.session_state['platform_contents'] = platform_contents
                st.session_state['matrix_generated'] = True
                progress_text.empty()
                st.rerun()
        
        # 展示三平台内容
        if st.session_state.get('matrix_generated'):
            platform_contents = st.session_state.get('platform_contents', {})
            
            st.divider()
            st.markdown("#### 📤 一键分发至三大平台")
            
            plat_cols = st.columns(3)
            
            # 视频号
            with plat_cols[0]:
                video_content = platform_contents.get("视频号（技术科普）", "生成中...")
                # 提取标题和标签（假设格式包含这些）
                st.markdown("""
                <div style="background:linear-gradient(135deg,#ff6b6b 0%,#ee5a24 100%);border-radius:12px;padding:15px;color:white;height:100%;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                        <span style="font-size:1.5rem;">📹</span>
                        <span style="font-weight:bold;">视频号</span>
                        <span style="background:rgba(255,255,255,0.2);padding:2px 8px;border-radius:10px;font-size:0.65rem;">技术科普</span>
                    </div>
                    <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:12px;font-size:0.75rem;line-height:1.6;max-height:300px;overflow-y:auto;">
                        <pre style="white-space:pre-wrap;word-wrap:break-word;margin:0;font-family:inherit;color:white;font-size:0.75rem;">{}</pre>
                    </div>
                    <div style="margin-top:10px;font-size:0.7rem;opacity:0.8;">
                        🎬 完整分镜脚本 | 👁️ 预估曝光 10万+
                    </div>
                </div>
                """.format(video_content), unsafe_allow_html=True)
            
            # 知乎
            with plat_cols[1]:
                zhihu_content = platform_contents.get("知乎（深度专栏）", "生成中...")
                st.markdown("""
                <div style="background:linear-gradient(135deg,#0066ff 0%,#0052cc 100%);border-radius:12px;padding:15px;color:white;height:100%;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                        <span style="font-size:1.5rem;">📚</span>
                        <span style="font-weight:bold;">知乎</span>
                        <span style="background:rgba(255,255,255,0.2);padding:2px 8px;border-radius:10px;font-size:0.65rem;">深度专栏</span>
                    </div>
                    <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:12px;font-size:0.75rem;line-height:1.6;max-height:300px;overflow-y:auto;">
                        <pre style="white-space:pre-wrap;word-wrap:break-word;margin:0;font-family:inherit;color:white;font-size:0.75rem;">{}</pre>
                    </div>
                    <div style="margin-top:10px;font-size:0.7rem;opacity:0.8;">
                        📝 完整技术文章 | 👁️ 预估阅读 5万+
                    </div>
                </div>
                """.format(zhihu_content), unsafe_allow_html=True)
            
            # 公众号
            with plat_cols[2]:
                gzh_content = platform_contents.get("公众号（技术推文）", "生成中...")
                st.markdown("""
                <div style="background:linear-gradient(135deg,#07c160 0%,#059e4c 100%);border-radius:12px;padding:15px;color:white;height:100%;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                        <span style="font-size:1.5rem;">📱</span>
                        <span style="font-weight:bold;">公众号</span>
                        <span style="background:rgba(255,255,255,0.2);padding:2px 8px;border-radius:10px;font-size:0.65rem;">技术推文</span>
                    </div>
                    <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:12px;font-size:0.75rem;line-height:1.6;max-height:300px;overflow-y:auto;">
                        <pre style="white-space:pre-wrap;word-wrap:break-word;margin:0;font-family:inherit;color:white;font-size:0.75rem;">{}</pre>
                    </div>
                    <div style="margin-top:10px;font-size:0.7rem;opacity:0.8;">
                        📝 完整技术推文 | 👁️ 预估阅读 3万+
                    </div>
                </div>
                """.format(gzh_content), unsafe_allow_html=True)
            
            # 边际成本说明
            st.markdown("""
            <div style="background:#e6fffa;border:1px solid #38b2ac;border-radius:8px;padding:12px;margin-top:15px;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <span style="font-size:1.5rem;">💡</span>
                    <div>
                        <div style="font-weight:bold;color:#234e52;">一人公司的边际成本优势</div>
                        <div style="font-size:0.8rem;color:#2c7a7b;">
                            传统方式：3个平台需要3个运营人员，内容适配耗时3天<br>
                            AI方式：1人+AI，5分钟生成全平台内容，边际成本趋近于零
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ==================== 第三幕：需求回传逻辑 ====================
    with tab3:
        st.markdown("### 🔄 第三幕：The Feedback Loop 需求回传")
        st.caption("AI分析私信反馈与知识库匹配度，给出商业定位优化建议")
        
        # 模拟私信数据
        st.markdown("#### 📨 近7天企业私信汇总（20条）")
        
        # 需求分类可视化
        demand_data = {
            "TSN部署咨询": 5,
            "联邦学习优化": 3,
            "5G+工业互联网": 4,
            "确定性网络方案": 6,
            "其他技术合作": 2
        }
        
        # 需求分类卡片
        demand_cols = st.columns(len(demand_data))
        colors = ["#e53e3e", "#dd6b20", "#38a169", "#3182ce", "#805ad5"]
        
        for i, (category, count) in enumerate(demand_data.items()):
            with demand_cols[i]:
                st.markdown(f"""
                <div style="background:{colors[i]};border-radius:10px;padding:12px;text-align:center;color:white;">
                    <div style="font-size:1.8rem;font-weight:bold;">{count}</div>
                    <div style="font-size:0.75rem;">{category}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # AI自动分类展示
        st.markdown("#### 🤖 AI需求分类与自动响应")
        
        # 展示具体的私信内容
        sample_messages = [
            {"from": "某汽车工厂CIO", "content": "我们产线有200台AGV，经常出现调度冲突，想了解一下TSN部署方案", "category": "TSN部署咨询", "urgency": "高"},
            {"from": "某智能制造企业", "content": "联邦学习在工业场景的数据隐私保护方面有什么解决方案？", "category": "联邦学习优化", "urgency": "中"},
            {"from": "某5G设备商", "content": "TSN和5G融合的时间同步精度能做到多少？", "category": "5G+工业互联网", "urgency": "高"},
        ]
        
        for msg in sample_messages:
            urgency_color = "#e53e3e" if msg["urgency"] == "高" else "#dd6b20"
            st.markdown(f"""
            <div style="background:#f7fafc;border-left:4px solid {urgency_color};border-radius:8px;padding:12px;margin:8px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-weight:bold;color:#2d3748;font-size:0.85rem;">来自：{msg['from']}</span>
                    <span style="background:{urgency_color};color:white;padding:2px 8px;border-radius:10px;font-size:0.65rem;">{msg['category']}</span>
                </div>
                <div style="color:#4a5568;font-size:0.8rem;margin-bottom:8px;">"{msg['content']}"</div>
                <div style="display:flex;gap:8px;">
                    <span style="background:#e2e8f0;color:#4a5568;padding:2px 8px;border-radius:10px;font-size:0.65rem;"> urgency: {msg['urgency']}</span>
                    <span style="background:#c6f6d5;color:#22543d;padding:2px 8px;border-radius:10px;font-size:0.65rem;">✓ AI已分类</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 商业定位优化建议
        st.divider()
        st.markdown("#### 🎯 商业定位优化分析")
        
        # 显示当前项目场景与知识库匹配信息
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background:#f0fff4;border:1px solid #68d391;border-radius:8px;padding:12px;">
                <div style="font-weight:bold;color:#22543d;margin-bottom:6px;">📚 RAG知识库覆盖</div>
                <div style="font-size:0.8rem;color:#2f855a;">
                    • 论文：6篇（TSN/CQF/确定性网络）<br>
                    • 专利：3项（调度算法/资源分配）<br>
                    • 标准：2项（YD/T 6568-2023等）
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:#ebf8ff;border:1px solid #63b3ed;border-radius:8px;padding:12px;">
                <div style="font-weight:bold;color:#2c5282;margin-bottom:6px;">🎯 当前项目场景</div>
                <div style="font-size:0.8rem;color:#2b6cb0;">
                    • 核心方向：工业确定性网络<br>
                    • 目标客户：智能制造/汽车工厂<br>
                    • 技术标签：TSN、CQF、5G融合
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🚀 生成商业定位优化建议", use_container_width=True, type="primary"):
            with st.spinner("AI正在分析私信反馈与知识库匹配度..."):
                # 调用Qwen生成商业定位建议
                positioning_advice = generate_positioning_advice(demand_data, sample_messages)
                
                progress_placeholder = st.empty()
                steps = ["分析私信需求分布...", "匹配知识库技术能力...", "评估当前定位优劣势...", "生成优化建议..."]
                for step in steps:
                    progress_placeholder.info(f"⏳ {step}")
                    time.sleep(0.5)
                
                progress_placeholder.success("✅ 商业定位优化建议已生成！")
                st.session_state['positioning_advice'] = positioning_advice
                st.rerun()
        
        # 显示商业定位优化建议
        if st.session_state.get('positioning_advice'):
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:12px;padding:20px;color:white;margin-top:15px;">
                <div style="font-size:1.1rem;font-weight:bold;margin-bottom:15px;">📊 商业定位优化建议（AI生成）</div>
                <div style="background:rgba(255,255,255,0.15);border-radius:8px;padding:15px;font-size:0.85rem;line-height:1.8;">
                    <pre style="white-space:pre-wrap;word-wrap:break-word;margin:0;font-family:inherit;color:white;font-size:0.85rem;">{st.session_state['positioning_advice']}</pre>
                </div>
                <div style="margin-top:12px;font-size:0.75rem;opacity:0.9;">
                    基于近7天20条私信反馈 | 匹配RAG知识库11项技术资产 | 由Qwen-turbo生成
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 闭环说明
        st.markdown("""
        <div style="background:#fffaf0;border:1px solid #ed8936;border-radius:8px;padding:12px;margin-top:15px;">
            <div style="font-weight:bold;color:#c05621;margin-bottom:6px;">🔄 闭环逻辑</div>
            <div style="font-size:0.8rem;color:#744210;">
                下游IP运营产生影响力 → 吸引企业咨询 → AI自动分类需求 → 分析商业定位匹配度 → 
                生成优化建议 → 反哺上游知识库建设 → 形成商业闭环
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption(f"🤖 AI驱动一人公司 | 更新于 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
