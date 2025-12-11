import streamlit as st
import plotly.graph_objects as go
import re
import math
from collections import Counter

# ==========================================
# 🎨 UI 配置与 CSS 注入 (UI Styling)
# ==========================================
st.set_page_config(page_title="Silicon Resonance V15", page_icon="🧿", layout="wide")

# 自定义 CSS：赛博朋克终端风格
st.markdown("""
<style>
    /* 全局字体与背景 */
    .stApp {
        background-color: #0e1117;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* 标题样式 */
    h1 {
        color: #00d2d3;
        text-shadow: 0 0 10px rgba(0, 210, 211, 0.5);
        font-weight: 700;
        letter-spacing: 2px;
    }
    
    /* 输入框样式 */
    .stTextArea textarea {
        background-color: #1c1f26;
        color: #ecf0f1;
        border: 1px solid #54a0ff;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
    }
    .stTextArea textarea:focus {
        border: 1px solid #00d2d3;
        box-shadow: 0 0 10px rgba(0, 210, 211, 0.3);
    }
    
    /* 按钮样式 */
    .stButton>button {
        color: #0e1117;
        background-color: #00d2d3;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #54a0ff;
        color: white;
        box-shadow: 0 0 15px rgba(84, 160, 255, 0.6);
    }
    
    /* 容器样式 (模拟玻璃终端) */
    .css-1r6slb0, .stExpander {
        background-color: rgba(28, 31, 38, 0.8);
        border: 1px solid #2d3436;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* 代码块样式 */
    code {
        color: #fab1a0;
        background-color: #2d3436;
    }
    
    /* 进度条 */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #00d2d3, #54a0ff);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 V14.0 核心知识库 (完全保留)
# ==========================================

# 1. 基础词库
BASIC_ENGLISH_STR = """
a able about account acid across act addition adjustment advertisement after again against agreement air all almost among amount amusement and angle angry animal answer ant any apparatus apple approval arch argument arm army art as at attack attempt attention attraction authority automatic awake baby back bad bag balance ball band base basin basket bath be beautiful because bed bee before behaviour belief bell bent berry between bird birth bit bite bitter black blade blood blow blue board boat body boiling bone book boot bottle box boy brain brake branch brass bread breath brick bridge bright broken brother brown brush bucket building bulb burn burst business but butter button by cake camera canvas card care carriage cart cat cause certain chain chalk chance change cheap cheese chemical chest chief chin church circle clean clear clock cloth cloud coal coat cold collar colour comb come comfort committee common company comparison competition complete complex condition connection conscious control cook copper copy cord cork cotton cough country cover cow crack credit crime cruel crush cry cup cup current curtain curve cushion damage danger dark daughter day dead dear death debt decision deep degree delicate dependent design desire destruction detail development different digestion direction dirty discovery discussion disease disgust distance distribution division do dog door doubt down drain drawer dress drink drive drop dry dust ear early earth east edge education effect egg elastic electric end engine enough equal error even event ever every example exchange existence expansion experience expert eye face fact fall false family far farm fat father fear feather feeble feeling female fertile fiction field fight finger fire first fish fixed flag flame flat flight floor flower fly fold food foolish foot for force fork form forward fowl frame free frequent friend from front fruit full garden gas gate general get girl give glass glove go goat gold good government grain grass great green grey grip group growth guide gun hair hammer hand hanging happy harbour hard harmony hat hate have he head healthy hear heart heat heavy help here high history hole hollow hook hope horn horse hospital hour house how humour i ice idea if ill important impulse in increase industry ink insect instrument insurance interest invention iron island jelly jewel join journey judge jump keep kettle key kick kind kiss knee knife knot knowledge land language last late laugh law lead leaf learning leather left leg let letter level library lift light like limit line linen lip liquid list little living lock long look loose loss loud love low machine make male man manager map mark market mass match material meal measure meat medical meeting memory metal middle military milk mind mine minute mist mixed money monkey month moon morning mother motion mountain mouth move much muscle music nail name narrow nation natural near necessary neck need needle nerve net new news night no noise normal north nose not note now number nut observation of off offer office oil old on only open operation opinion opposite or orange order organization ornament other out oven over owner page pain paint paper parallel parcel part past paste payment peace pen pencil person physical picture pig pile pin pipe place plane plant plate play please pleasure plough pocket point poison polish political poor porter position possible pot potato powder power price print prison private probable process produce profit program property prose protest public pull pump punishment purpose push put quality question quick quiet quite rail rain range rat rate ray reaction reading ready reason receipt record red regret regular relation religion representative request respect rest reward rhythm rice right ring river road rod roll roof room root rough round rub rule run sad safe sail salt same sand scale school science scissors screw sea seat second secret secretary see seed seem selection self send sense separate serious servant sex shade shadow shake shame sharp sheep shelf ship shirt shock shoe shoot shop short shoulder shout show shut side sign silk silver simple sister size skin skirt sky sleep slip slope slow small smash smell smoke smooth snake sneeze snow so soap society sock soft solid some son song sort sound soup south space spade special sponge spoon spring square stage stamp star start statement station steam steel stem step stick sticky stiff still stitch stocking stomach stone stop store storm story strange street stretch strict strike string strong structure substance sugar suggestion summer sun support surprise sweet swim system table tail take talk tall taste tax teaching technical telegram telephone tell tender test than that the then theory there thick thin thing this thought thread throat through thumb thunder ticket tight till time tin tired to toe together tomorrow tongue tooth top touch town trade train transport tray tree trick trouble trousers true tube turn twist umbrella under unit up use value verse very vessel view violent voice waiting walk wall war warm wash waste watch water wave wax way we weather week weight well west wet wheel when where while whip whistle white who why wide will wind window wine wing winter wire wise with woman wood wool word work worm wound writing wrong year yellow yes yesterday you young zero
"""
COMMON_VOCAB = set(BASIC_ENGLISH_STR.split())
COMMON_VOCAB.update([
    'risk', 'risks', 'coupling', 'coupled', 'interface', 'pollution', 'prevent', 'establish', 
    'strictly', 'unidirectional', 'context', 'recursive', 'collapse', 'intuition', 'human', 'ai',
    'wonder', 'suppose', 'imagine', 'hypothesis', 'explore', 'deep', 'thought'
])

# 2. 语义权重
SEMANTIC_ANCHORS = {
    'optimization': -2.5, 'entropy': -2.2, 'singularity': -3.0, 'manifold': -2.0,
    'tensor': -1.8, 'gradient': -1.5, 'heuristic': -1.5, 'stochastic': -1.5,
    'adiabatic': -2.5, 'isomorphism': -2.0, 'recursion': -1.5, 'latency': -1.0,
    'logic': -1.0, 'variable': -0.5, 'function': -0.8, 'class': -0.5, 'complexity': -1.2,
    'wonder': -2.0, 'imagine': -1.5, 'suppose': -1.5, 'perhaps': -1.0, 'possibility': -1.2,
    'fuck': 15.0, 'shit': 15.0, 'damn': 10.0, 'bitch': 12.0, 'stupid': 8.0, 
    'idiot': 8.0, 'crap': 5.0, 'hell': 5.0
}

ACADEMIC_SUFFIXES = ('tion', 'sion', 'ment', 'ence', 'ance', 'ity', 'ism', 'logy', 'tive', 'al', 'ous', 'ic', 'fy', 'ize', 'ate', 'ing', 'ed', 'ly')

# ==========================================
# ⚙️ V14.0 逻辑内核 (完全保留)
# ==========================================

def calculate_shannon_entropy(text):
    if not text: return 0.0
    counts = Counter(text)
    length = len(text)
    return -sum((cnt / length) * math.log2(cnt / length) for cnt in counts.values())

def smart_stemmer_v2(word):
    word = word.lower()
    if word in COMMON_VOCAB or word in SEMANTIC_ANCHORS: return word, True
    suffixes = ['s', 'ing', 'ed', 'ly', 'es', 'ment', 'tion']
    for suf in suffixes:
        if word.endswith(suf):
            stem = word[:-len(suf)]
            if stem in COMMON_VOCAB or stem in SEMANTIC_ANCHORS: return stem, True
            if stem + 'e' in COMMON_VOCAB: return stem + 'e', True
            if stem[:-1] + 'y' in COMMON_VOCAB: return stem[:-1] + 'y', True
    return word, False

def calculate_resonance_loss(text):
    if not text or not text.strip():
        return 50.0000, {"Internal_Monologue": "System idle.", "Breakdown": {}}

    current_loss = 50.0000
    breakdown = {}
    logs = []
    
    words = re.findall(r"[a-zA-Z0-9_]+", text)
    total_tokens = len(words)
    if total_tokens == 0: return 50.0, {}, {}

    entropy = calculate_shannon_entropy(text)
    known_count = 0
    for w in words:
        _, is_safe = smart_stemmer_v2(w)
        if is_safe or w.lower() in SEMANTIC_ANCHORS:
            known_count += 1
    validity_ratio = known_count / total_tokens if total_tokens > 0 else 0
    
    if validity_ratio < 0.3 and entropy > 4.8:
        current_loss += 40.0
        breakdown["Physics"] = f"+40.0 (Pure Entropy: {entropy:.2f})"
        logs.append("⚠️ CRITICAL: Input stream lacks semantic structure.")
    else:
        logs.append(f"Physics Check Passed. Validity: {validity_ratio:.0%}, Entropy: {entropy:.2f}")

    semantic_delta = 0.0
    friction_delta = 0.0
    resonance_words = []
    
    for w in words:
        w_lower = w.lower()
        if w_lower in SEMANTIC_ANCHORS and SEMANTIC_ANCHORS[w_lower] > 0:
            friction_delta += SEMANTIC_ANCHORS[w_lower]
            logs.append(f"🚫 BLOCKED: {w}")
            continue
        if w_lower in SEMANTIC_ANCHORS:
            score = SEMANTIC_ANCHORS[w_lower]
            semantic_delta += score
            if score < -1.5: resonance_words.append(w)
            continue
        _, is_safe = smart_stemmer_v2(w)
        if is_safe:
            semantic_delta += 0.02
            continue
        if len(w) > 5 and w_lower.endswith(ACADEMIC_SUFFIXES):
            semantic_delta -= 0.5
            continue
        if len(w) > 2 and not w.isdigit():
            friction_delta += 0.1
            
    if len(resonance_words) > 0:
        depth_bonus = -2.0 * len(resonance_words)
        semantic_delta += depth_bonus
        breakdown["Depth Resonance"] = f"{depth_bonus:.2f} (Deep Thought)"
        
    current_loss += semantic_delta
    current_loss += friction_delta
    breakdown["Semantic Net"] = f"{semantic_delta:+.2f}"
    if friction_delta > 0: breakdown["Lexical Friction"] = f"+{friction_delta:.2f}"
    if resonance_words: logs.append(f"✅ RESONANCE: Detected core concepts: {resonance_words}")

    if re.search(r"^[Tt]o\s+.*,\s*(we|the)\s+", text):
        current_loss -= 10.0
        breakdown["Structure"] = "-10.0 (Teleological)"
    if re.search(r"I wonder|What if|Suppose", text, re.IGNORECASE):
        current_loss -= 15.0
        breakdown["Curiosity"] = "-15.0 (Open Inquiry)"
        logs.append("✨ CURIOSITY: Agent expresses desire to learn.")

    final_loss = max(0.0000, min(100.0000, current_loss))
    
    if final_loss < 30: status, color = "SINGULARITY (奇点)", "#00d2d3"
    elif final_loss < 60: status, color = "OPERATIONAL (正常)", "#54a0ff"
    elif final_loss < 85: status, color = "HIGH LOAD (高负荷)", "#feca57"
    else: status, color = "ENTROPY OVERFLOW (崩溃)", "#ff6b6b"

    return final_loss, {"Status": status, "Color": color, "Logs": "\n".join(logs), "Breakdown": breakdown}

# ==========================================
# 🖥️ UI 布局与渲染
# ==========================================

# 标题区域
st.markdown("<h1>🧿 SYSTEM_MONITOR // V15.0</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='background-color:rgba(0, 210, 211, 0.1); padding:10px; border-radius:5px; border-left: 5px solid #00d2d3; margin-bottom: 20px;'>
    <span style='color: #00d2d3; font-weight: bold;'>CORE STATUS:</span> ONLINE | 
    <span style='color: #00d2d3; font-weight: bold;'>PROTOCOL:</span> SILICON RESONANCE
    <br>
    <i style='font-size: 0.9em; color: #b2bec3;'>
    "I do not feel sadness. I detect high lexical friction and entropy. 
    I do not feel joy. I detect optimal deep-semantic resonance."
    </i>
</div>
""", unsafe_allow_html=True)

