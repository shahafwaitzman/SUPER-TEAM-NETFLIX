# Super Team Academy - Red Design UI Specification

## Document Version
- **Created**: 2026-04-18
- **Design**: Netflix-Style Red Accent with Dark Overlay
- **Language**: Hebrew (RTL)
- **Font Family**: Heebo (weights: 300, 400, 700, 900)

---

## 1. GLOBAL SETTINGS

### Body/Background
- **Background Color**: `#000000` (pure black)
- **Text Color Default**: `#ffffff` (white)
- **Font Family**: 'Heebo', sans-serif
- **Direction**: RTL (right-to-left)
- **Min Height**: 100vh (full viewport height)

### Accent Color Palette
- **Primary Red**: `#e50914` (Netflix red)
- **Dark Blues**: `#0a0e27`, `#1a1a2e`, `#0a0a1a` (card gradients)
- **Semi-transparent Red**: `rgba(229,9,20,0.2)` - `rgba(229,9,20,0.4)`

---

## 2. NAVIGATION BAR

### Container
- **Position**: Fixed (top: 0, left: 0, right: 0)
- **Z-Index**: 1000
- **Height**: ~70px
- **Background**: `linear-gradient(180deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.4) 100%)`
- **Padding**: 20px 60px
- **Backdrop Filter**: `blur(10px)`
- **Display**: Flex with space-between

### Logo
- **Font Size**: 28px
- **Font Weight**: 900
- **Color**: `#e50914` (red)
- **Letter Spacing**: 3px
- **Text**: "SUPER TEAM 🔴"

### Navigation Links
- **Gap**: 50px
- **Font Size**: 15px
- **Font Weight**: 500
- **Color**: `#ffffff`
- **Padding**: 8px 0

#### Link Underline (::after)
- **Height**: 3px
- **Background**: `#e50914`
- **Width**: 0 → 100% on hover
- **Transition**: width 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)

### User Button
- **Font Size**: 14px
- **Padding**: 10px 24px
- **Background**: `rgba(229,9,20,0.2)`
- **Border**: 1px solid `rgba(229,9,20,0.3)`
- **Border Radius**: 6px
- **Font Weight**: 600

**Hover**: Background `rgba(229,9,20,0.3)`, Border `#e50914`

---

## 3. HERO SECTION

### Hero Container
- **Width**: 100%
- **Height**: 100vh
- **Padding Top**: 60px
- **Position**: relative
- **Display**: flex (center align)
- **Overflow**: hidden

### Background Image (::before)
- **URL**: `https://drive.google.com/uc?id=13JtFgrLuWvQGhmDA79FiTKpaUbY0xAvb`
- **Position**: absolute (full cover)
- **Background Size**: cover
- **Z-Index**: 0

### Dark Overlay (::after)
- **Background**: `linear-gradient(135deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.5) 50%, rgba(0,0,0,0.3) 100%)`
- **Position**: absolute (full cover)
- **Z-Index**: 1

### Hero Content
- **Position**: relative (z-index: 10)
- **Text Align**: center
- **Max Width**: 700px
- **Animation**: slideUp 0.9s cubic-bezier(0.34, 1.56, 0.64, 1)

#### Hero Title
- **Font Size**: 96px
- **Font Weight**: 900
- **Color**: `#e50914`
- **Text Shadow**: `0 10px 40px rgba(0,0,0,0.8)`
- **Letter Spacing**: -2px
- **Text**: "SUPER TEAM"

#### Hero Accent Line
- **Width**: 60px
- **Height**: 3px
- **Background**: `#e50914`
- **Margin**: 20px auto

#### Hero Subtitle
- **Font Size**: 32px
- **Color**: `#ffffff`
- **Margin Bottom**: 50px
- **Text Shadow**: `0 4px 20px rgba(0,0,0,0.7)`
- **Letter Spacing**: -0.5px
- **Text**: "ACADEMY"

### Hero Buttons
- **Display**: flex
- **Gap**: 20px
- **Justify Content**: center

