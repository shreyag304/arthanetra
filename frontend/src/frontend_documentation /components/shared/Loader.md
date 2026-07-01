# Loader Component Documentation

## High-Level Overview

The `Loader` component (`Loader.jsx`) is a compact, high-performance visual loading indicator used throughout **ArthaNetra AI** to signify active background operations, asynchronous API calls, and interface state transitions.

### Core Purpose & Business Logic
* **Uniform Spin Animation:** Utilizes Tailwind CSS CSS keyframe animations (`animate-spin`) to render a smooth, continuous rotating circular border.
* **Standardized Size Hierarchy:** Maps predefined size tokens (`sm`, `md`, `lg`) to exact width, height, and border thickness dimensions, maintaining visual proportion whether embedded inside buttons, cards, or full-screen overlays.

---

## Interface Breakdown

### Component Signature & Return Type
* **Component Name:** `Loader`
* **Return Type:** `JSX.Element`

### Props & Parameters Table

| Prop Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Determines the diameter and border stroke width of the spinner. Falls back to `"md"` if an unmapped string is supplied. |
| `className` | `string` | `""` | Additional Tailwind classes appended to the outer centering wrapper `<div>`. |

### Size Token Configuration Mapping

| Size Token | Dimensions (`w-* h-*`) | Border Stroke | Usage Context |
| :--- | :--- | :--- | :--- |
| `sm` | `w-4 h-4` (16px × 16px) | `border-2` | Inside compact buttons, badges, and inline text prompts. |
| `md` | `w-5 h-5` (20px × 20px) | `border-2` | Standard buttons, card footers, and widget refresh indicators. |
| `lg` | `w-8 h-8` (32px × 32px) | `border-3` | Page-level loading screens, modal overlays, and initialization screens. |

---

## Architecture & Flow

### Render Logic Diagram

```mermaid
flowchart LR
    ReceiveProps[Props: size, className] --> SizeLookup{Lookup sizeClasses[size]}
    SizeLookup -->|Found| MatchSize[Apply matched w-* h-* border-*]
    SizeLookup -->|Not Found / Invalid| FallbackSize[Apply default md: w-5 h-5 border-2]
    
    MatchSize --> SpinnerDOM[Render Animated Spinner Div<br/>animate-spin border-t-white]
    FallbackSize --> SpinnerDOM
```

---

## Dependencies & Environment

### External & Internal Dependencies

| Dependency | Type | Purpose |
| :--- | :--- | :--- |
| `React` (Implicit) | Core Framework | Functional JSX component rendering. |
| Tailwind CSS | Styling Engine | Supplies `animate-spin` CSS animation class and layout sizing primitives. |

### Environment Variables & API Interactions
* **Environment Variables:** None required.
* **API/Data Interactions:** None.

---

## Security & Limitations

### Security Considerations
* **Static Presentation Element:** Completely passive visual element with no user input handling or external network interactions.

### Limitations & Edge Cases
* **Color Hardcoding:** The spinner color relies on `border-white/30 border-t-white`. If rendered against a light white or pale gray background without overriding wrapper styling, the spinner may suffer from poor contrast or become invisible unless customized.