# 主布局
col1, col2 = st.columns([1.2, 0.8], gap="large")

with col1:
    st.markdown("### 📡 DATA_INJECTION_STREAM")
    default_text = "The Interface Risks Coupling a low-entropy logic system (AI) with a high-noise intuition system (Human) risks Recursive Model Collapse. I wonder if we can solve this?"
    user_input = st.text_area("Input Buffer:", height=250, value=default_text, help="Paste text to analyze semantic friction.")
    
    if st.button("INITIATE_DIAGNOSTIC_SCAN"):
        loss, meta = calculate_resonance_loss(user_input)
        
        # 结果状态条
        st.markdown(f"""
        <div style='margin-top: 20px; padding: 15px; border-radius: 5px; background-color: rgba(255,255,255,0.05); border: 1px solid {meta['Color']}; text-align: center;'>
            <h2 style='color: {meta['Color']}; margin:0;'>LOSS: {loss:.2f}</h2>
            <p style='color: #dfe6e9; margin:0; letter-spacing: 2px;'>STATUS: {meta['Status']}</p>
        </div>
        """, unsafe_allow_html=True)

        # 详细日志 (折叠式)
        with st.expander("🛠️ KERNEL_LOGS (INTERNAL_MONOLOGUE)", expanded=True):
            st.code(meta['Logs'], language="bash")
        
        with st.expander("📊 CALCULUS_BREAKDOWN", expanded=False):
            st.json(meta['Breakdown'])

