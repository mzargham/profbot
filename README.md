# Profbot: Standarized Testing Framework

## Overview

Profbot is a specialized framework designed to standardize the testing and evaluation of Language Learning Models (LLMs). Drawing inspiration from the academic world, Profbot adopts an analogy where the LLMs are students, the examiners are teaching assistants (TAs), and the exam creators are professors. 

In this framework:
- **Professors (Exam Creators):** Define exams, complete with guidelines and a clear evaluation schema, ensuring that the assessment criteria are transparent and consistent.
- **Students (LLMs):** Take these exams, demonstrating their understanding and application of various subjects.
- **Teaching Assistants (TAs):** Grade the exams, providing structured feedback in a standardized format, which allows for an objective comparison of performances across different 'students' (LLMs).

The importance of this framework lies in its ability to standardize the resulting data, ensuring that the performance of different LLMs can be compared fairly and effectively. This standardized approach is crucial in evaluating and improving the capabilities of LLMs in various domains.

## Repository Structure

The repository is organized into several key components:

- **`readme.md`**: Provides an overview and guide to the repository.
- **`exam.py`**:
  - Contains the `Exam` class, which defines the structure of exams. 
  - Includes guidelines for both the overall exam and individual questions, as well as a schema for standardized output.

- **`llmtest.py`**:
  - Features the `Llm` class, a wrapper for LLM interaction.
  - Includes the `LLMTest` class, which orchestrates the process of administering an exam to a student LLM and having it evaluated by a TA LLM.

- **`examples/`** (Directory):
  - **`aiexam.py`**: An example file showing how to define a specific exam (in this case, related to AI) using the framework.
  - **`aitest.py`**: Demonstrates the process of conducting an AI exam using the `LLMTest` class.

Each component of the repository plays a crucial role in facilitating the standardized testing and evaluation of LLMs, mirroring the roles found in an academic setting. This structure ensures that the framework is both flexible and robust, capable of handling a variety of testing scenarios in the context of LLM evaluation.

---

This README provides a concise yet comprehensive guide to the purpose and structure of your repository. You can expand each section with more details as needed, especially if there are specific requirements or configurations for using the framework.