---
id: FRONTEND
name: Frontend
severity: Medium
category: Governance
version: 1.0.0
---

# FRONTEND.MD - Client-Side Mastery

> **Goal**: Unified management of Web & Mobile Interfaces. One source of truth for user experience.



## 📱 2. MOBILE & RESPONSIVE

1. **Touch Targets**: Buttons at least 44x44px (Thumb standard).
2. **Safe Areas**: Respect Notch and Home Indicator on iOS/Android.
3. **Mobile-First**: Code CSS for mobile first, override for PC later.



## 🛡️ 4. STATE & COMPONENT

1. **Atomic Design**: Small, highly reusable components (`<Button />`, `<INPUT />`).
2. **State**: Server State (TanStack Query) !== Client State (Zustand/Context). Clear separation.
