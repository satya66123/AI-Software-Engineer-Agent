import streamlit as st
import os
from src.agents.bug_finder.bug_finder import find_bugs
from src.agents.security_analyzer import analyze_security
from src.agents.code_reviewer import review_code
from src.agents.pr_review_agent import review_pull_request
from src.agents.feature_generator import generate_features
from src.agents.code_generator import generate_code
from src.github.validator import validate_github_url
from src.github.cloner import clone_repository
from src.github.scanner import scan_repository
from src.github.language_detector import detect_languages
from src.github.stats import calculate_stats
from src.github.tree_viewer import generate_tree
from src.github.readme_analyzer import read_readme
from src.github.project_summary import generate_summary
from src.rag.indexer import build_repository_index
from src.rag.vector_store import get_all_vectors
from src.rag.vector_store import clear_vectors
from src.rag.search import search_repository
from src.rag.qa import answer_question
from src.utils.logger import logger
from src.agents.code_explainer.code_explainer import explain_code
from src.agents.documentation_agent.documentation_generator import generate_documentation
from src.agents.test_generator.test_generator import generate_tests
from src.agents.refactoring_agent.refactoring_agent import refactor_code
from src.agents.dependency_analyzer import analyze_dependencies
from src.agents.architecture_analyzer import analyze_architecture
from src.agents.api_doc_generator import generate_api_docs
from src.agents.code_flow_analyzer import analyze_code_flow
from src.agents.multi_file_analyzer import analyze_multiple_files
from src.analytics.dashboard import get_dashboard_stats
from src.rag.bm25_search import bm25_search
from src.rag.hybrid_search import hybrid_search
from src.rag.reranker import rerank_chunks
from src.utils.report_exporter import (
    export_pdf,
    export_docx,
    export_txt
)
from src.utils.settings import (
    load_settings,
    save_settings
)
from src.analytics.usage_stats import (
    increment_stat,
    get_usage_stats,
    initialize_stats
)

st.set_page_config(
    page_title="AI Software Engineer Agent",
    layout="wide"
)

logger.info("Application started")

st.title("🤖 AI Software Engineer Agent")
st.markdown("---")

# Initialize session state
if "repo_loaded" not in st.session_state:
    st.session_state.repo_loaded = False
if "readme_content" not in st.session_state:
    st.session_state.readme_content = None
if "files" not in st.session_state:
    st.session_state.files = []
if "clone_path" not in st.session_state:
    st.session_state.clone_path = ""
if "current_tab" not in st.session_state:
    st.session_state.current_tab = 0

initialize_stats()

provider = st.sidebar.selectbox(
    "🧠 AI Provider",
    ["Ollama", "OpenAI"]
)

if provider == "Ollama":
    models = [
        "qwen2.5:1.5b",
        "deepseek-coder:latest",
        "gemma2:2b",
        "phi3:latest",
        "gemma3:4b",
        "mistral:latest",
        "llama3:8b",
        "llama3.1:8b",
        "qwen3:latest"
    ]
else:
    models = [
        "gpt-4o-mini",
        "gpt-4o"
    ]

selected_model = st.sidebar.selectbox(
    "Model",
    models
)

st.session_state.provider = provider
st.session_state.selected_model = selected_model

# Convenience: short references used throughout tabs
_provider = st.session_state.provider
_model = st.session_state.selected_model


# ── Repository Input (always visible) ────────────────────────────────────────
repo_url = st.text_input(
    "Enter GitHub Repository URL",
    placeholder="https://github.com/user/repository"
)

if st.button("Analyze Repository"):
    logger.info(f"Analyze Repository clicked. URL: {repo_url}")

    if not repo_url.strip():
        logger.warning("Empty repository URL submitted")
        st.warning("Please enter a GitHub repository URL.")
        st.stop()

    result = validate_github_url(repo_url)
    if not result["valid"]:
        logger.warning(f"Invalid GitHub URL provided: {repo_url}")
        st.error("Invalid GitHub Repository URL")
        st.stop()

    try:
        with st.spinner("Cloning repository..."):
            logger.info(f"Cloning repository: {repo_url}")
            clone_path = clone_repository(repo_url)
            logger.info(f"Repository cloned to: {clone_path}")

        with st.spinner("Scanning"
                        " repository..."):
            logger.info(f"Scanning repository at: {clone_path}")
            files = scan_repository(clone_path)
            logger.info(f"Scan complete. {len(files)} supported files found")

        readme_content = read_readme(clone_path)
        if readme_content:
            logger.info("README.md found and loaded")
        else:
            logger.warning("README.md not found in repository")

        st.session_state.repo_loaded = True
        st.session_state.files = files
        st.session_state.clone_path = clone_path
        st.session_state.readme_content = readme_content
        logger.info("Repository loaded successfully into session state")
        increment_stat("repository_loaded")
        st.success("Repository loaded successfully")

    except Exception as e:
        logger.error(f"Clone Error: {str(e)}")
        st.error(f"Error: {str(e)}")

