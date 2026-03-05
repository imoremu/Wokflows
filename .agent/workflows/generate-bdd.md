---
description: Generates a new BDD feature file following project standards
---

# Generate BDD Workflow

This workflow guides the agent in creating a new BDD feature file using the `bdd-generator` skill.

1.  **Analyze Request**:
    *   Identify the functionality to be tested.
    *   Determine the target component (HMI, CTX, AI, LC).

2.  **Read Skill**:
    *   Read `skills/bdd-generator/SKILL.md` to load the standards and template.

3.  **Draft Content**:
    *   Create the Gherkin content following the **English Keywords + Spanish Content** rule.
    *   Ensure proper tagging (`@ui`, `@api`, etc.).
    *   Include references to Requirements (RF-XXX).

4.  **Create File**:
    *   Use `write_to_file` to create the `.feature` file in `<componente>/tests/features/`.

5.  **Review**:
    *   Ask the user to confirm the scenarios before proceeding to step definitions.
