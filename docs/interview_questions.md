# Interview Questions & Answers

## 1. What problem does this project solve?

This project helps developers analyze, understand, document, review, and improve software repositories using AI-powered agents.

## 2. What is RAG?

RAG (Retrieval Augmented Generation) combines information retrieval with LLM generation. Relevant code chunks are retrieved and provided as context before generating answers.

## 3. Why use RAG instead of sending the whole repository to an LLM?

Large repositories exceed model context limits. RAG retrieves only the most relevant code sections, improving performance and accuracy.

## 4. What AI agents are implemented?

* Code Explainer
* Documentation Generator
* Bug Finder
* Unit Test Generator
* Refactoring Agent
* Security Analyzer
* Code Reviewer
* PR Review Agent
* Feature Generator
* Code Generator

## 5. How does Repository Q&A work?

Repository files are indexed into vector embeddings. User questions are converted into embeddings and matched against indexed code chunks. Relevant chunks are then passed to the LLM.

## 6. Why Streamlit?

Streamlit allows rapid development of interactive AI applications with minimal frontend code.

## 7. How is repository indexing performed?

Repository files are chunked, converted into embeddings, and stored in a vector store for semantic retrieval.

## 8. What challenges did you face?

* Large repository processing
* Context management
* Streamlit reruns
* Local model performance optimization
* File handling and indexing

## 9. What improvements would you make?

* Multi-user support
* Cloud deployment
* Authentication
* CI/CD integration
* Team collaboration features

## 10. What was your role?

Designed, developed, tested, and integrated all repository analysis, RAG, AI agent, dashboard, export, and reporting features.
