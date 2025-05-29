# **HSN Code Validation & Suggestion Agent - Capabilities Demonstration**

Checkout this google docs for checking out chat screenshots: - https://docs.google.com/document/d/10zTMNwemPdpVFOx7Qyf_VL8Sha7NU_ywLEmrIUx-TQE/edit?usp=sharing

## **Overview**

This document demonstrates the comprehensive capabilities of our HSN Code Validation & Suggestion Agent, built using Google's Agent Developer Kit (ADK) and Vertex AI. The agent combines local CSV validation with RAG (Retrieval-Augmented Generation) technology to provide accurate HSN code validation and intelligent suggestions.

## **Core Capabilities**

### **1. Multi-Product Query Handling**

The agent can handle complex queries requesting HSN codes for multiple different products simultaneously.

**Example Query**: _"I want two code one for horse for games and other for horse meat"_

**Agent Response**:

![Multi-Product Query Handling](hsn_agent/documentation/screenshots/1.Multi-Product%20Query%20Handling.png)

- **For "horse for games"**:

  - `01012910` – Horses for polo (score: 0.470574011623741642)
  - `01019010` – LIVE HORSES, ASSES, MULES AND HINNIES - OTHER - HORSES FOR POLO
  - `95010010` – WHEELED TOYS DESIGNED TO BE RIDDEN BY CHILDREN

- **For "horse meat"**:
  - `02050000` – MEAT OF HORSES, ASSES, MULES OR HINNES, FRESH, CHILLED OR FROZEN
  - `02109900` – OTHER
  - `05079010` – HOOF MEAL

_Key Feature_: The agent intelligently separates different product requests and provides relevant codes for each category.

---

### **2. Pattern-Based Code Search**

The agent can find HSN codes based on partial patterns, such as codes ending with specific digits.

**Example Query**: _"I dont remember the exact hsn code but it had 99 in between"_

![Pattern-Based Code Search](hsn_agent/documentation/screenshots/2.Pattern-Based%20Code%20Search.png)

**Agent Response**: The agent found HSN codes containing '99':

- `01012990` – Other (catch-all category under 'LIVE HORSES, ASSES, MULES AND HINNIES')
- `01022990` – OTHER, INCLUDING CALVES
- `01059900` – OTHER (under 'LIVE POULTRY')
- `01069900` – OTHER (under 'LIVE POULTRY')
- `01064990` – Other (under 'OTHER LIVE ANIMALS')

_Key Feature_: Pattern recognition allows users to find codes even with incomplete information.

---

### **3. Direct Code Validation**

The agent provides instant validation for specific HSN codes with complete hierarchical information.

**Example Query**: _"33012912"_

![Direct Code Validation](hsn_agent/documentation/screenshots/3.Direct%20Code%20Validation.png)

**Agent Response**:

- **Code**: `33012912` is valid
- **Description**: CAJEPUT OIL
- **Hierarchy**:
  - `33`: Essential oils and resinoids; perfumery, cosmetic or toilet preparations
  - `3301`: ESSENTIAL OILS (TERPENELESS OR NOT), INCLUDING CONCRETES AND ABSOLUTES
  - `330129`: OTHER
  - `33012912`: CAJEPUT OIL

_Key Feature_: Complete hierarchical breakdown shows the classification structure from broad category to specific product.

---

### **4. Administrative Functions**

The agent includes comprehensive administrative capabilities for corpus management.

**Example Interaction**: _"admin: list all corpus"_

![Administrative Functions](hsn_agent/documentation/screenshots/4.Administrative%20Functions.png)

**Agent Capabilities**:

- List existing corpora (hsn_master, testing, hsn)
- Create new corpora
- Add data from Google Drive links
- Manage RAG datasets

_Key Feature_: Full administrative control over data sources and RAG corpora for optimal performance.

---

### **5. Advanced Pattern Matching**

The agent can find codes ending with specific digit patterns.

**Example Query**: _"it ends with 1223"_

![Advanced Pattern Matching](hsn_agent/documentation/screenshots/5.Advanced%20Pattern%20Matching.png)

**Agent Response**:

- `32041223` – ACID GREEN 28 (CARBOLAN BRILL GREEN 5G)
- `521223` – DYED

_Key Feature_: Precise pattern matching for specific ending sequences.

---

### **6. Flexible Pattern Search with Recommendations**

When exact patterns aren't found, the agent provides closest matches and helpful suggestions.

**Example Query**: _"i cant remember the hsn code but i remember it ends with 333"_

![Flexible Pattern Search](hsn_agent/documentation/screenshots/6.Flexible%20Pattern%20Search.png)

**Agent Response**:

- Found: `30039033` – CALCIUM SENNOSIDE (ending with '33', closest match)
- **Recommendation**: Agent suggests using the `load_hsn_master` tool for more comprehensive results

_Key Feature_: Intelligent fallback with helpful guidance for better search results.

---

### **7. Code Suggestion with Context**

The agent can suggest multiple related codes when an exact match isn't found.

**Example Query**: _"112"_

![Code Suggestion with Context](hsn_agent/documentation/screenshots/7.Code%20Suggestion%20with%20Context.png)

**Agent Response** (when code "112" is not valid): Suggested related codes:

- `9112`: CLOCK CASES AND CASES OF A SIMILAR TYPE FOR OTHER GOODS
- `8112`: BERYLLIUM, CHROMIUM, HAFNIUM, RHENIUM, THALLIUM, CADMIUM, GERMANIUM, VANADIUM, GALLIUM
- `7112`: WASTE AND SCRAP OF PRECIOUS METAL
- `6112`: TRACK SUITS, SKI SUITS AND SWIMWEAR
- `5112`: WOVEN FABRICS OF COMBED WOOL

