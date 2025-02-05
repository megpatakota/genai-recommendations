# Documentation for GenAI-Based Recommendation Service

## Table of Contents
1. [Prompt/Model Approach](#promptmodel-approach)
2. [Data Integration](#data-integration)
3. [System Design](#system-design)
4. [Trade-Offs & Next Steps](#trade-offs--next-steps)

---

## Prompt/Model Approach

### Model Choice
This project employs OpenAI's `gpt-4o-mini` to power its recommendation engine. Reasons for using this model in the MVP:
- **High-Quality Structured Outputs**: Produces coherent, context-sensitive responses that conform to a JSON schema.
- **Cost-Effective**: Budget-friendly solution compared to larger models. 
- **Minimal Overhead**: Hosted by OpenAI, removing the need for in-house infrastructure.  
- **Scalable**: High rate limits with their real-time endpoint, which can be updated to the lower-cost batch endpoint post-MVP.
  
This model is suitable for:
- Generating human-readable explanations.
- Interpreting structured data like user profiles and transaction history.
- Contextually linking diverse data points (e.g., dining preferences and location).

### Prompt Design
Prompts are dynamically crafted using **Jinja2 templates** to ensure:
- **Clarity**: Each user’s data (e.g., profile details, transaction history) is presented to the LLM in a structured format.
- **Flexibility**: Easy to adapt for new data fields or experience categories.
- **Organised**: Use of Jinja2 templates avoids having disorganised prompts spread throughout a codebase. It allows for centralised, organised prompt management.

[Find all prompt templates used](../backend/templates/)

#### Example Prompt Structure:
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

## Available Experiences
- Experience Title: Weekend Surf Trip
  - Category: Adventure
- Experience Title: Yoga & Mindfulness Retreat
  - Category: Wellness

## Personalised Experience Recommendations
Based on the user's past experiences and recent transactions, suggest 3 new experiences this user might enjoy.
```

The system sends the above prompt to the LLM, which responds with structured recommendations and corresponding justifications.

---

## Data Integration

### Member Data
The `members` dataset contains:
- **Profile Information**: Name, location, and unique member ID.
- **Historical Data**:
  - `past_redeemed_offers`: Records of previously redeemed experiences.
  - `card_transactions`: Transaction history with merchant names, categories, and amounts.

### Experience Data
The `experiences` dataset includes:
- **Attributes**: Experience title, category, description, price range, and availability dates.
- **Exclusions**: Experiences already redeemed by the user are filtered out.

### Integration Flow
1. **Data Preparation**:
   - Filter and format user-specific data (e.g., exclude redeemed experiences).
   - Convert transactions into a human-readable format (e.g., `£45.32`).
2. **Dynamic Prompt Generation**:
   - Inject the prepared data into a Jinja2 template.
   - Ensure consistent formatting for LLM consumption.
3. **LLM Query**:
   - Submit the generated prompt to OpenAI GPT.
   - Parse and validate the returned recommendations.

---

## System Design
![Architecture](../images/ProcessDiagram.png)

### Architecture Overview
The system is modular, with clearly separated responsibilities for data preparation, prompt generation, and recommendation display. 

#### Key Components:
1. **Frontend**:
   - **Streamlit UI**: Captures user input (Member ID) and displays recommendations.
2. **Backend**:
   - **Prompt Preparation**: Combines member and experience data into a structured prompt using Jinja2.
   - **LLM Integration**: Sends prompts to OpenAI GPT and processes the results.
3. **Deployment**:
   - **Docker**: Ensures consistent deployment across environments.

### Workflow Diagram:
The workflow adheres to the architecture outlined in the provided diagram:
1. **Input Capture**: User enters Member ID in the Streamlit interface.
2. **Prompt Creation**: Member data and available experiences are combined into a structured prompt.
3. **LLM Processing**: OpenAI GPT generates recommendations.
4. **Output Display**: Recommendations are rendered in the Streamlit UI.

---

## Trade-Offs & Next Steps

1. **Cost**:
   - **Current**: At very large production-level scales, the cost of this solution might not be worth it. However, the benefit is a rapid MVP to gain buy-in for future development.
   - **Future**: Evaluate OpenAI's batch processing endpoint, or building in-house infrastructure to run a batch processing task using open-source LLMs such as Phi-4, Llama 3.1 or Gemma 2.
2. **Data Storage**:
   - **Current**: JSON files provide a lightweight, easy-to-edit solution for MVP development.
   - **Future**: Transition to a relational database (e.g., PostgreSQL) for scalability.
3. **Frontend**:
   - **Current**: Streamlit is ideal for demos but lacks the flexibility of modern front-end frameworks.
   - **Future**: The recommendations should be integrated into the live application.
