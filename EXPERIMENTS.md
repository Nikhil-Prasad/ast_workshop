# AST Workshop - Experiments Roadmap

Foundation-building exercises for compiler/interpreter design and agent framework development.

## Progress Overview
- **Completed:** 1/30 items (3%)
- **In Progress:** AST as Contract (Kata #1)
- **Current Focus:** Lexer complete, studying Pratt parsing next

---

## Full 30-Item Roadmap

### Top 12 Priority Items ⭐

1. ⭐ [IN PROGRESS] AST as contract (IR + invariants)
2. ⭐ [ ] Normalize / Lowering (canonical form)
3. ⭐ [ ] DAG execution + topo scheduling (and cycle detection)
4. ⭐ [ ] Trace schema + replay (event sourcing)
5. ⭐ [ ] Tool registry + schemas + adapters
6. ⭐ [ ] Laws as contracts (property tests for algebra + invariants)
7. ⭐ [ ] Async batching + backpressure (bounded queues)
8. ⭐ [ ] Rate limiting + per-tool profiles (token bucket)
9. ⭐ [ ] Timeouts + retries + idempotency (jittered backoff)
10. ⭐ [ ] Streaming proxy (SSE) + cancellation
11. ⭐ [ ] pgvector schema + indexes + HNSW knobs
12. ⭐ [ ] Hybrid retrieval + rerank + eval gate

### Next Queue (13-30)

13. [ ] DSL surface → AST (keep thin)
14. [ ] Determinism modes (seeded runs, fixed routes, fixed prompts)
15. [ ] Choose as learning seam (bandits/MCTS policies)
16. [ ] Policy hooks + budgeters (pre/post tool hooks)
17. [ ] Document normalization + hashing (idempotent ingestion)
18. [ ] OCR backend abstraction + caching
19. [ ] Layout / ROI detection metrics (IoU) + postprocessing
20. [ ] Table/plot extraction normalization
21. [ ] Chunking strategies + provenance/citations metadata
22. [ ] Embedding pipeline throughput + batching + provider abstraction
23. [ ] Evidence package schema (facts/tables/spans + lineage)
24. [ ] Observability taxonomy (errors, p50/p95, trace IDs)
25. [ ] Gateway routing + capability gating (OpenAI/Azure/vLLM)
26. [ ] Local stack baseline (compose: pg/redis/minio)
27. [ ] JobSpec YAML + runner (repro jobs)
28. [ ] SkyPilot managed jobs (spot-safe)
29. [ ] Artifacts/registry + promotion rules
30. [ ] Packaging with uv extras/groups (lean serve, heavy train)

---

## Top 12 Detailed Breakdown

### ⭐ 1. AST as Contract (IR + Invariants)

**Status:** 🟡 In Progress  
**Why:** Foundation - if AST is frozen, everything else becomes compilers + interpreters + tests

#### 📚 Reading
- [ ] [Compilation course intro to IR](https://www.cs.cornell.edu/courses/cs6120/2020fa/lesson/2/)
- [ ] [Lowering AST → IR perspective](https://thunderseethe.dev/posts/what-even-is-a-lowering-pass/)

#### 🎯 Drills
- [x] **LC 150:** Evaluate Reverse Polish Notation ✓ (stack evaluation = tiny interpreter)
- [ ] **LC 224:** Basic Calculator (expression eval)
- [ ] **LC 297:** Serialize and Deserialize Binary Tree (round-trip contract thinking)
- [ ] **Math:** Write 5 AST invariants and prove they're checkable locally (O(nodes+edges))

#### 🛠️ Repo Kata
**Current Progress:**
- [x] Core AST nodes implemented (`expr_ast.py`)
  - [x] Statement/Expr base classes with `evaluate()` interface
  - [x] Expression nodes: Num, Name, BinOp, Compare, BoolOp, UnaryOp
  - [x] Statement nodes: Assign, Print, If, ForRange
  - [x] Module class for program evaluation
- [x] Lexer implemented (`parse.py`)
  - [x] Token class and token type constants
  - [x] Lexer with `next_token()` method
  - [x] Multi-digit numbers, operators, parentheses, whitespace handling

**Remaining:**
- [ ] Parser (Pratt) - text → AST
- [ ] `validate_ast(ast) -> list[Violation]`
  - [ ] Single START node check
  - [ ] No dangling node refs
  - [ ] Acyclicity where required
  - [ ] Tool nodes have validated args
  - [ ] Type checks
- [ ] Round-trip: `ast -> json -> ast` preserves meaning (canonicalized)
- [ ] Tests:
  - [ ] Unit tests for each invariant
  - [ ] Golden AST fixture (contract regression test)

**Files:** `expr_ast.py`, `parse.py`, `tests/test_ast_invariants.py`

---

### ⭐ 2. Normalize / Lowering (Canonical Form)

**Status:** ⚪ Not Started  
**Why:** Mastery = saying "this is the same program" across superficial differences

#### 📚 Reading
- [ ] [Lowering framing](https://thunderseethe.dev/posts/what-even-is-a-lowering-pass/)

#### 🎯 Drills
- [ ] **LC 133:** Clone Graph
- [ ] **LC 261:** Graph Valid Tree / **LC 207:** Course Schedule (prep)
- [ ] **Math:** Prove idempotence target: `normalize(normalize(x)) == normalize(x)`
- [ ] **Math:** Define "semantic preservation" in your system

#### 🛠️ Repo Kata
- [ ] Implement `normalize(ast)`:
  - [ ] Ensure explicit START node
  - [ ] Stable ordering of nodes/edges (canonical sort)
  - [ ] Eliminate trivial no-ops (optional)
  - [ ] Deterministic IDs (optional but huge for diffability)
- [ ] Tests:
  - [ ] Idempotence test
  - [ ] Equivalence test: two syntactically different ASTs → same canonical form

**Files:** `lower.py` (or `normalize.py`)

---

### ⭐ 3. DAG Execution + Topo Scheduling (Cycle Detection)

**Status:** ⚪ Not Started  
**Why:** Interview-classic + beating heart of orchestration

#### 📚 Reading
- [ ] [Topological sorting overview (Kahn/DFS)](https://en.wikipedia.org/wiki/Topological_sorting)

#### 🎯 Drills
- [ ] **LC 207:** Course Schedule
- [ ] **LC 210:** Course Schedule II
- [ ] **LC 621:** Task Scheduler (resource constraints mental model)
- [ ] **Math:** Prove why cycle detection falls out of Kahn's algorithm

#### 🛠️ Repo Kata
Build `execute(ast, tool_registry, policy) -> Result + Trace`:
- [ ] Topo order for dependencies
- [ ] Detect/report cycles with actionable error
- [ ] Retries with budget (hook into #9 later)
- [ ] Parallel execution for independent nodes (applicative flavor)
- [ ] Emit trace events (tie into #4)

**Files:** Executor module + AST node definitions

---

### ⭐ 4. Trace Schema + Replay (Event Sourcing)

**Status:** ⚪ Not Started  
**Why:** Can't stabilize LLM-assisted code without replayable evidence

#### 📚 Reading
- [ ] [Event Sourcing pattern](https://martinfowler.com/eaaDev/EventSourcing.html)

#### 🎯 Drills
- [ ] **LC 362:** Design Hit Counter (time-indexed events)
- [ ] **LC 981:** Time Based Key-Value Store (event log retrieval)
- [ ] **Math:** Define minimal trace event algebra (append-only log + fold reducer) and show it's a monoid

#### 🛠️ Repo Kata
- [ ] Define strict trace schema:
  - [ ] RunStarted, NodeReady, ToolCalled, ToolReturned, NodeCompleted, RunCompleted, RunFailed
  - [ ] Include: node_id, timestamps, inputs hash, outputs hash, error taxonomy, cost/latency
- [ ] Implement `replay(trace, stub_tools=True)`:
  - [ ] Replays control flow deterministically
  - [ ] Verifies hashes match when deterministic mode enabled
- [ ] Tests:
  - [ ] Golden trace fixture
  - [ ] Replay produces same normalized AST outputs

**Files:** Trace event definitions

---

### ⭐ 5. Tool Registry + Schemas + Adapters

**Status:** ⚪ Not Started  
**Why:** Main "LLMs wrote code" hardening lever - validate everything at boundary

#### 📚 Reading
- [ ] [JSON Schema spec (Core/Validation)](https://json-schema.org/specification)
- [ ] [Pydantic model validation](https://docs.pydantic.dev/)
- [ ] [Function/tool calling reliability](https://help.openai.com/en/articles/6654000-best-practices-for-function-calling-with-chat-completions-api)

#### 🎯 Drills
- [ ] **LC 146:** LRU Cache (registry cache / schema cache instincts)
- [ ] **LC 208:** Implement Trie (schema lookup, tool name routing)
- [ ] **Math:** Define "tool signature" and show validation is `raw_json -> Either[Error, Args]`

#### 🛠️ Repo Kata
- [ ] Build `ToolSpec(name, schema, handler, retryable, idempotent, qps, concurrency, timeout_s)`
- [ ] Implement `call_tool(name, raw_args)`:
  - [ ] Validate args (JSON Schema or Pydantic)
  - [ ] Coerce + reject unknowns
  - [ ] Attach idempotency key support (ties into #9)
  - [ ] Unify provider adapters (OpenAI-style tool call ⇄ internal)
- [ ] Tests:
  - [ ] Schema rejects invalid payloads
  - [ ] Unknown fields rejected
  - [ ] Adapter round-trip

**Files:** Tool wiring / tool config

---

### ⭐ 6. Laws as Contracts (Property Tests)

**Status:** ⚪ Not Started  
**Why:** Final 10-20% formalization - turn laws into tests

#### 📚 Reading
- [ ] [Typeclassopedia](https://wiki.haskell.org/Typeclassopedia) (reference)
- [ ] [Hypothesis intro](https://hypothesis.readthedocs.io/) (property testing mindset)

#### 🎯 Drills
Write 3 property tests (not LC):
- [ ] Monoid associativity for trace reducer / event fold
- [ ] Identity element exists for reducer
- [ ] Normalization idempotence on randomized small graphs
- [ ] **Optional LC 412:** Fizz Buzz (forces property framing over examples)

#### 🛠️ Repo Kata
Add Hypothesis tests for:
- [ ] Normalize idempotence
- [ ] "Compose" associativity in combinators/blueprints (Seq-style nodes)
- [ ] Tool adapter round-trip properties
- [ ] Keep generators tiny (≤20 nodes), bias toward edge cases

**Files:** `tests/test_combinator_blueprints.py`

---

### ⭐ 7. Async Batching + Backpressure (Bounded Queues)

**Status:** ⚪ Not Started  
**Why:** Throughput without fragility - shows up in interviews constantly

#### 📚 Reading
- [ ] [asyncio.Queue semantics](https://docs.python.org/3/library/asyncio-queue.html) (maxsize, backpressure, join/task_done)
- [ ] [Cancellation basics](https://docs.python.org/3/library/asyncio-task.html#task-cancellation)

#### 🎯 Drills
- [ ] **LC 1188:** Design Bounded Blocking Queue
- [ ] **LC 622:** Design Circular Queue (bounded buffer thinking)
- [ ] **Math:** Compute worst-case in-flight: `producers * maxsize + worker batch size`

#### 🛠️ Repo Kata
Implement async batcher:
- [ ] `put(item)` from many producers
- [ ] Emits batch of size N or after T seconds
- [ ] Bounded queue applies backpressure
- [ ] Graceful shutdown with sentinel + join()
- [ ] Integrate: embeddings pipeline batching or tool call batching

Tests:
- [ ] Batch flush by size
- [ ] Batch flush by time
- [ ] Shutdown doesn't drop items

---

### ⭐ 8. Rate Limiting + Per-Tool Profiles (Token Bucket)

**Status:** ⚪ Not Started  
**Why:** Turns "policy" into first-class runtime guarantee

#### 📚 Reading
- [ ] [Token bucket definition](https://en.wikipedia.org/wiki/Token_bucket)
- [ ] [Leaky bucket contrast](https://en.wikipedia.org/wiki/Leaky_bucket)

#### 🎯 Drills
- [ ] **LC 359:** Logger Rate Limiter
- [ ] **LC 362:** Design Hit Counter
- [ ] **Math:** Given (rate=r, burst=b), compute whether request at time t should pass

#### 🛠️ Repo Kata
- [ ] Implement `TokenBucket(rate_per_s, burst)` limiter (async-safe):
  - [ ] `acquire(n=1)` awaits until allowed
- [ ] Attach limiter to ToolSpec:
  - [ ] Per-tool QPS + burst + concurrency cap
- [ ] Tests:
  - [ ] Burst allowed then throttled
  - [ ] Sustained rate respects r
  - [ ] Fairness under concurrency (basic)

---

### ⭐ 9. Timeouts + Retries + Idempotency (Jittered Backoff)

**Status:** ⚪ Not Started  
**Why:** Reliability without retry storms or duplicate side effects

#### 📚 Reading
- [ ] [Exponential backoff + jitter (canonical)](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [ ] [Idempotent requests](https://stripe.com/docs/api/idempotent_requests)
- [ ] [Retry hygiene / retry storms](https://sre.google/sre-book/addressing-cascading-failures/)

#### 🎯 Drills
- [ ] **Math:** Implement backoff schedule variants (full jitter vs equal jitter)
- [ ] **System-design:** Identify which tools are safe to retry vs must be idempotent-keyed

#### 🛠️ Repo Kata
- [ ] Add `RetryPolicy(max_attempts, max_elapsed, base_delay, jitter, retry_on=...)`
- [ ] Add timeouts per node/tool (hard deadline)
- [ ] Add idempotency keys for mutating tools:
  - [ ] Executor attaches key derived from (run_id, node_id, attempt) or stable call signature
- [ ] Tests:
  - [ ] Repeated call with same idempotency key returns cached result
  - [ ] Retries stop after budget
  - [ ] Jitter spreads retries (statistical test ok)

---

### ⭐ 10. Streaming Proxy (SSE) + Cancellation

**Status:** ⚪ Not Started  
**Why:** User-facing responsiveness + cost control + correctness on disconnect

#### 📚 Reading
- [ ] [SSE basics and failure modes](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [ ] [Streaming responses in Starlette/FastAPI](https://www.starlette.io/responses/#streamingresponse)

#### 🎯 Drills
- [ ] **Build-once:** Write minimal SSE server + client and handle disconnect
- [ ] **Math:** Reason about backpressure: what if client reads slower than provider produces?

#### 🛠️ Repo Kata
Implement `/stream` endpoint that:
- [ ] Proxies upstream model stream → downstream SSE
- [ ] Terminates upstream on client disconnect
- [ ] Doesn't buffer whole response
- [ ] Emits structured trace events per chunk (ties to #4)
- [ ] Add integration test with in-process fake upstream generator

**Files:** Gateway or agents service layer

---

### ⭐ 11. pgvector Schema + Indexes + HNSW Knobs

**Status:** ⚪ Not Started  
**Why:** Retrieval quality and latency live or die here - interview-relevant (DB + ANN)

#### 📚 Reading
- [ ] [pgvector index/query options (HNSW params + ef_search)](https://github.com/pgvector/pgvector)
- [ ] [Postgres text search types (tsvector, tsquery)](https://www.postgresql.org/docs/current/textsearch.html)

#### 🎯 Drills
- [ ] **LC 588:** Design In-Memory File System (schema objects, hierarchical IDs)
- [ ] **LC 1268:** Search Suggestions System (retrieval interface instincts)
- [ ] **Math:** Cosine similarity + normalization; explain why cosine needs unit vectors

#### 🛠️ Repo Kata
- [ ] Migration(s):
  - [ ] Vector column + HNSW index
  - [ ] Optional tsvector column + GIN index for sparse retrieval
- [ ] Query wrapper:
  - [ ] Sets `SET LOCAL hnsw.ef_search = ...`
  - [ ] Enforces `ef_search >= k` constraint
- [ ] Tests:
  - [ ] Migration applies
  - [ ] Query uses index path (EXPLAIN in tests or smoke test)

**Files:** Migration file(s)

---

### ⭐ 12. Hybrid Retrieval + Rerank + Eval Gate

**Status:** ⚪ Not Started  
**Why:** Bridge from "it works" to "it stays working"

#### 📚 Reading
- [ ] [Hybrid search concept and weighting](https://weaviate.io/blog/hybrid-search-explained)
- [ ] [Cross-encoder reranking overview](https://www.sbert.net/examples/applications/cross-encoder/README.html)

#### 🎯 Drills
- [ ] **LC 347:** Top K Frequent Elements
- [ ] **LC 215:** Kth Largest Element in an Array
- [ ] **Math:** Write RRF formula and do one hand-computed fusion example (3 docs, 2 rankers)

#### 🛠️ Repo Kata
Implement retrieval pipeline:
- [ ] Sparse retrieve
- [ ] Dense retrieve
- [ ] Fuse (alpha blend or RRF)
- [ ] Rerank (plug-in interface, can start with stub)
- [ ] Add eval gate:
  - [ ] Tiny gold set (10-30 queries) + expected doc IDs / snippets
  - [ ] Metric thresholds (Recall@K, MRR@K)
  - [ ] CI check that blocks regressions
  - [ ] Trace every stage (debug why recall dropped)

**Files:** Memory pipeline + reranker toggle

---

## Notes

**"Done" Definition:** Each item is complete when:
1. ✅ Handwritten 1-pager notes
2. ✅ Drills completed with notes
3. ✅ Repo kata merged with tests passing

**Current Focus:** Completing AST kata #1 (parser implementation next), then proceeding to #2 (Normalize/Lowering).
