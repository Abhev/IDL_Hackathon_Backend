# Mock Debating AI Agent - Backend

This repository houses the powerful backend for the Mock Debating AI Agent, the brain behind the realistic debate simulations. What makes this backend truly unique is its construction: it's built *purely* using **Relevance AI's cutting-edge platform**, leveraging a sophisticated **Agent** coupled with **two distinct tools** – one custom-coded and the other low-code.

---

## About the Project

The Mock Debating AI Agent Backend is responsible for all the core logic, argumentation, and speech generation that drives the debate simulations. It interacts with the frontend to receive user inputs and deliver AI-generated speeches, timers, and debate flow management.

Its architecture is a testament to the power and flexibility of the Relevance AI platform, demonstrating how complex AI functionalities can be achieved with minimal traditional coding effort through intelligent agent design and tool integration.

---

## Architecture Highlights (Powered by Relevance AI)

The core of this backend is an **Agent** built within Relevance AI, designed for intelligent decision-making and content generation in a debate context.

This Agent operates as a **no-code** component, primarily driven by:

* **Prompting:** Sophisticated prompts guide the Agent's reasoning, argumentation structure, and contextual understanding of debate formats and motions.
* **Knowledge:** The Agent is endowed with relevant knowledge bases, allowing it to access and utilize information for constructing coherent and persuasive arguments.

The Agent leverages **two powerful tools** to execute its debate-specific tasks:

1.  **Custom Code Tool:** -- VISIBLE AS PYTHON FILE
    * This tool encapsulates specific, custom-developed logic that was necessary for highly specialized debate functions, which might include:
        * Complex timer management and phase transitions for specific debate formats.
        * Integration with external APIs if required for specific data retrieval not handled by the low-code tool.
    * This tool demonstrates how targeted programming can augment an otherwise no-code agent.

2.  **Low-Code Tool:** -- VISIBLE AS RAI FILE
    * This tool handles more standardized or repetitive tasks, built efficiently using Relevance AI's low-code capabilities. This might include:
        * Standard text generation and formatting based on debate roles.
        * Basic motion parsing and topic analysis.
        * Data retrieval and manipulation from structured sources within the Relevance AI ecosystem.
    * It exemplifies how rapid development can be achieved for common AI workflows.

---

## Key Responsibilities

The Backend Agent handles crucial aspects of the debate simulation, including:

* **Argument Generation:** Formulating compelling arguments and rebuttals based on the debate motion and current state.
* **Speech Composition:** Crafting full speeches that adhere to the style and requirements of each debate format (e.g., Opening Government, Opposition Leader, POIs).
* **Debate Flow Management:** Tracking turns, time limits, and overall progression of the debate.
* **Role Adherence:** Ensuring the AI speakers stay true to their assigned roles (e.g., defining the motion, rebutting, summarizing).
* **Contextual Understanding:** Maintaining context throughout the debate to build on previous arguments and address opposing points effectively.

---

## How it Works (High-Level)

1.  The **frontend** sends a request to the backend, initiating a debate with a chosen format and motion.
2.  The **Relevance AI Agent** (VISIBLE AS RAI FILE) receives this request.
3.  Based on its **Prompting** and **Knowledge**, the Agent determines the next logical action (e.g., generate
   
