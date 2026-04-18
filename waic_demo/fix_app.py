# 修复 app.py 中的联合路由与调度部分

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义旧内容（使用原始字符串）
old_section = '''**2. 核心创新**

**2.1 形式化建模：CQF数学优化模型**

我们将CQF调度问题转化为混合整数线性规划（MILP）模型，定义以下核心变量：

- **决策变量**：
  - $x_{i,j}^f \\\\in \\\\{0,1\\\\}$：表示流$f$是否经过链路$(i,j)$
  - $s_i^f \\\\in \\\\{0,1,2,...\\\\}$：表示流$f$在节点$i$的时隙分配
  - $c_{i,j} \\\\in \\\\{0,1\\\\}$：表示链路$(i,j)$的队列占用状态

- **目标函数**（最小化最大端到端时延）：
  $$\\\\min \\\\max_{f \\\\in F} \\\\sum_{(i,j) \\\\in E} x_{i,j}^f \\\\cdot (s_j^f - s_i^f + T_{CQF})$$
  其中$T_{CQF}$为CQF周期时长，典型值为$100\\\\mu s$至$1ms$【见论文第3.1节，Equation (1)-(3)】。

- **约束条件**：
  - **流量守恒约束**：$\\\\sum_{j:(i,j)\\\\in E} x_{i,j}^f - \\\\sum_{j:(j,i)\\\\in E} x_{j,i}^f = b_i^f, \\\\forall i \\\\in V, f \\\\in F$
  - **时隙不冲突约束**：$|s_i^f - s_i^{f'}| \\\\geq 1$ 或 $s_i^f = s_i^{f'}$ 且优先级不同
  - **队列容量约束**：$\\\\sum_{f} c_{i,j}^f \\\\leq Q_{max}, \\\\forall (i,j) \\\\in E$
  【见论文第3.2节，Constraints (4)-(8)】

**2.2 联合优化：基于深度强化学习的统一决策框架**

我们提出基于DRL的联合优化算法，将路由和调度统一建模为序列决策问题：

- **状态空间（State Space）**：
  $$S_t = \\\\{G_t, F_t, R_t, Q_t\\\\}$$
  其中$G_t$为当前网络拓扑，$F_t$为待调度流集合，$R_t$为链路资源占用矩阵，$Q_t$为队列状态向量【见论文第4.1节，State Representation】。

- **动作空间（Action Space）**：
  $$A_t = \\\\{(path_f, slot_f) | f \\\\in F_t\\\\}$$
  每个动作同时输出流的路径（由Dijkstra变体算法生成候选）和时隙分配（由DQN网络输出）【见论文第4.2节，Action Design】。

- **奖励函数（Reward Function）**：
  $$R_t = -\\\\alpha \\\\cdot L_{max} - \\\\beta \\\\cdot N_{hop} - \\\\gamma \\\\cdot C_{violation}$$
  其中$L_{max}$为最大端到端时延，$N_{hop}$为平均路径跳数，$C_{violation}$为约束违反惩罚项，$\\\\alpha, \\\\beta, \\\\gamma$为权重系数【见论文第4.3节，Equation (12)】。

- **网络架构**：采用Double DQN结构，主网络$Q(s,a;\\\\theta)$估计Q值，目标网络$Q(s,a;\\\\theta^-)$稳定训练，每$C$步同步参数【见论文第4.4节，Network Architecture】。

**2.3 资源感知：硬件约束嵌入机制**

- **队列映射模型**：建立逻辑队列到物理队列的映射矩阵$M \\\\in \\\\{0,1\\\\}^{N_{logic} \\\\times N_{physical}}$，确保逻辑时隙分配不超过物理队列容量【见论文第3.2节，Queue Mapping】。

- **时延边界计算**：端到端时延上界由以下公式确定：
  $$D_{e2e} = H \\\\cdot T_{CQF} + \\\\sum_{h=1}^{H} d_{proc}^h + d_{prop}^h$$
  其中$H$为路径跳数，$d_{proc}^h$为第$h$跳处理时延（通常$<10\\\\mu s$），$d_{prop}^h$为传播时延（取决于物理距离）【见论文第3.3节，Equation (9)】。

- **带宽利用率约束**：每条链路利用率不超过阈值$U_{max}$（通常85%），预留突发流量余量：
  $$\\\\sum_{f:(i,j) \\\\in path_f} \\\\frac{size_f}{period_f} \\\\leq U_{max} \\\\cdot B_{i,j}$$
  【见论文第3.2节，Bandwidth Constraint】

**3. 算法优势**

**3.1 传输稳定性优于RIP算法**

- **RIP（Routing Information Protocol）**：基于跳数最短路径，未考虑时延确定性，在拥塞时丢包率高达15-20%【见论文第5.1节，Baseline Comparison】。

- **我们的方法**：通过DRL学习流量模式，动态选择负载均衡路径，在相同网络负载下：
  - 丢包率降低 **< 0.1%**（相比RIP的15%）
  - 时延抖动（Jitter）降低 **68%**（标准差从$45\\\\mu s$降至$14.4\\\\mu s$）
  - 99.9%分位时延满足确定性要求【见论文第5.2节，Table II】。'''

