# IMAGO Coding Challenge – Backend-Focused Submission

## Overview

This document outlines my solution to the IMAGO coding challenge. I chose to emphasise the backend implementation, building a robust and modular FastAPI-based service that interacts with the provided Elasticsearch index, retrieves and normalises media content, and exposes an API endpoint for clients to consume.

The source code is available at: [[GITHUB](https://github.com/vasekw/imago)]

The service is also hosted on the free-tier of Render: [[API Docs](https://imago-f5x4.onrender.com/api/docs)] 
(note that the initial request can take time as the container spins down after 15 minutes of inactivity)

## Features Implemented

- API using **FastAPI**
- Integration with  `elasticsearch_dsl`
- Media search and filtering based on keyword, metadata field, sort criteria, and pagination
- Construction of media thumbnail URLs using the provided schema
- Graceful handling of unstructured or missing fields (e.g. fallback from `description` to `suchtext`)
- Dependency injection using `dependency_injector`
- Structured error handling and logging using `loguru`
- Unit testing with `pytest`

---

## Key Assumptions

- Elasticsearch is used primarily for read access; media data is pre-indexed.
- Media thumbnails can be constructed via the formula: `https://www.imago-images.de/bild/<DB>/<MEDIA_ID.zfill(10)>/s.jpg`
- The following fields are always populated in the data
  - id
  - db
---

## Identified Issue – Inconsistent Field Availability

A key issue encountered during development is inconsistent data across Elasticsearch documents. In particular:

- Fields like `title` and `description` are frequently **absent**.
- A field named `suchtext` often contains a **combined** or fallback text block (sometimes merging title/description), but its structure is unpredictable.

### Performance Impact

- The absence of structured fields like `title` and `description` means that keyword queries relying on them (e.g. `search_by=title`) often yield **no results**, making the filtering mechanism unreliable.
- Search queries that rely on multiple fields (`fields=["title", "description"]`) increase the likelihood of empty matches and wasted query computation.
- Overhead from fallback logic (e.g., manually inspecting `suchtext`) adds complexity and slows down post-query data normalisation.

### Proposed Rectification

1. **Data Pipeline Improvement**:
   - Update the indexing pipeline to ensure that each document contains properly parsed and structured fields: `title`, `description`, and `tags` if applicable.
   - Use natural language processing (NLP) techniques to separate and cleanly extract these fields from raw `suchtext`.

2. **Index Template Enhancements**:
   - Define an Elasticsearch index template that enforces mappings for key fields to avoid inconsistencies.
   - Ensure `title`, `description`, and other metadata fields have defined types and analysers.

3. **Application-Level Mitigation**:
   - Introduce caching for documents with missing fields to avoid repeated transformations.
   - Implement a `normalised_description` field during runtime by parsing `suchtext` intelligently if structured fields are missing.

4. **Frontend Feedback**:
   - When `title` or `description` is not found, indicate this clearly in the UI (e.g., “No structured title available”) instead of leaving it blank.

---

## Scalability & Maintainability

The current architecture supports horizontal scalability and ease of maintenance through several design choices:

### Horizontal Scaling
- The backend is stateless and can be horizontally scaled by running multiple instances behind a load balancer (e.g., using Kubernetes)

### Efficient Querying
- All search queries support pagination, limiting memory and CPU usage per request.
- Optional filters and sorting fields allow for fine-grained control over query complexity and performance impact.
- Asynchronous FastAPI endpoints (using async def) support high concurrency under load.

### Modular Design
- The codebase is divided into isolated modules (client, container, views, etc.) with clearly defined responsibilities.
- New data providers, authentication layers, or feature flags can be added with minimal disruption.

### Cloud-native Readiness
- The app can be deployed using Docker and integrated into CI/CD pipelines for automated testing and delivery. 
- Secrets (e.g., ES credentials) are handled through environment variables or secret managers, allowing secure cloud deployment.

### Maintenance
- Dependency injection makes it easier to mock or swap components during testing and development.
- Centralised configuration via settings.py simplifies management across environments.
- Type-annotated code and Pydantic schemas enable auto-validation and clear API contracts.
- Logging is centralised using `loguru` and can be redirected to monitoring tools.
- Code is structured for testability, with injectable dependencies and isolated units.

---

## Monitoring & Testing

- Structured logs provide traceability for user queries and internal errors.
- Tests are written using `pytest` and include:
  - Mocked Elasticsearch responses
  - Edge case handling (missing fields, no results)
  - Query validation

---

## Potential Enhancements

- Add fuzzy search or synonym support for broader results.
- Extend query filters to include date ranges, photographer, or DB type.
- Rate-limit the API and add caching for repeated queries.
- Frontend client using React/Vue to visualise results.

---

## Conclusion

Thank you for the opportunity!

