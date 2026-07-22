
<div align="center">

# 🚀 NumLang Compiler

### Design • Compile • Optimize • Execute • Visualize

<p>
A complete implementation of a <b>Mini Compiler</b> for a custom programming language (<b>NumLang</b>) built using <b>Python</b>, featuring lexical analysis, parsing, semantic analysis, intermediate code generation, optimization, execution, and interactive visualization.
</p>

<p>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Graphviz](https://img.shields.io/badge/Graphviz-009688?style=for-the-badge)
![Compiler](https://img.shields.io/badge/Compiler-Design-blueviolet?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

</p>

</div>

---

# 📖 Table of Contents

- 📚 About
- ✨ Features
- 🏗 Architecture
- ⚙ Compiler Pipeline
- 🧠 NumLang Language
- 💻 Technologies Used
- 📂 Project Structure
- 🚀 Getting Started
- 🖥 Usage
- 🧪 Testing
- 📊 Outputs
- 🔮 Future Enhancements
- 👨‍💻 Authors
- 📜 License

---

# 📚 About

NumLang Compiler is an educational compiler implementation that demonstrates every major phase involved in compiler construction.

Instead of directly executing the source code, the compiler transforms it through multiple stages including lexical analysis, syntax analysis, semantic validation, intermediate code generation, optimization, and execution.

To improve understanding of compiler internals, the project also includes an interactive Streamlit dashboard capable of visualizing the parser output, symbol table, control flow graph, dependency graph, and optimized intermediate code.

---

# ✨ Features

## 🔹 Compiler Components

- ✅ Lexical Analyzer (Regex-based Tokenizer)
- ✅ Recursive Descent Parser
- ✅ Semantic Analyzer
- ✅ Symbol Table Generator
- ✅ Three Address Code (TAC) Generator
- ✅ Code Optimizer
- ✅ Interpreter-Based Execution Engine

## 📈 Visualizations

- 🌳 Parse Tree
- 📋 Symbol Table
- 🔀 Control Flow Graph (CFG)
- 🔗 Dependency Graph
- ⚡ Optimized TAC
- 📄 Execution Output

---

# 🏗 System Architecture

```
               Source Code
                    │
                    ▼
          Lexical Analysis
                    │
                    ▼
          Syntax Analysis
                    │
                    ▼
         Semantic Analysis
                    │
                    ▼
            Symbol Table
                    │
                    ▼
      Three Address Code (TAC)
                    │
                    ▼
          Code Optimization
                    │
                    ▼
    Control Flow / Dependency Graph
                    │
                    ▼
          Execution Engine
                    │
                    ▼
             Program Output
```

---

# ⚙ Compiler Pipeline

| Phase | Description |
|--------|-------------|
| 🔍 Lexical Analysis | Converts source code into tokens |
| 🌲 Syntax Analysis | Validates grammar using Recursive Descent Parsing |
| 🧠 Semantic Analysis | Detects logical and semantic errors |
| 📋 Symbol Table | Stores identifiers and their properties |
| ⚡ TAC Generation | Produces platform-independent intermediate code |
| 🚀 Optimization | Performs Constant Folding & Algebraic Simplification |
| ▶ Execution | Executes generated TAC using an Interpreter |
| 📊 Visualization | Displays compiler internals interactively |

---

# 🧠 NumLang Language

## Variable Declaration

```text
num a;
```

## Assignment

```text
a = 10;
```

## Print

```text
show a;
```

## Conditional

```text
cond(a>b){
    show a;
}
else{
    show b;
}
```

## Loop

```text
loop(i<10){
    show i;
}
```

## Function

```text
func add(num a,num b){
    return a+b;
}

x = add(5,3);
```

---

# 💻 Technologies Used

<div align="center">

| Technology | Purpose |
|------------|----------|
| 🐍 Python | Core Compiler Implementation |
| 🎨 Streamlit | Interactive Dashboard |
| 📊 Graphviz | Graph Visualization |
| 🔍 Regular Expressions | Lexical Analysis |
| 🧠 Recursive Descent Parsing | Syntax Analysis |

</div>



---


# 🖥 Usage

The Streamlit interface allows users to

- ✍ Write NumLang programs
- 🔍 Perform Lexical Analysis
- 🌳 Generate Parse Tree
- 📋 View Symbol Table
- ⚡ Generate Three Address Code
- 🚀 Optimize Intermediate Code
- 🔗 Visualize Control Flow Graph
- ▶ Execute Programs
- 📊 Analyze Compiler Output

---

# 🧪 Testing

The compiler has been tested against various compiler scenarios.

| Test Case | Status |
|-----------|--------|
| ✅ Parenthesis Checking | Passed |
| ✅ If Conditions | Passed |
| ✅ Undeclared Variables | Passed |
| ✅ Duplicate Declaration | Passed |
| ✅ Semantic Errors | Passed |
| ✅ Division by Zero | Passed |
| ✅ Function Validation | Passed |
| ✅ Nested Expressions | Passed |

---

# 📊 Sample Outputs

The compiler generates

- 📄 Token Stream
- 🌳 Parse Tree
- 📋 Symbol Table
- ⚡ Three Address Code
- 🚀 Optimized TAC
- 🔀 Control Flow Graph
- 🔗 Dependency Graph
- ▶ Execution Output

---

# 🎯 Educational Objectives

This project demonstrates

- Compiler Construction
- Language Processing
- Parsing Techniques
- Intermediate Code Generation
- Program Optimization
- Static Analysis
- Runtime Execution
- Compiler Visualization

making it an excellent educational tool for understanding compiler design principles.

---

# 🔮 Future Enhancements

- ✅ Floating Point Support
- ✅ String Data Type
- ✅ Arrays
- ✅ Classes
- ✅ Function Overloading
- ✅ Dead Code Elimination
- ✅ Register Allocation
- ✅ LLVM Backend
- ✅ MIPS Code Generation
- ✅ Advanced Optimizations

---

# 📈 Project Highlights

<div align="center">

| Feature | Available |
|----------|-----------|
| Lexical Analysis | ✅ |
| Parser | ✅ |
| Semantic Analyzer | ✅ |
| Symbol Table | ✅ |
| TAC Generator | ✅ |
| Optimization | ✅ |
| Interpreter | ✅ |
| Streamlit UI | ✅ |
| Graphviz Visualization | ✅ |

</div>

---

# 🤝 Contributing

Contributions, suggestions, and improvements are always welcome.

If you'd like to improve the compiler or extend NumLang with additional language features, feel free to fork the repository and submit a pull request.

---

# 👨‍💻 Authors

**Kanusu Manikanta Sai**

B.Tech Computer Science Engineering

Amrita Vishwa Vidyapeetham, Bengaluru

---

<div align="center">

## ⭐ If you found this project useful, consider giving it a Star!

</div>

---

<div align="center">

Made with ❤️ using Python, Streamlit and Graphviz

</div>
