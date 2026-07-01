# Card Component Documentation

## High-Level Overview

The `Card` component (`Card.jsx`) is a specialized surface container within **ArthaNetra AI** designed to encapsulate layout modules, forms, and widgets. Its primary role is to enforce visual harmony, depth, and glassmorphic aesthetics across the application.

### Core Purpose & Business Logic
* **Glassmorphic Surface Design:** Applies semi-transparent white backgrounds (`bg-white/90`), deep backdrop blurring (`backdrop-blur-xl`), and subtle borders (`border-white/60`) to create a floating, modern visual layer against dark or animated gradients.
* **Consistent Layout Geometry:** Provides uniform border radius (`rounded-3xl`), responsive padding (`p-8 sm:p-10`), and deep ambient shadowing (`shadow-2xl shadow-indigo-950/5`), ensuring visual uniformity across authentication screens and workspace panels.

---

## Interface Breakdown

### Component Signature & Return Type
* **Component Name:** `Card`
* **Return Type:** `JSX.Element`

### Props & Parameters Table

| Prop Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `children` | `React.ReactNode` | Required | Content enclosed within the card surface (e.g., forms, lists, text, or nested layouts). |
| `className` | `string` | `""` | Additional or overriding Tailwind utility classes applied to the root container `<div>`. |

---

## Architecture & Flow

### Component Structure & Composition Diagram

```mermaid
graph LR
    subgraph Card Surface Container [Card.jsx Root Div]
        Direction[Tailwind Base Classes:<br/>bg-white/90 backdrop-blur-xl rounded-3xl p-8 sm:p-10]
        Custom[Prop: className appended]
        
        subgraph Child Injection
            Children[Prop: children rendered inside]
        </Direction>
    end
```

---

## Dependencies & Environment

### External & Internal Dependencies

| Dependency | Type | Purpose |
| :--- | :--- | :--- |
| `React` (Implicit) | Core Framework | JSX functional component rendering. |
| Tailwind CSS | Styling Engine | Utility classes for backdrop filters, spacing, shadows, and borders. |

### Environment Variables & API Interactions
* **Environment Variables:** None required.
* **API/Data Interactions:** None; purely presentational container.

---

## Security & Limitations

### Security Considerations
* **Passive Layout Wrapper:** Acts purely as a structural layout DOM element (`<div>`). Does not process user input or perform network operations.

### Limitations & Edge Cases
* **CSS Specificity & Padding Overrides:** Because classes are concatenated using standard template literals (`bg-white/90 ... p-8 sm:p-10 ... ${className}`), overriding default padding requires CSS `!important` flags (e.g., `!p-6 sm:!p-8` used in `Login.jsx`) unless processed by a specificity resolution utility such as `clsx` + `tailwind-merge`.