_Key Feature_: Contextual suggestions help users find the correct code even when their initial query is incomplete.

---

### **8. Multi-Code Validation**

The agent can validate multiple HSN codes simultaneously with detailed hierarchical information.

**Example Query**: _"03029910, 030312, 05119929 and 09042110"_

![Multi-Code Validation](hsn_agent/documentation/screenshots/8.Multi-Code%20Validation.png)

**Agent Response**: Detailed validation for each code:

- `03029910`: Fish fins other than shark fins (with complete hierarchy)
- `030312`: OTHER PACIFIC SALMON (with hierarchy)
- `05119929`: OTHER (animal products)
- `09042110`: OF GENUS CAPSICUM (spices)

_Key Feature_: Batch processing capability with comprehensive hierarchical information for each code.

---

### **9. Natural Language Product Queries**

The agent excels at understanding natural language descriptions and finding relevant HSN codes.

**Example Query**: _"shark have a feature on their body i want the code for that"_

![Natural Language Product Queries](hsn_agent/documentation/screenshots/9.Natural%20Language%20Product%20Queries.png)

**Agent Response**: Shark-related HSN codes:

- `03039200`: SHARK FINS
- `03039210`: Shark fins
- `03038992`: EDIBLE SHARK FINS OF WILD LIFE
- `030381`: DOGFISH AND OTHER SHARKS
- `030447`: DOGFISH AND OTHER SHARKS
- `03038190`: OTHER SHARKS
- `03044700`: Dogfish and other sharks
- `03044920`: SHARK
- `03038110`: DOGFISH

_Key Feature_: Understanding of product features and biological characteristics to suggest relevant codes.

---

### **10. Contextual Code Resolution**

When faced with ambiguous queries, the agent provides context and asks for clarification.

**Example Query**: _"1234"_ → Follow-up: _"yes it is related to wood"_

![Contextual Code Resolution](hsn_agent/documentation/screenshots/10.Contextual%20Code%20Resolution.png)

**Agent Response**: After clarification, the agent found:

- `441234`: OTHER, WITH AT LEAST ONE OUTER PLY OF NON-CONIFEROUS WOOD NOT SPECIFIED UNDER SUB-HEADING 4412 33
- **Hierarchy**:
  - `44`: Wood and articles of wood; wood charcoal
  - `4412`: PLYWOOD, VENEERED PANELS AND SIMILAR LAMINATED WOOD
  - `441234`: OTHER, WITH AT LEAST ONE OUTER PLY OF NON-CONIFEROUS WOOD

_Key Feature_: Interactive clarification process leads to accurate code identification.

---

### **11. Specific Product Identification**

The agent can provide exact HSN codes for specific products with high accuracy.

**Example Query**: _"what is the hsn code for horse in polo"_

![Specific Product Identification](hsn_agent/documentation/screenshots/11.Specific%20Product%20Identification.png)

**Agent Response**:

- **HSN Code**: `01012910` for horses used for polo

_Key Feature_: Direct, accurate responses for specific product categories.

---

### **12. Specialized Product Categories**

The agent can handle queries for specialized or unique products.

**Example Query**: _"what is the hsn code for spaceship"_

![Specialized Product Categories](hsn_agent/documentation/screenshots/12.Specialized%20Product%20Categories.png)

**Agent Response**:

- `88026000` – SPACECRAFT (INCLUDING SATELLITES) AND SUBORBITAL AND SPACECRAFT LAUNCH VEHICLES

_Key Feature_: Coverage of specialized and high-tech product categories.

---

### **13. Creative Product Interpretation**

The agent can interpret creative or fictional product queries and provide relevant alternatives.

**Example Query**: _"what is for hsn code flying mermaid"_

![Creative Product Interpretation](hsn_agent/documentation/screenshots/13.Creative%20Product%20Interpretation.png)

**Agent Response**: The agent recognized this as a fantastical item and suggested:

- `88069900` – UNMANNED AIRCRAFT - OTHER (for flying toys)
- `95089000` – ROUNDABOUTS, SWINGS, SHOOTING GALLERIES AND OTHER FAIRGROUND AMUSEMENTS

_Key Feature_: Creative interpretation with practical alternatives for unusual queries.

---

### **14. Mythical Product Handling**

The agent appropriately handles queries for non-existent products while providing helpful alternatives.

**Example Query**: _"what is the hsn code for dragon meat"_

![Mythical Product Handling](hsn_agent/documentation/screenshots/14.Mythical%20Product%20Handling.png)

**Agent Response**: The agent explained that dragons are mythical, but provided meat-related codes:

- `02071100` – MEAT AND EDIBLE OFFAL OF POULTRY (FRESH, CHILLED OR FROZEN)
- `02085000` – OTHER MEAT AND EDIBLE MEAT OFFAL (OF REPTILES)
- `02109300` – MEAT AND EDIBLE MEAT OFFAL (OTHER, INCLUDING EDIBLE FLOURS AND MEALS)

_Key Feature_: Educational responses with practical alternatives for impossible queries.

---

## **Key Technical Features**

### **Dual Validation System**

- **Local CSV**: Instant validation against master HSN database
- **RAG Technology**: Semantic search for natural language queries

### **Intelligent Query Processing**

- Pattern recognition (ends with, contains, begins with)
- Multi-product query handling
- Context-aware suggestions

### **Comprehensive Data Management**

- Master CSV with lazy loading
- Multiple corpus support
- Administrative tools for data updates

### **Advanced Matching Algorithms**

- Exact code validation
- Hierarchical code breakdown
- Semantic similarity scoring

### **Natural Language Understanding**

- Product description interpretation
- Feature-based code suggestions
- Creative query handling