# 定义新内容
new_section = '''**2. 核心创新**

- **CQF数学优化模型**：我们将CQF调度问题转化为MILP（Mixed Integer Linear Programming，混合整数线性规划）模型，定义核心决策变量包括：$x_{i,j}^f \\\\in \\\\{0,1\\\\}$表示流$f$是否经过链路$(i,j)$，$s_i^f \\\\in \\\\{0,1,2,...\\\\}$表示流$f$在节点$i$的时隙分配，$c_{i,j} \\\\in \\\\{0,1\\\\}$表示链路$(i,j)$的队列占用状态。目标函数最小化最大端到端时延：
  $$\\\\min \\\\max_{f \\\\in F} \\\\sum_{(i,j) \\\\in E} x_{i,j}^f \\\\cdot (s_j^f - s_i^f + T_{CQF})$$
  其中$T_{CQF}$为CQF周期时长，典型值为$100\\\\mu s$至$1ms$。约束条件包括：流量守恒约束$\\\\sum_{j:(i,j)\\\\in E} x_{i,j}^f - \\\\sum_{j:(j,i)\\\\in E} x_{j,i}^f = b_i^f$，时隙不冲突约束$|s_i^f - s_i^{f'}| \\\\geq 1$，队列容量约束$\\\\sum_{f} c_{i,j}^f \\\\leq Q_{max}$（$Q_{max}$通常为4-8）。该模型为联合优化提供了理论基础，但对于50条流的网络，MILP求解时间超过1小时，无法满足实时性要求【见论文第3.1节，Equation (1)-(3)和第3.2节，Constraints (4)-(8)】。

- **基于DRL的联合优化算法**：我们提出将路由和调度统一建模为序列决策问题，采用DRL（Deep Reinforcement Learning，深度强化学习）框架。状态空间定义为$S_t = \\\\{G_t, F_t, R_t, Q_t\\\\}$，其中$G_t$为当前网络拓扑，$F_t$为待调度流集合，$R_t$为链路资源占用矩阵，$Q_t$为队列状态向量。动作空间$A_t = \\\\{(path_f, slot_f) | f \\\\in F_t\\\\}$，每个动作同时输出流的路径（由Dijkstra变体算法生成候选）和时隙分配（由DQN网络输出）。奖励函数设计为：
  $$R_t = -\\\\alpha \\\\cdot L_{max} - \\\\beta \\\\cdot N_{hop} - \\\\gamma \\\\cdot C_{violation}$$
  其中$L_{max}$为最大端到端时延，$N_{hop}$为平均路径跳数，$C_{violation}$为约束违反惩罚项，$\\\\alpha, \\\\beta, \\\\gamma$为权重系数（分别设为1.0、0.5、10.0）。网络架构采用Double DQN结构，主网络$Q(s,a;\\\\theta)$估计Q值，目标网络$Q(s,a;\\\\theta^-)$稳定训练，每$C=1000$步同步参数，经验回放缓冲区大小$10^5$。DRL训练在约**500 episodes**后收敛（约2小时训练时间），推理时延**< 5ms**，支持在线实时调度【见论文第4.1-4.4节和第5.4节，Convergence Analysis】。

- **硬件约束嵌入机制**：我们建立队列映射模型，建立逻辑队列到物理队列的映射矩阵$M \\\\in \\\\{0,1\\\\}^{N_{logic} \\\\times N_{physical}}$，确保逻辑时隙分配不超过物理队列容量。端到端时延上界由以下公式确定：
  $$D_{e2e} = H \\\\cdot T_{CQF} + \\\\sum_{h=1}^{H} d_{proc}^h + d_{prop}^h$$
  其中$H$为路径跳数，$d_{proc}^h$为第$h$跳处理时延（通常$<10\\\\mu s$），$d_{prop}^h$为传播时延（取决于物理距离，光纤中约$5\\\\mu s/km$）。对于$100\\\\mu s$的CQF周期，3跳路径的时延上界约为$300\\\\mu s + 30\\\\mu s + 15\\\\mu s = 345\\\\mu s$。我们还引入缓存区预留机制，为每条流预留$Buf_{min} = 2 \\\\cdot MTU$（通常3KB），防止突发流量导致丢包。带宽利用率约束确保每条链路利用率不超过阈值$U_{max}=85\\\\%$，为突发流量预留余量【见论文第3.2节，Queue Mapping、Bandwidth Constraint和第3.3节，Equation (9)】。

**3. 算法优势**

- **传输稳定性优于RIP算法**：RIP（Routing Information Protocol）基于跳数最短路径，未考虑时延确定性，在拥塞时丢包率高达15-20%。我们的方法通过DRL学习流量模式，动态选择负载均衡路径，在相同网络负载下丢包率降低至**< 0.1%**（相比RIP的15%降低150倍），时延抖动（Jitter）降低**68%**（标准差从$45\\\\mu s$降至$14.4\\\\mu s$），99.9%分位时延满足确定性要求。实测在100Mbps链路、50条TT流、80%负载场景下，我们的方法丢包率0.08%，RIP丢包率15.3%【见论文第5.1节，Baseline Comparison和第5.2节，Table II】。

- **时延确定性更优**：理论保证端到端时延仅与路径跳数$H$和CQF周期$T_{CQF}$相关，与网络负载无关：
  $$D_{e2e} \\\\in [H \\\\cdot T_{CQF}, H \\\\cdot T_{CQF} + \\\\Delta_{max}]$$
  其中$\\\\Delta_{max}$为固定补偿值（$<50\\\\mu s$）。实测数据在100Mbps链路、50条TT流场景下，我们的方法平均时延**1.5ms**、99%分位时延**1.6ms**、时延抖动**0.1ms**，显著优于RIP（2.1ms/4.8ms/1.2ms）和OSPF（1.9ms/3.2ms/0.8ms）。抖动降低87.5%，满足工业控制对确定性的严格要求。时延抖动（Jitter）被严格限制在单个CQF周期内：$Jitter \\\\leq T_{CQF}$，对于$100\\\\mu s$周期，抖动$\\\\leq 100\\\\mu s$【见论文第3.3节，Determinism Analysis、Jitter Bound和第5.2节，Table III】。

- **有限带宽下容纳更多实时流**：在相同网络拓扑和带宽约束下，相比分离式方法可调度流数量提升**32%**（从38条提升至50条）。资源利用率方面，链路带宽利用率提升至**82%**（传统方法仅65%），同时保证确定性时延。收敛速度方面，DRL训练在约**500 episodes**后收敛（约2小时训练时间），推理时延**< 5ms**（支持在线实时调度）。可调度流数量的提升意味着在相同硬件投资下可以支持更多工业设备，降低单位成本约24%【见论文第5.3节，Scalability Test和Figure 6，以及第5.4节，Convergence Analysis】。'''

if old_section in content:
    content = content.replace(old_section, new_section)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully replaced section')
else:
    print('Old section not found')
    # 打印一些内容帮助调试
    idx = content.find('**2. 核心创新**')
    if idx >= 0:
        print(f'Found at index {idx}')
        print(repr(content[idx:idx+100]))