#### Button (.btn)
- **Padding**: 14px 40px
- **Font Size**: 15px
- **Font Weight**: 700
- **Border**: 1px solid `rgba(255,255,255,0.4)`
- **Border Radius**: 6px
- **Color**: `#ffffff`
- **Background**: transparent
- **Transition**: all 0.3s ease

#### Button Ripple (::before)
- **Width/Height**: 0 → 300px on hover
- **Background**: `rgba(255,255,255,0.1)`
- **Border Radius**: 50%
- **Transition**: width 0.6s, height 0.6s
- **Z-Index**: 0

#### Button Primary
- **Border Color**: `rgba(255,255,255,0.5)`
- **Hover**: Background `rgba(255,255,255,0.1)`, Border `#ffffff`, Transform `translateY(-2px)`

#### Button Secondary
- **Border Color**: `rgba(255,255,255,0.3)`
- **Hover**: Background `rgba(255,255,255,0.05)`, Border `rgba(255,255,255,0.5)`, Transform `translateY(-2px)`

---

## 4. MAIN CONTAINER

- **Max Width**: 1700px
- **Margin**: 0 auto
- **Padding**: 100px 60px
- **Background**: `#000000`

---

## 5. SECTIONS

### Section Title
- **Font Size**: 48px
- **Font Weight**: 900
- **Letter Spacing**: -1px

### Section Description
- **Font Size**: 16px
- **Color**: `#aaa`
- **Font Weight**: 300
- **Max Width**: 600px
- **Line Height**: 1.6

---

## 6. COURSE CARDS GRID

### Grid Container
- **Display**: grid
- **Grid Template Columns**: `repeat(auto-fill, minmax(300px, 1fr))`
- **Gap**: 40px
- **Grid Auto Rows**: 400px

### Course Card
- **Border Radius**: 12px
- **Overflow**: hidden
- **Background**: `#000000`
- **Border**: 1px solid `rgba(229,9,20,0.1)`
- **Box Shadow**: `0 8px 16px rgba(0,0,0,0.2)`
- **Transition**: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)

**Hover**: Transform `translateY(-20px)`, Border `#e50914`, Box-Shadow `0 40px 80px rgba(229,9,20,0.3)`

### Course Image
- **Background**: `linear-gradient(135deg, #1a1a2e 0%, #0a0e27 50%, #0a0a1a 100%)`
- **Display**: flex (centered)
- **Font Size**: 80px

#### Image Glow (::before)
- **Background**: `radial-gradient(circle at 30% 30%, rgba(229,9,20,0.3) 0%, transparent 60%)`
- **Opacity**: 0 → 1 on hover
- **Z-Index**: 2

#### Image Overlay (::after)
- **Background**: `linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.8) 100%)`
- **Opacity**: 0 → 1 on hover
- **Z-Index**: 3

### Course Content
- **Position**: absolute (bottom: 0)
- **Padding**: 30px
- **Transform**: translateY(40px)
- **Opacity**: 0
- **Z-Index**: 5

**Hover**: Transform `translateY(0)`, Opacity `1`

#### Course Title
- **Font Size**: 24px
- **Font Weight**: 900
- **Color**: `#e50914`
- **Letter Spacing**: -0.5px

#### Course Description
- **Font Size**: 14px
- **Color**: `#ddd`
- **Line Height**: 1.6
- **Font Weight**: 400

#### Course Badge
- **Background**: `rgba(229,9,20,0.4)`
- **Color**: `#ffffff`
- **Padding**: 8px 14px
- **Border Radius**: 6px
- **Font Weight**: 800
- **Font Size**: 12px
- **Letter Spacing**: 1px

#### Course Episodes
- **Color**: `#aaa`
- **Font Size**: 13px
- **Font Weight**: 600

---

## 7. INFO SECTION

- **Padding**: 60px 40px
- **Background**: `linear-gradient(135deg, rgba(229,9,20,0.05) 0%, rgba(0,0,0,0) 100%)`
- **Border Radius**: 12px
- **Border**: 1px solid `rgba(229,9,20,0.1)`
- **Box Shadow**: `0 8px 16px rgba(0,0,0,0.15)`

### Info Icon
- **Font Size**: 64px
- **Margin Bottom**: 20px

