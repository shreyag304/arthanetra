# PersonaCard Component Documentation

## High-Level Overview
The `PersonaCard` component displays the active demographic profile and income classification assigned to the current user by ArthaNetra AI's inference engine. Its core purpose is to verify user identity attributes (such as occupation or socioeconomic segment) and show the corresponding income profile used to customize conversational advice.

Within the Context Panel sidebar, it provides visual reassurance that user profiles are verified while highlighting their specific income profile or demographic classification.

## Interface Breakdown

### Component Props
| Prop Name | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `persona` | `string` | Optional | `"Student"` | The categorical classification assigned to the user profile (e.g., `"Student"`, `"Farmer"`, `"MSME Owner"`). |
| `incomeType` | `string` | Optional | `"Variable"` | The user's income classification or profile type (e.g., `"Variable"`, `"Salaried"`). |

### Visual Layout Sections
| Section | Elements Displayed | Styling Theme |
| :--- | :--- | :--- |
| **Card Header** | User Check Icon (`FiUserCheck`) and `"Verified"` shield badge (`FiShield`). | Purple & Indigo accent colors. |
| **Profile Display** | Assigned persona string (`persona`). | Bold white typography (`text-base font-bold`). |
| **Income Indicator** | Dynamic income type classification (`incomeType`). | Purple highlight (`text-purple-300`). |

## Architecture & Flow

```mermaid
graph TD
    Telemetry[Telemetry Context] -->|persona & income_type| PC[PersonaCard Component]
    PC --> Header[Render Icon & Verified Badge]
    PC --> Body[Render Persona & Income Type Box]
```

## Dependencies & Environment

### External Packages
- **`react-icons/fi`**: Uses Feather icons (`FiUserCheck`, `FiShield`) for identity verification cues.
- **Tailwind CSS**: Leverages translucent backgrounds (`bg-slate-800/60`), border styling, and hover brightening effects (`hover:bg-slate-800/80`).
