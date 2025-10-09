 <!-- Sync Impact Report
 Version change: none → 1.0.0 (MAJOR: Initial definition of project principles)
 Modified principles: All principles updated to match user-specified requirements
 Added sections: None
 Removed sections: None
 Templates requiring updates: ✅ .specify/templates/plan-template.md (updated Constitution Check to align with new principles)
 Follow-up TODOs: RATIFICATION_DATE (original adoption date unknown)
 -->

 # image_to_ascii Constitution

 ## Core Principles

 ### I. Simplicity
 The application MUST be written as simply as possible, avoiding unnecessary complexity. All code MUST prioritize straightforward solutions over elaborate architectures unless complexity is explicitly justified by performance or functional requirements.

 ### II. Separation of Concerns
 Each major feature MUST be modular and separated into its own module. Features MUST not share implementation details unnecessarily, ensuring that changes to one module do not impact others without clear interfaces.

 ### III. Documentation
 Each major feature MUST have a corresponding Markdown file documenting its purpose, implementation, and usage. Documentation MUST be kept up-to-date and include examples where applicable.

 ### IV. Basic Libraries
 The project MUST use only basic libraries such as NumPy for numerical operations and PIL for image processing. No additional libraries beyond these basics are permitted unless explicitly required and justified.

 ### V. First Principles
 Features MUST be implemented from first principles where possible, using relatively advanced math. Solutions MUST derive from fundamental concepts rather than relying on high-level abstractions.

 ## Technology Constraints

 The project is constrained to using NumPy and PIL as the primary libraries. All image processing and numerical computations MUST adhere to these tools. Advanced mathematical implementations MUST be built from basic operations provided by these libraries.

 ## Development Practices

 Development MUST follow the core principles, ensuring modularity, simplicity, and thorough documentation. Each feature implementation MUST include its documentation file as part of the development process. Code reviews MUST verify adherence to these principles.

 ## Governance

 This constitution supersedes all other practices. Amendments require documentation of the rationale, approval from maintainers, and a migration plan if changes affect existing code. All development activities MUST comply with these principles; deviations MUST be justified and documented.

 **Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown | **Last Amended**: 2025-10-09