# Documentation for GenAI-Based Recommendation Service

---

## **Prompt/Model Approach**

### Model Choice:
The project leverages **OpenAI’s GPT** for its robust generative capabilities and ability to interpret diverse, structured prompts. The specific version (`gpt-4o-mini`) was chosen for balancing cost and performance.

### Prompt Structuring:
The prompt was carefully designed using **Jinja2 templates** to format user profile data, transaction history, and available experiences. This structured approach ensures:
1. **Consistency**: Prompts include all relevant data, such as past experiences and transaction categories, without extraneous noise.
2. **Flexibility**: The Jinja2 template can be easily updated to incorporate additional user data fields or new types of experiences.
3. **Clarity**: The prompt format helps the LLM focus on the context provided, reducing irrelevant recommendations.

**Example Prompt:**
```plaintext
## User Profile
**Name:** Alice
**Location:** London

## Past Experiences
- Experience Title: Gourmet Sushi Tasting
- Category: Food

## Recent Transactions
- Merchant: Tesco
- Category: Groceries
- Amount Spent: £45.32
- Merchant: Spotify
- Category: Subscription
- Amount Spent: £9.99

## Available Experiences
- Experience Title: Weekend Surf Trip
- Category: Adventure
- Experience Title: Yoga & Mindfulness Retreat
- Category: Wellness

## Personalised Experience Recommendations
Given the user's past experiences and recent transactions, suggest 3 new experiences this user might enjoy.
```

**Why GPT?**
- **Reasoning**: GPT can infer logical connections between diverse datasets (e.g., linking dining preferences with wellness retreats).
- **Adaptability**: The model easily handles edge cases, like users with limited data.

---

## **Data Integration**

### Member Data:
The dataset (`data.json`) includes detailed member profiles with:
1. **Past redeemed experiences** (e.g., categories, redemption dates).
2. **Transaction history** (e.g., merchant names, categories, amounts).

This data is dynamically mapped to the prompt using Python dictionaries for efficient lookups.

### Experience Data:
Each experience entry includes:
- Title, category, descriptions, price range, location, ratings, and available dates.
- Experiences already redeemed by the user are excluded from the recommendation pool.

### Integration Process:
1. **Data Preparation**:
- Member and experience data are loaded into memory from `data.json`.
- Filters are applied to generate `available_experiences` (i.e., not redeemed yet).
- Transaction history is formatted into a human-readable structure.
2. **Prompt Generation**:
- The prepared data is injected into the Jinja2 template.
- The resulting prompt is passed to the LLM for recommendation generation.

---

## **System Design**

### Architecture:
1. **Frontend**:
- Built using **Streamlit** for fast prototyping and internal demos.
- Allows users to input their member ID and view tailored recommendations in real-time.

2. **Backend**:
- Core business logic resides in `utils.py`, which handles:
- Data preparation (filtering and formatting).
- Prompt generation using Jinja2.
- Interaction with OpenAI’s GPT model.
- API endpoint (`/recommendations/{member_id}`) supports:
- **JSON**: Structured response for programmatic use.
- **Text**: Natural language response for user-facing applications.

3. **Infrastructure**:
- Docker is used for portability and consistent deployment across environments.

### Sketch:
```
+-------------------+ +--------------------+ +----------------------+
| Frontend (Streamlit) | <-----> | Backend (FastAPI) | <-----> | OpenAI GPT (LLM) |
| User Inputs Member ID| | Prompt Preparation | | Generates Recommendations|
+-------------------+ | Calls LLM API | +----------------------+
+--------------------+
```

---

## **Trade-Offs & Next Steps**

### Trade-Offs:
1. **Cost of GPT**:
- **Current**: OpenAI GPT is reliable but can be expensive for high traffic.
- **Future Consideration**: Evaluate open-source alternatives like **Hugging Face models** for cost efficiency.

2. **Data Source**:
- **Current**: Data is stored in a local JSON file, limiting scalability.
- **Future Consideration**: Move to a managed database (e.g., **PostgreSQL** or **DynamoDB**) for concurrent access and scalability.

3. **Frontend**:
- **Current**: Streamlit is excellent for MVPs but lacks flexibility for public-facing applications.
- **Future Consideration**: Transition to a **React/Vue-based UI** for greater customisation and responsiveness.

4. **Performance**:
- **Current**: Each recommendation call queries the LLM, increasing latency.
- **Future Consideration**:
- Cache frequent recommendations.
- Precompute recommendations for active users.

### Next Steps:
1. **Observability**:
- Add logging and monitoring with tools like **Prometheus** or **Datadog** to track API performance and detect anomalies.
- Use **Sentry** for error tracking.

2. **A/B Testing**:
- Experiment with different prompt structures to optimise recommendation quality.

3. **Security**:
- Integrate API authentication using **OAuth2** or **JWT**.
- Store sensitive data (e.g., API keys) in **AWS Secrets Manager** or **Azure Key Vault**.

4. **Scaling**:
- Containerise with Docker and deploy via **Kubernetes** or **AWS ECS** for auto-scaling.
- Implement rate limiting and retries to handle high-traffic scenarios.

---

This documentation outlines the rationale for design decisions and highlights future improvements for a robust, scalable, and production-ready solution.