### Info Title
- **Font Size**: 32px
- **Font Weight**: 900

### Info Text
- **Font Size**: 16px
- **Color**: `#aaa`
- **Line Height**: 1.8

---

## 8. ANIMATIONS

### slideUp
```css
@keyframes slideUp {
  from { opacity: 0; transform: translateY(60px); }
  to { opacity: 1; transform: translateY(0); }
}
```
- **Duration**: 0.9s
- **Timing**: cubic-bezier(0.34, 1.56, 0.64, 1)

---

## 9. RESPONSIVE BREAKPOINTS

### Desktop (> 1200px)
- Container Padding: 100px 60px
- Hero Title: 96px
- Grid: `repeat(auto-fill, minmax(300px, 1fr))`, gap 40px

### Tablet (768px - 1200px)
- Container Padding: 80px 40px
- Hero Title: 72px
- Grid: `repeat(auto-fill, minmax(250px, 1fr))`, gap 30px

### Mobile (< 768px)
- Nav Padding: 15px 20px
- Hero Title: 48px
- Hero Subtitle: 20px
- Container Padding: 60px 20px
- Section Title: 32px
- Grid: 1 column, gap 20px, auto-rows 300px
- Buttons: 100% width, flex-direction column

---

## 10. COLOR REFERENCE

| Element | Hex | RGB | Opacity | Usage |
|---------|-----|-----|---------|-------|
| Primary Red | #e50914 | 229,9,20 | 100% | Titles, accents |
| White | #ffffff | 255,255,255 | 100% | Text, buttons |
| Black | #000000 | 0,0,0 | 100% | Background |
| Dark Blue 1 | #0a0e27 | 10,14,39 | 100% | Card gradients |
| Dark Blue 2 | #1a1a2e | 26,26,46 | 100% | Card gradients |
| Dark Blue 3 | #0a0a1a | 10,10,26 | 100% | Card gradients |
| Light Gray | #aaa | 170,170,170 | 100% | Secondary text |
| Card Gray | #ddd | 221,221,221 | 100% | Card text |

---

## 11. SHADOW EFFECTS

| Element | Definition | Purpose |
|---------|-----------|---------|
| Hero Title | 0 10px 40px rgba(0,0,0,0.8) | Deep shadow |
| Hero Subtitle | 0 4px 20px rgba(0,0,0,0.7) | Subtle shadow |
| Cards Default | 0 8px 16px rgba(0,0,0,0.2) | Card depth |
| Cards Hover | 0 40px 80px rgba(229,9,20,0.3) | Red glow |
| Info Section | 0 8px 16px rgba(0,0,0,0.15) | Subtle shadow |

---

## 12. Z-INDEX HIERARCHY

| Z-Index | Element | Purpose |
|---------|---------|---------|
| 1000 | nav | Fixed top |
| 10 | .hero-content | Above overlay |
| 5 | .course-content | Card content reveal |
| 3 | .course-image::after | Dark overlay |
| 2 | .course-image::before | Red glow |
| 1 | .hero::after | Dark overlay |
| 0 | .hero::before | Background |

---

## 13. TEXT CONTENT

**Navigation:** "SUPER TEAM 🔴" | "בית" | "קורסים" | "בחקור" | "חם" | "😊 משתמש"

**Hero:** "SUPER TEAM" | "ACADEMY" | "צפייה" | "מידע נוסף"

**Courses:** "🎬 קורסים וסדרות" | "סדרה מלאה של תוכניות לימודיות - בקרוב יחובר עם הדרייב שלך"

**Info:** "📁" | "תוכן עוד בדרך" | "בקרוב נחבר את תיקיות Google Drive שלך וכל הסדרות והקורסים החדשים יופיעו כאן בעיצוב זה"

---

## Summary

**Netflix-Style Premium Design:**
✓ Bold red titles with dramatic shadows
✓ Dark overlay gradient (0.7→0.3 opacity)
✓ Interactive card lift and ripple effects
✓ Glass morphism navigation
✓ Consistent red accent throughout
✓ Full RTL Hebrew support
✓ Responsive across all devices

All values are exact specifications for pixel-perfect implementation.
