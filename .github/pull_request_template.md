name: Pull Request
description: Template for pull requests
title: ""
body:
  - type: markdown
    attributes:
      value: |
        Thanks for contributing to F1 WHO IS BETTER DRIVER? 🏎️
        
        Please make sure you've read our [Contributing Guidelines](CONTRIBUTING.md) before submitting.

  - type: dropdown
    id: pr-type
    attributes:
      label: Type of Change
      description: What type of change does this PR introduce?
      options:
        - Bug fix (non-breaking change which fixes an issue)
        - New feature (non-breaking change which adds functionality)  
        - Breaking change (fix or feature that would cause existing functionality to not work as expected)
        - Documentation update
        - Code refactoring
        - Performance improvement
        - Dependency update
        - Other
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the changes you've made
      placeholder: |
        ## What
        Brief description of what was changed
        
        ## Why  
        Why was this change necessary?
        
        ## How
        How was it implemented?
    validations:
      required: true

  - type: textarea
    id: related-issues
    attributes:
      label: Related Issues
      description: Link any related issues
      placeholder: |
        Fixes #123
        Closes #456
        Related to #789

  - type: checkboxes
    id: testing
    attributes:
      label: Testing
      description: How has this been tested?
      options:
        - label: Unit tests added/updated
        - label: Integration tests added/updated  
        - label: Manual testing performed
        - label: Web interface tested
        - label: CLI functionality tested
        - label: F1 data functionality tested

  - type: textarea
    id: test-details
    attributes:
      label: Test Details
      description: Describe the testing you performed
      placeholder: |
        - Test environment: 
        - Test data used:
        - Test scenarios covered:

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      description: Please confirm the following
      options:
        - label: My code follows the project's style guidelines
        - label: I have performed a self-review of my code
        - label: I have commented my code, particularly in hard-to-understand areas
        - label: I have made corresponding changes to the documentation
        - label: My changes generate no new warnings
        - label: I have added tests that prove my fix is effective or that my feature works
        - label: New and existing unit tests pass locally with my changes

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots (if applicable)
      description: Add screenshots to help explain your changes

  - type: textarea
    id: additional-notes
    attributes:
      label: Additional Notes
      description: Any additional information you'd like to provide