st.markdown("---")

# ── Tabs (shown only after a repo is loaded) ─────────────────────────────────
if st.session_state.repo_loaded:
    files = st.session_state.files
    clone_path = st.session_state.clone_path
    readme_content = st.session_state.readme_content

    # Always read the latest provider/model from session state inside tabs
    _provider = st.session_state.provider
    _model = st.session_state.selected_model

    (tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8,
     tab9, tab10, tab11, tab12, tab13, tab14, tab15,
     tab16, tab17, tab18, tab19, tab20, tab21,
     tab22, tab23, tab24, tab25) = st.tabs([
        "📂 Repository Statistics",
        "📊 Project Structure",
        "📖 README",
        "🧠 Index",
        "❓ Q&A",
        "📜 Logs",
        "🤖 Code Explainer",
        "📚 Documentation",
        "🐞 Bug Finder",
        "🧪 Unit Tests",
        "♻️ Refactoring",
        "📦 Dependencies",
        "🏗 Architecture",
        "📘 API Docs",
        "🔄 Code Flow",
        "🧠 Multi-File Analyzer",
        "🔐 Security Analyzer",
        "👨‍💻 Code Reviewer",
        "📝 PR Review Agent",
        "⚡ Feature Generator",
        "🚀 Code Generator",
        "📊 Dashboard",
        "📄 Export Report",
        "⚙️ Settings",
        "📈 Usage Stats",
    ])

    # ── Tab 1: Repository Statistics ─────────────────────────────────────────
    with tab1:
        st.subheader("Repository Statistics")

        languages = detect_languages(files)
        stats = calculate_stats(files)
        logger.info(
            f"Stats calculated: {stats['total_files']} files, "
            f"{stats['total_lines']} lines"
        )

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Files", stats["total_files"])
        with col2:
            st.metric("Total Lines", stats["total_lines"])

        st.markdown("---")
        st.subheader("Languages Used")
        for language, count in languages.items():
            st.write(f"**{language}:** {count}")

    # ── Tab 2: Project Structure ──────────────────────────────────────────────
    with tab2:
        st.subheader("Project Structure")
        tree = generate_tree(clone_path)
        st.code("\n".join(tree), language="text")

        st.markdown("---")
        st.subheader("Repository Files")
        for file in files[:50]:
            st.write(f"📄 {file['name']} ({file['extension']})")
        if len(files) > 50:
            st.info(f"Showing first 50 files out of {len(files)}")

    # ── Tab 3: README ─────────────────────────────────────────────────────────
    with tab3:
        st.subheader("README Analysis")

        if readme_content:
            st.success("README.md Found")
            st.text_area("README Content", readme_content, height=300)

            if st.button("Generate AI Summary"):
                logger.info("Generate AI Summary clicked")
                try:
                    with st.spinner("Generating summary..."):
                        # Pass provider + model so generate_summary can route
                        # to Ollama or OpenAI accordingly.
                        summary = generate_summary(
                            readme_content,
                            provider=_provider,
                            model=_model
                        )
                    logger.info("AI summary generated successfully")
                    st.subheader("AI Project Summary")
                    increment_stat("agents_used")
                    st.write(summary)
                except Exception as e:
                    logger.error(f"Summary Error: {str(e)}")
                    st.error(f"Summary Error: {str(e)}")
        else:
            st.warning("README.md not found")


    # ── Tab 4: Index ──────────────────────────────────────────────────────────

    with tab4:

        st.subheader("🧠 Build Repository Index")

        st.write(
            "Chunk and embed repository files for semantic search."
        )

        if st.button(
                "Build Repository Index",
                key="build_index_btn"
        ):

            logger.info(
                "Build Repository Index clicked"
            )

            try:

                with st.spinner(
                        "Generating embeddings..."
                ):

                    # Embedding Model Selection

                    embedding_model = (
                        "text-embedding-3-small"
                        if _provider == "OpenAI"
                        else "nomic-embed-text"
                    )

                    logger.info(
                        f"Provider={_provider}"
                    )

                    logger.info(
                        f"Embedding Model={embedding_model}"
                    )

                    clear_vectors(
                        _provider
                    )

                    chunk_count = (
                        build_repository_index(
                            files=files,
                            provider=_provider,
                            model=_model
                        )
                    )

                    st.write(
                        "Current Provider:",
                        _provider
                    )

                    st.write(
                        "Stored Vectors:",
                        len(
                            get_all_vectors(
                                _provider
                            )
                        )
                    )

                    logger.info(
                        f"Indexed {chunk_count} chunks"
                    )

                st.success(
                    f"Indexed {chunk_count} chunks"
                )

                st.write(
                    f"Stored Vectors: "
                    f"{len(get_all_vectors(_provider))}"
                )

            except Exception as e:

                logger.error(
                    f"Indexing Error: {e}"
                )

                st.error(
                    f"Indexing Error: {e}"
                )

    # ── Tab 5: Q&A ────────────────────────────────────────────────────────────

    with tab5:

        st.subheader("❓ Repository Q&A")

        question = st.text_input("Ask a question about the repository")

        search_type = st.radio(
            "Search Method",
            ["Semantic", "BM25", "Hybrid"],
            horizontal=True
        )

        st.info(f"Provider: {_provider}")
        st.info(f"Chat Model: {_model}")
        st.info(f"Stored Vectors: {len(get_all_vectors(_provider))}")

        if st.button("Ask Repository", key="ask_repository_btn"):

            if not question.strip():
                st.warning("Please enter a question.")

            else:

                embedding_model = (
                    "text-embedding-3-small"
                    if _provider == "OpenAI"
                    else "nomic-embed-text"
                )

                # ===============================
                # Search Repository
                # ===============================
                with st.spinner(f"🔍 Searching repository using {search_type} search..."):

                    if search_type == "Semantic":
                        chunks = search_repository(
                            question=question,
                            provider=_provider,
                            embedding_model=embedding_model,
                            top_k=10
                        )

                    elif search_type == "BM25":
                        chunks = bm25_search(
                            question=question,
                            provider=_provider,
                            top_k=10
                        )

                    else:
                        chunks = hybrid_search(
                            question=question,
                            provider=_provider,
                            embedding_model=embedding_model,
                            top_k=10
                        )

                # ===============================
                # Re-rank Results
                # ===============================
                with st.spinner("📊 Re-ranking retrieved chunks..."):

                    chunks = rerank_chunks(
                        question=question,
                        chunks=chunks,
                        provider=_provider,
                        model=_model,
                        top_k=3
                    )

                st.success(f"Retrieved {len(chunks)} relevant chunks")

                for i, item in enumerate(chunks, start=1):
                    label = (
                        f"Chunk: {i}    |    "
                        f"Score: {item['score']:.4f}    |    "
                        f"Search: {item.get('search_type', 'Semantic')}"
                    )

                    with st.expander(label):
                        st.write(f"Source: {item['source']}  ")
                        st.code(item["chunk"], language="python")


                # ===============================
                # Generate Answer
                # ===============================
                with st.spinner("🤖 Generating AI answer..."):

                    result = answer_question(
                        question=question,
                        chunks=chunks,
                        provider=_provider,
                        model=_model
                    )

                st.subheader("💡 Answer")

                if isinstance(result, dict):

                    st.write(result["answer"])

                    st.subheader("📚 Sources Used")

                    for s in result["sources"]:
                        st.write("📄", s)

                else:
                    st.write(result)

                increment_stat("questions_asked")


    # ── Tab 6: Logs ───────────────────────────────────────────────────────────
    with tab6:
        st.subheader("Application Logs")

        col_view, col_clear = st.columns(2)

        with col_view:
            if st.button("View Logs"):
                if os.path.exists("src/logs/app.log"):
                    with open("src/logs/app.log", "r", encoding="utf-8") as f:
                        logs = f.read()
                    st.text_area("Log Output", logs, height=400)
                else:
                    logger.warning("Log file not found when View Logs clicked")
                    st.warning("No log file found.")

        with col_clear:
            if st.button("Clear Logs"):
                try:
                    with open("src/logs/app.log", "w", encoding="utf-8") as f:
                        f.write("")
                    st.success("Logs cleared successfully")
                    logger.info("Logs cleared by user")
                except Exception as e:
                    st.error(f"Error clearing logs: {str(e)}")
                    logger.error(f"Clear Logs Error: {str(e)}")

    # ── Tab 7: Code Explainer ─────────────────────────────────────────────────
    with tab7:
        st.subheader("🤖 Code Explainer Agent")

        if st.session_state.repo_loaded:
            file_paths = [file["path"] for file in files]
            selected_file = st.selectbox("Select File", file_paths)

            if st.button("Explain Code"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()

                    with st.spinner("Analyzing Code..."):
                        # provider + model forwarded so the agent can call
                        # OpenAI or Ollama depending on the sidebar selection.
                        explanation = explain_code(
                            code,
                            model=_model,
                            provider=_provider
                        )

                    st.subheader("Code Explanation")
                    st.write(explanation)
                    increment_stat("agents_used")
                    logger.info(f"Code explained: {selected_file}")

                except Exception as e:
                    logger.error(f"Code Explainer Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 8: Documentation Generator ───────────────────────────────────────
    with tab8:
        st.subheader("📚 Documentation Generator")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="doc_file"
            )

            if st.button("Generate Documentation"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:500]

                    with st.spinner("Generating Documentation..."):
                        documentation = generate_documentation(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Generated Documentation")
                    st.write(documentation)
                    increment_stat("agents_used")
                    logger.info(f"Documentation generated: {selected_file}")

                except Exception as e:
                    logger.error(f"Documentation Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 9: Bug Finder ─────────────────────────────────────────────────────
    with tab9:
        st.subheader("🐞 Bug Finder Agent")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="bug_file"
            )

            if st.button("Find Bugs"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Analyzing Code..."):
                        result = find_bugs(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Bug Analysis")
                    st.write(result)
                    increment_stat("agents_used")
                    logger.info(f"Bug analysis completed: {selected_file}")

                except Exception as e:
                    logger.error(f"Bug Finder Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 10: Unit Test Generator ───────────────────────────────────────────
    with tab10:
        st.subheader("🧪 Unit Test Generator")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="test_file"
            )

            if st.button("Generate Tests"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Generating Tests..."):
                        tests = generate_tests(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Generated Unit Tests")
                    st.code(tests, language="python")
                    increment_stat("agents_used")
                    logger.info(f"Tests generated for: {selected_file}")

                except Exception as e:
                    logger.error(f"Test Generator Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 11: Refactoring Agent ─────────────────────────────────────────────
    with tab11:
        st.subheader("♻️ Refactoring Agent")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="refactor_file"
            )

            if st.button("Analyze Refactoring"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Analyzing Code..."):
                        suggestions = refactor_code(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Refactoring Suggestions")
                    st.write(suggestions)
                    increment_stat("agents_used")
                    logger.info(
                        f"Refactoring analysis completed: {selected_file}"
                    )

                except Exception as e:
                    logger.error(f"Refactoring Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 12: Dependency Analyzer ───────────────────────────────────────────
    with tab12:
        st.subheader("📦 Dependency Analyzer")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="dependency_file"
            )

            if st.button("Analyze Dependencies"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Analyzing Dependencies..."):
                        analysis = analyze_dependencies(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Dependency Analysis")
                    st.write(analysis)
                    increment_stat("agents_used")
                    logger.info(
                        f"Dependency analysis completed: {selected_file}"
                    )

                except Exception as e:
                    logger.error(f"Dependency Analyzer Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 13: Architecture Analyzer ─────────────────────────────────────────
    with tab13:
        st.subheader("🏗 Architecture Analyzer")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="architecture_file"
            )

            if st.button("Analyze Architecture"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Analyzing Architecture..."):
                        result = analyze_architecture(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Architecture Report")
                    st.write(result)
                    increment_stat("agents_used")
                    logger.info(
                        f"Architecture analysis completed: {selected_file}"
                    )

                except Exception as e:
                    logger.error(f"Architecture Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 14: API Documentation Generator ──────────────────────────────────
    with tab14:
        st.subheader("📘 API Documentation Generator")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="api_doc_file"
            )

            if st.button("Generate API Docs"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Generating Documentation..."):
                        result = generate_api_docs(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("API Documentation")
                    st.write(result)
                    increment_stat("agents_used")
                    logger.info(f"API docs generated: {selected_file}")

                except Exception as e:
                    logger.error(f"API Docs Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 15: Code Flow Analyzer ────────────────────────────────────────────
    with tab15:
        st.subheader("🔄 Code Flow Analyzer")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="flow_file"
            )

            if st.button("Analyze Code Flow"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Analyzing Code Flow..."):
                        result = analyze_code_flow(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Code Flow Report")
                    st.write(result)
                    increment_stat("agents_used")
                    logger.info(f"Code flow analyzed: {selected_file}")

                except Exception as e:
                    logger.error(f"Code Flow Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 16: Multi-File Analyzer ───────────────────────────────────────────
    with tab16:
        st.subheader("🧠 Multi-File Understanding")

        if st.session_state.repo_loaded:
            if st.button("Analyze Repository Relationships"):
                try:
                    combined_code = ""
                    for file in files[:10]:
                        try:
                            with open(
                                file["path"], "r",
                                encoding="utf-8", errors="ignore"
                            ) as f:
                                combined_code += f"\n\n=== {file['name']} ===\n"
                                combined_code += f.read()[:1000]
                        except Exception:
                            pass

                    with st.spinner("Analyzing Repository..."):
                        result = analyze_multiple_files(
                            combined_code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Repository Relationships")
                    st.write(result)
                    increment_stat("agents_used")
                    logger.info("Multi-file analysis completed")

                except Exception as e:
                    logger.error(f"Multi File Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 17: Security Analyzer ─────────────────────────────────────────────
    with tab17:
        st.subheader("🔐 Security Analyzer")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="security_file"
            )

            if st.button("Analyze Security", key="security_btn"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Analyzing Security..."):
                        result = analyze_security(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Security Report")
                    st.write(result)
                    increment_stat("agents_used")
                    logger.info(
                        f"Security analysis completed: {selected_file}"
                    )

                except Exception as e:
                    logger.error(f"Security Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 18: Code Reviewer ─────────────────────────────────────────────────
    with tab18:
        st.subheader("👨‍💻 Code Reviewer")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="review_file"
            )

            if st.button("Review Code", key="review_btn"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Reviewing Code..."):
                        result = review_code(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Code Review Report")
                    st.write(result)
                    increment_stat("agents_used")
                    logger.info(f"Code reviewed: {selected_file}")

                except Exception as e:
                    logger.error(f"Review Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 19: PR Review Agent ───────────────────────────────────────────────
    with tab19:
        st.subheader("📝 Pull Request Review Agent")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="pr_file"
            )

            if st.button("Review Pull Request", key="pr_btn"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Reviewing PR..."):
                        result = review_pull_request(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("PR Review Report")
                    st.write(result)
                    increment_stat("agents_used")
                    logger.info(f"PR review completed: {selected_file}")

                except Exception as e:
                    logger.error(f"PR Review Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 20: Feature Generator ─────────────────────────────────────────────
    with tab20:
        st.subheader("⚡ Feature Generator")

        if st.session_state.repo_loaded:
            selected_file = st.selectbox(
                "Select File",
                [file["path"] for file in files],
                key="feature_file"
            )

            if st.button("Generate Features", key="feature_btn"):
                try:
                    with open(
                        selected_file, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        code = f.read()[:3000]

                    with st.spinner("Generating Features..."):
                        result = generate_features(
                            code,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Suggested Features")
                    st.write(result)
                    increment_stat("agents_used")
                    logger.info(f"Features generated: {selected_file}")

                except Exception as e:
                    logger.error(f"Feature Generator Error: {str(e)}")
                    st.error(str(e))
        else:
            st.warning("Load a repository first.")

    # ── Tab 21: Code Generator ────────────────────────────────────────────────
    with tab21:
        st.subheader("🚀 Code Generator")

        requirement = st.text_area(
            "Enter Requirement",
            height=150,
            key="code_requirement"
        )

        if st.button("Generate Code", key="generate_code_btn"):
            if requirement.strip():
                try:
                    with st.spinner("Generating Code..."):
                        result = generate_code(
                            requirement,
                            provider=_provider,
                            model=_model
                        )

                    st.subheader("Generated Code")
                    st.code(result, language="python")
                    logger.info("Code generated successfully")
                    increment_stat("agents_used")

                except Exception as e:
                    logger.error(f"Code Generator Error: {str(e)}")
                    st.error(str(e))
            else:
                st.warning("Please enter a requirement.")

    # ── Tab 22: Analytics Dashboard ───────────────────────────────────────────
    with tab22:
        st.subheader("📊 Analytics Dashboard")

        if st.session_state.repo_loaded:
            stats = get_dashboard_stats(files)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Files", stats["total_files"])
            with col2:
                st.metric("Total Lines", stats["total_lines"])

            st.markdown("---")
            st.subheader("Extensions Distribution")
            st.bar_chart(stats["extensions"])

            st.markdown("---")
            st.subheader("Extension Counts")
            for ext, count in stats["extensions"].items():
                st.write(f"{ext} : {count}")

            st.markdown("---")
            st.subheader("Debug Information")
            st.write(f"Files Found: {len(files)}")

            for file in files:
                st.write("File Object:", file)
                try:
                    file_path = file["path"]
                    st.write(f"Path: {file_path}")
                    st.write(f"Exists: {os.path.exists(file_path)}")
                    with open(
                        file_path, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        line_count = len(f.readlines())
                    st.success(f"{file['name']} -> {line_count} lines")
                except Exception as e:
                    st.error(f"{file.get('name', 'Unknown')} -> {str(e)}")
        else:
            st.warning("Load a repository first.")

    # ── Tab 23: Export Report ─────────────────────────────────────────────────
    with tab23:
        st.subheader("📄 Export Report")

        report_text = st.text_area(
            "Report Content",
            height=300,
            placeholder="Paste AI analysis here..."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Export PDF", key="pdf_export"):
                path = export_pdf(report_text, "repository_report.pdf")
                increment_stat("reports_generated")
                with open(path, "rb") as f:
                    st.download_button(
                        "Download PDF", f,
                        file_name="repository_report.pdf",
                        mime="application/pdf"
                    )

        with col2:
            if st.button("Export DOCX", key="docx_export"):
                path = export_docx(report_text, "repository_report.docx")
                increment_stat("reports_generated")
                with open(path, "rb") as f:
                    st.download_button(
                        "Download DOCX", f,
                        file_name="repository_report.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

        with col3:
            if st.button("Export TXT", key="txt_export"):
                path = export_txt(report_text, "repository_report.txt")
                increment_stat("reports_generated")
                with open(path, "rb") as f:
                    st.download_button(
                        "Download TXT", f,
                        file_name="repository_report.txt",
                        mime="text/plain"
                    )

    # ── Tab 24: Settings ──────────────────────────────────────────────────────
    # ── Tab 24: Settings ─────────────────────────────────────

    with tab24:

        st.subheader("⚙️ Application Settings")

        settings = load_settings()

        # Theme
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark"],
            index=0 if settings.get("theme", "Light") == "Light" else 1
        )

        # Provider
        provider = st.selectbox(
            "AI Provider",
            ["Ollama", "OpenAI"],
            index=0 if settings.get(
                "provider",
                "Ollama"
            ) == "Ollama" else 1
        )

        # Dynamic Models
        if provider == "Ollama":

            models = [
                "qwen2.5:1.5b",
                "deepseek-coder:latest",
                "gemma2:2b",
                "phi3:latest",
                "gemma3:4b",
                "mistral:latest",
                "llama3:8b",
                "llama3.1:8b",
                "qwen3:latest"
            ]

        else:

            models = [
                "gpt-4o-mini",
                "gpt-4o"
            ]

        default_model = settings.get(
            "default_model",
            models[0]
        )

        model_index = (
            models.index(default_model)
            if default_model in models
            else 0
        )

        model = st.selectbox(
            "Default Model",
            models,
            index=model_index
        )

        # RAG Search
        top_k = st.slider(
            "Default Top K",
            min_value=1,
            max_value=20,
            value=settings.get(
                "top_k",
                5
            )
        )

        # Save Settings
        if st.button(
                "💾 Save Settings",
                key="settings_btn"
        ):
            save_settings({

                "theme": theme,

                "provider": provider,

                "default_model": model,

                "top_k": top_k

            })

            # Update Session State

            st.session_state.provider = provider

            st.session_state.selected_model = model

            st.session_state.top_k = top_k

            st.success(
                "Settings Saved Successfully"
            )

            logger.info(
                f"Settings Updated | "
                f"Provider={provider} | "
                f"Model={model} | "
                f"TopK={top_k}"
            )

    # ── Tab 25: Usage Statistics ──────────────────────────────────────────────
    with tab25:
        st.subheader("📈 Usage Statistics")

        stats = get_usage_stats()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Repositories Loaded", stats["repository_loaded"])
            st.metric("Questions Asked", stats["questions_asked"])

        with col2:
            st.metric("Reports Generated", stats["reports_generated"])
            st.metric("Agents Used", stats["agents_used"])