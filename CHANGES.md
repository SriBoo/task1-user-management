# CHANGES.md

## 🔍 Issues Identified in Legacy Code

1. **Poor Code Structure**
   - All logic in a single file with mixed concerns (routing, logic, DB).
2. **No HTML Styling**
   - No frontend support; not user-friendly.
3. **No Error Handling**
   - No try/except blocks for DB operations.
4. **Hardcoded Database Logic**
   - No abstraction or reuse of code for DB queries.
5. **No Separation of API and Frontend**

---

## ✅ Changes Made

1. **Added Templates with Styling**
   - Added `index.html` for homepage and user creation.
   - Added `user.html` to show individual user data with a back button.
   - Integrated CSS and basic styling for clarity.

2. **Improved Code Structure**
   - All endpoints now clearly separated.
   - Kept code in `app.py` as per assignment but structured cleanly.

3. **Better HTTP Responses**
   - Added appropriate response codes (e.g., `201` on creation, `404` on not found).

4. **Minor Security Fixes**
   - Used parameterized SQL queries (`?` placeholders) to avoid SQL injection.

5. **Maintained Compatibility**
   - The original endpoints and functionality are fully preserved.

---

## 🤝 Trade-offs / Assumptions

- Passwords are stored in plaintext as per original code. Hashing was avoided to stick to instructions.
- HTML pages are basic and functional, as UI wasn’t the primary focus.

---

## 🧠 If I Had More Time

- Modularize code: separate routes, DB logic, and templates
- Add form validation in frontend
- Implement password hashing and user authentication securely
- Add Flask Blueprints for better organization
- Add test coverage for each endpoint

---

## 🤖 AI Usage

- **Tool Used**: ChatGPT (OpenAI GPT-4)
- **Used For**: Styling support, organization suggestions, README structure
- **AI-generated Code**: Modified to fit project structure and requirements
