# Logo Component Documentation

## High-Level Overview

The `Logo` component (`Logo.jsx`) defines the visual brand identity of **ArthaNetra AI** across the application. It establishes high-impact brand recognition on authentication pages, workspace headers, and navigation bars.

### Core Purpose & Business Logic
* **Brand Visual Anchor:** Combines a vibrant, rounded gradient badge containing an upward financial trend graph (`FiTrendingUp`) with multi-tone gradient typography (`ArthaNetra`).
* **Interactive Micro-Animation:** Incorporates subtle hover physics (`hover:rotate-6 transition-transform duration-300`), creating a polished and dynamic feel during user navigation.

---

## Interface Breakdown

### Component Signature & Return Type
* **Component Name:** `Logo`
* **Return Type:** `JSX.Element`

### Props & Parameters Table

| Prop Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `className` | `string` | `"text-3xl"` | Custom Tailwind font sizing or spacing classes applied directly to the flex root container. Controls overall typographic scaling. |

---

## Architecture & Flow

### Visual Structure & Layering Diagram

```mermaid
graph TD
    subgraph Logo Root Flex Container [Logo.jsx Root Div]
        Direction[Flex Items Center Gap-2.5 Font-Extrabold]
        
        subgraph Icon Badge Layer
            IconBox[Div: w-10 h-10 rounded-2xl bg-gradient-to-tr hover:rotate-6]
            Icon[Icon: FiTrendingUp stroke-2.5]
            IconBox --> Icon
        </Direction>
        
        subgraph Typography Layer
            Span[Span: bg-gradient-to-r bg-clip-text text-transparent]
            TextPrefix[Text: Artha]
            TextSuffix[Span: Netra text-blue-600 font-black]
            Span --> TextPrefix
            Span --> TextSuffix
        </Direction>
    end
```

---

## Dependencies & Environment

### External & Internal Dependencies

| Dependency | Type | Purpose |
| :--- | :--- | :--- |
| `react-icons/fi` (`FiTrendingUp`) | External Package | Provides clean SVG vector iconography representing financial growth. |
| Tailwind CSS | Styling Engine | Supplies background gradient clipping (`bg-clip-text text-transparent`), box shadows, and transform hover utilities. |

### Environment Variables & API Interactions
* **Environment Variables:** None required.
* **API/Data Interactions:** None.

---

## Security & Limitations

### Security Considerations
* **Static Presentation Element:** Completely safe static visual component with no data injection points or stateful handlers.

### Limitations & Edge Cases
* **Fixed Icon Box Scaling:** While the root container accepts a `className` prop to scale text font sizes (`text-xl`, `text-3xl`), the icon badge box dimensions (`w-10 h-10`) are hardcoded. At very large or very small text scales, icon-to-text proportions may become unbalanced unless modified.
