#app.py
import streamlit as st
from main import run_compiler

# -----------------------------
# PAGE CONFIG (FORCE LIGHT MODE)
# -----------------------------
st.set_page_config(
    page_title="NUMLANG Compiler",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# FORCE WHITE BACKGROUND (CSS)
# -----------------------------
st.markdown("""
    <style>
        /* App background */
        .stApp {
            background-color: white;
        }

        /* ✅ ONLY headings → dark */
        h1, h2, h3 {
            color: #111 !important;
            font-weight: 700;
        }

        /* ✅ Labels (like "Enter code") */
        label {
            color: #222 !important;
        }

        

        /* Code blocks (keep light style) */
        .stCodeBlock {
            background-color: #f6f8fa !important;
            color: #333 !important;
        }

        /* JSON display */
        .stJson {
            background-color: #f6f8fa !important;
            color: #333 !important;
        }

        /* Output messages */
        .stSuccess {
            background-color: #e6f4ea !important;
            color: #1b5e20 !important;
        }

        .stInfo {
            background-color: #eef3fb !important;
            color: #1a237e !important;
        }

        /* Text area */
        textarea {
            background-color: #fafafa !important;
            color: #111 !important;
        }

        /* Button */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("NUMLANG Compiler Simulator 🚀")

# -----------------------------
# CODE INPUT
# -----------------------------
code = st.text_area(
    "Enter your NumLang Code:",
    height=300,
    placeholder="Example:\nnum a;\na = 5;\nshow a;"
)

# -----------------------------
# RUN BUTTON
# -----------------------------
if st.button("Run Compiler"):

    if not code.strip():
        st.warning("Please enter some code.")
    else:
        result = run_compiler(code)

        # -----------------------------
        # DEBUG (REMOVE LATER)
        # -----------------------------
        # st.write(result)

        if "error" in result:
            st.error(result["error"])

        else:
            # -----------------------------
            # LAYOUT (2 COLUMNS)
            # -----------------------------
            col1, col2 = st.columns(2)

            # -----------------------------
            # LEFT SIDE
            # -----------------------------
            with col1:
                st.subheader("🧾 Tokens")
                st.json(result.get("tokens", []))

                st.subheader("📊 Symbol Table")
                st.json(result.get("symbol_table", {}))

            # -----------------------------
            # RIGHT SIDE
            # -----------------------------
            with col2:
                st.subheader("🌳 Parse Tree (Visual)")
                tree = result.get("parse_tree_graph")
                if tree:
                    st.graphviz_chart(tree)
                else:
                    st.error("Parse tree graph not generated")

                st.subheader("🔧 Three Address Code (TAC)")
                st.code("\n".join(result.get("tac", [])), language="text")

                st.subheader("⚡ Optimized Code")
                st.code("\n".join(result.get("optimized", [])), language="text")

                st.subheader("🔗 Dependency Graph")
                dep_graph = result.get("dependency_graph")
                if dep_graph:
                    st.graphviz_chart(dep_graph)
                else:
                    st.info("No dependency graph available")

                st.subheader("🔁 Control Flow Graph (CFG)")
                cfg = result.get("cfg_graph")
                if cfg:
                    st.graphviz_chart(cfg)
                else:
                    st.info("No CFG available")

            # -----------------------------
            # OUTPUT
            # -----------------------------
            st.subheader("🖥️ Execution Output")

            output = result.get("output", [])

            if output:
                for line in output:
                    st.success(line)
            else:
                st.info("No output generated.")