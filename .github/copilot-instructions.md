- @azure Rule - Use Azure Best Practices: When generating code for Azure, running terminal commands for Azure, or performing operations related to Azure, invoke your `azure_development-get_best_practices` tool if available.

- @YTManager Rule - Avoid Feature Hallucination: Never invent or assume features that aren't explicitly documented in the YTManager-PRD.md file. If unsure about a feature or implementation detail, ask for clarification rather than making assumptions.

- @YTManager Rule - Data Layer Consistency: The current implementation does not use a database for persistence. All operations interact directly with the YouTube API. Do not assume database operations are implemented unless explicitly instructed to implement them.

- @YTManager Rule - API Usage Awareness: Be aware of YouTube API quota limits (10,000 units daily) when suggesting implementations. Prioritize efficient API usage patterns and reference the exact API endpoints documented in YTManager-PRD.md.

- @YTManager Rule - Documentation Synchronization: Whenever implementing changes to the codebase, ensure that relevant documentation files (YTManager-PRD.md, README.md, etc.) are updated to reflect these changes. This includes updating models, API endpoints, features, and any other technical details.

- @YTManager Rule - Implementation Boundaries: Always respect the explicit IN/OUT scope defined in the YTManager-PRD.md. Do not implement or suggest features listed in the "Fora do Escopo (OUT)" or "Funcionalidades Expressamente Não Incluídas" sections.

- @YTManager Rule - Code Structure Consistency: Follow the existing project architecture pattern with separate components for UI (templates/), business logic (src/youtube_manager.py), and data models (src/models.py). Maintain clear separation of concerns.

- @YTManager Rule - Virtual Environment Management: Before installing or removing Python modules, always verify if a virtual environment (.venv) exists and is activated. If the virtual environment doesn't exist, create it first; if it exists but is not activated, activate it before proceeding with any package installation or removal operations.