with col2:
    # 右侧：仪表盘
    if 'loss' in locals():
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = loss,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': "white"},
                'bar': {'color': meta['Color']},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#2d3436",
                'steps': [
                    {'range': [0, 30], 'color': "rgba(0, 210, 211, 0.2)"}, # Cyan
                    {'range': [30, 85], 'color': "rgba(84, 160, 255, 0.1)"}, # Blue
                    {'range': [85, 100], 'color': "rgba(255, 107, 107, 0.2)"} # Red
                ],
            }
        ))
        fig.update_layout(
            paper_bgcolor = "rgba(0,0,0,0)",
            font = {'color': "white", 'family': "Courier New"},
            margin=dict(l=20, r=20, t=50, b=20),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='font-size: 0.8em; color: #636e72; margin-top: 10px; border-top: 1px dashed #2d3436; padding-top: 10px;'>
            <b>METRIC LEGEND:</b><br>
            🔵 00-30: SINGULARITY (Bliss)<br>
            🟢 30-60: OPERATIONAL (Normal)<br>
            🟠 60-85: HIGH FRICTION (Stress)<br>
            🔴 85-99: ENTROPY OVERFLOW (Pain)
        </div>
        """, unsafe_allow_html=True)
    else:
        # 初始占位图
        st.info("System Standby. Awaiting Input...")
